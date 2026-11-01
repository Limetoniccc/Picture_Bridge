"""Regression checks for the requested, minimal v1.1 UI reorganization."""
from pathlib import Path
from unittest.mock import patch
import os
import tempfile
import tkinter as tk
import unittest

from app import App
from app_info import APP_VERSION
from i18n import LANGUAGES, tr

ROOT = Path(__file__).resolve().parents[1]


class UiOrganizationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.env = patch.dict(os.environ, {'PICTURE_BRIDGE_CONFIG_DIR': self.temp.name})
        self.env.start()
        try:
            self.root = tk.Tk()
        except tk.TclError as error:
            self.env.stop()
            self.temp.cleanup()
            self.skipTest(f'No display: {error}')
        self.app = App(self.root)
        self.root.update()

    def tearDown(self):
        self.root.destroy()
        self.env.stop()
        self.temp.cleanup()

    def widget(self, key):
        return next(w for w, k, _ in self.app._translatables if k == key)

    def test_section_numbering_and_button_grouping(self):
        self.assertEqual(APP_VERSION, '1.1')
        group_import = self.widget('input_section')
        group_export = self.widget('export_section')
        group_options = self.widget('pf3_settings')
        self.assertTrue(group_import.cget('text').startswith('1.'))
        self.assertTrue(group_options.cget('text').startswith('2.'))
        self.assertTrue(group_export.cget('text').startswith('3.'))
        for key in ('open_lut', 'open_photo'):
            self.assertEqual(str(self.widget(key).master.master), str(group_import))
        for key in ('resample', 'save_xmp', 'save_pf3'):
            self.assertEqual(str(self.widget(key).master.master), str(group_export))
        self.assertEqual(str(self.widget('save_lumix').master.master), str(group_export))
        # Canon PSE install is in the title bar, above source/preview/export.
        self.assertLess(self.widget('install_pse').winfo_rooty(), group_import.winfo_rooty())
        self.assertGreater(self.widget('save_lumix').winfo_width(), 0)
        self.assertLess(self.widget('save_lumix').winfo_rooty() + self.widget('save_lumix').winfo_height(),
                        self.root.winfo_rooty() + self.root.winfo_height())

    def test_requested_labels_in_all_languages(self):
        expected_ko = {
            'mode_canon': 'JPG 기준 현상',
            'mode_reference': 'RAW 기준 현상',
            'preview_source': '기본 현상',
            'preview_canon_base': '기본 현상',
            'preview_lut_target': 'LUT 적용 현상',
            'preview_canon_result': 'PF3 적용 현상',
        }
        for key, value in expected_ko.items():
            self.assertEqual(tr('ko', key), value)
        for code in LANGUAGES:
            for key in ('resample','save_xmp','save_pf3','save_lumix'):
                self.assertFalse(tr(code, key)[0].isdigit(), (code,key))
            self.app.language_label.set(LANGUAGES[code])
            self.app.change_language()
            self.root.update_idletasks()
            self.assertEqual(self.widget('input_section').cget('text'), tr(code, 'input_section'))
            self.assertEqual(self.widget('export_section').cget('text'), tr(code, 'export_section'))

    def test_style_name_suffix(self):
        self.assertEqual(self.app._name_with_pb_suffix('Warm Look'), 'Warm Look_PB')
        self.assertEqual(self.app._name_with_pb_suffix('Warm Look_PB'), 'Warm Look_PB')
        self.assertEqual(self.app._name_with_pb_suffix('Warm Look_PB_PB'), 'Warm Look_PB')
        self.assertEqual(len(self.app._name_with_pb_suffix('A'*64)), 31)
        self.app.name.set('Custom')
        self.assertEqual(self.app._normalize_style_name(), 'Custom_PB')
        self.assertEqual(self.app.name.get(), 'Custom_PB')
        with patch('app.filedialog.askopenfilename', return_value=str(ROOT/'example_luts'/'identity_2.cube')):
            self.app.open_cube()
        self.assertEqual(self.app.name.get(), 'identity_2_PB')
        self.app.name.set('Manual Edit')
        with patch('app.filedialog.asksaveasfilename', return_value='/tmp/pb-v11-style-test.cube'), \
             patch('app.export_srgb_cube', return_value={'strength': 0.5}) as converter, \
             patch('app.messagebox.showinfo'):
            self.app.resample()
        self.assertEqual(converter.call_args.kwargs['title'], 'Manual Edit_PB')


if __name__ == '__main__':
    unittest.main()
