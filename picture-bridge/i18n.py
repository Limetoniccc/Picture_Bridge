"""Picture Bridge GUI translations. All UI text is offline, no web translation/API."""
from __future__ import annotations

import json
import os
from pathlib import Path

LANGUAGES = {'ko': '한국어', 'en': 'English', 'ja': '日本語', 'zh-CN': '简体中文'}
LANGUAGE_LABELS = {label: code for code, label in LANGUAGES.items()}
DEFAULT_LANGUAGE = 'ko'

# Each tuple: Korean, English, Japanese, Simplified Chinese.
_MESSAGES = {
    'app_title': ('{name} | CUBE / XMP → PF3 · CUBE → XMP',)*4,
    'language': ('언어', 'Language', '言語', '语言'),
    'about': ('프로그램 정보', 'About', 'アプリ情報', '关于软件'),
    'credit': ('버전 {version}  ·  제작자 : {author}', 'Version {version}  ·  Created by: {author}', 'バージョン {version}  ·  制作者：{author}', '版本 {version}  ·  制作者：{author}'),
    'description': ('Canon PF3 파일 직접 생성 · 캐논 Picture Style Editor 설치본의 직렬화 엔진 사용',
                    'Create Canon PF3 files using the serialization engine from installed Canon Picture Style Editor',
                    'インストール済みのCanon Picture Style EditorのエンジンでPF3ファイルを生成します',
                    '使用已安装的 Canon Picture Style Editor 引擎生成 PF3 文件'),
    'open_lut': ('1. .cube / .xmp 불러오기', '1. Open .cube / .xmp', '1. .cube / .xmp を開く', '1. 打开 .cube / .xmp'),
    'open_photo': ('사진 / RAW 미리보기', 'Preview photo / RAW', '写真 / RAW プレビュー', '照片 / RAW 预览'),
    'resample': ('33³ .cube 저장 (선택)', 'Save 33³ .cube (optional)', '33³ .cube を保存（任意）', '保存 33³ .cube（可选）'),
    'choose_lut': ('CUBE 또는 Adobe XMP 파일을 선택해 주세요.', 'Select a CUBE or Adobe XMP file.', 'CUBEまたはAdobe XMPファイルを選択してください。', '请选择 CUBE 或 Adobe XMP 文件。'),
    'photo_ready': ('JPEG·PNG·TIFF 및 카메라 RAW를 열 수 있습니다.', 'Open JPEG, PNG, TIFF and camera RAW files.', 'JPEG・PNG・TIFFおよびカメラRAWを開けます。', '支持打开 JPEG、PNG、TIFF 和相机 RAW 文件。'),
    'comparison_mode': ('비교 화면', 'Comparison mode', '比較モード', '对比模式'),
    'mode_canon': ('캐논 PF3 실제 현상', 'Actual Canon PF3 rendering', 'Canon PF3 実レンダリング', 'Canon PF3 实际渲染'),
    'mode_reference': ('고해상도 LUT 목표 참고', 'High-resolution LUT reference', '高解像度 LUT 参照', '高分辨率 LUT 参考'),
    'canon_preview_note': ('캐논 실제 현상: Canon RAW + PSE 필요 · 검증 해상도 1080×1620',
                           'Canon rendering: RAW + PSE required · tested at 1080×1620',
                           'Canon実レンダリング：RAWとPSEが必要 · 検証済み 1080×1620',
                           'Canon 实际渲染：需要 RAW 和 PSE · 已测试 1080×1620'),
    'pf3_settings': ('2. PF3 내보내기 설정', '2. PF3 export settings', '2. PF3 書き出し設定', '2. PF3 导出设置'),
    'style_name': ('스타일 이름', 'Style name', 'スタイル名', '样式名称'),
    'base_style': ('기준 스타일', 'Base style', '基本スタイル', '基础样式'),
    'strength': ('변환 강도', 'Effect strength', '変換の強度', '转换强度'),
    'canon_engine': ('Canon 엔진', 'Canon engine', 'Canonエンジン', 'Canon 引擎'),
    'choose_path': ('위치 선택', 'Browse', '参照', '浏览'),
    'check_installation': ('설치 확인', 'Check installation', 'インストール確認', '检查安装'),
    'dll_note': ('비워두면 자동 검색합니다. Windows에서 Canon Picture Style Editor 설치가 필요합니다.',
                 'Leave blank to search automatically. Canon Picture Style Editor must be installed on Windows.',
                 '空欄の場合は自動検索します。WindowsにCanon Picture Style Editorのインストールが必要です。',
                 '留空则自动查找。Windows 上需要安装 Canon Picture Style Editor。'),
    'save_pf3': ('3. 실제 .pf3 파일 생성', '3. Generate .pf3 file', '3. .pf3 ファイルを生成', '3. 生成 .pf3 文件'),
    'save_xmp': ('4. .cube → Lightroom .xmp 생성', '4. .cube → Lightroom .xmp', '4. .cube → Lightroom .xmp を生成', '4. .cube → 生成 Lightroom .xmp'),
    'install_pse': ('캐논 PSE 설치', 'Install Canon PSE', 'Canon PSEを入手', '安装 Canon PSE'),
    'footnote': ('PF3는 DPP가 읽는 색상 계수·톤 커브로 근사합니다. 실제 현상 화면으로 색감을 확인하세요. XMP 프리셋은 지원되는 색상 조정만 근사하며, 카메라 실물은 미검증입니다.',
                 'PF3 approximates color coefficients and tone curves read by DPP. Check the actual Canon rendering. XMP preset adjustments are approximated; physical camera compatibility is unverified.',
                 'PF3はDPPが読み取る色係数とトーンカーブで近似します。Canonの実レンダリングで確認してください。XMPプリセットも近似変換であり、実機互換性は未検証です。',
                 'PF3 使用 DPP 可读取的色彩系数和色调曲线进行近似。请检查 Canon 实际渲染。XMP 预设仅近似转换，尚未验证相机实机兼容性。'),
    'license': ('오픈소스 (MIT 라이선스)', 'Open source (MIT License)', 'オープンソース（MITライセンス）', '开源软件（MIT 许可证）'),
    'file_filter_lut_xmp': ('색상 LUT / Adobe XMP', 'Color LUT / Adobe XMP', 'カラーLUT / Adobe XMP', '颜色 LUT / Adobe XMP'),
    'file_filter_cube': ('CUBE 3D LUT',)*4,
    'file_filter_xmp': ('Lightroom / Camera Raw XMP',)*4,
    'file_filter_all': ('모든 파일', 'All files', 'すべてのファイル', '所有文件'),
    'file_filter_photos': ('사진 및 RAW', 'Photos and RAW', '写真とRAW', '照片和 RAW'),
    'file_filter_canon_raw': ('Canon RAW',)*4,
    'file_filter_camera_raw': ('카메라 RAW', 'Camera RAW', 'カメラRAW', '相机 RAW'),
    'file_filter_raster': ('일반 사진', 'Standard images', '一般の画像', '普通照片'),
    'cube_loaded': ('{name} | CUBE {size}³ | {count:,} RGB 좌표 | Domain: {domain_min} ~ {domain_max}',
                    '{name} | CUBE {size}³ | {count:,} RGB samples | Domain: {domain_min} ~ {domain_max}',
                    '{name} | CUBE {size}³ | RGB {count:,}点 | Domain: {domain_min} ～ {domain_max}',
                    '{name} | CUBE {size}³ | {count:,} 个 RGB 采样点 | 范围：{domain_min} ~ {domain_max}'),
    'xmp_profile': ('내장 RGB LUT 프로파일', 'Embedded RGB LUT profile', 'RGB LUT内蔵プロファイル', '内嵌 RGB LUT 配置文件'),
    'xmp_preset': ('Lightroom 보정 프리셋 · 근사 변환', 'Lightroom develop preset · approximation', 'Lightroom現像プリセット・近似変換', 'Lightroom 调整预设 · 近似转换'),
    'xmp_loaded': ('{name} | {kind} → {size}³ RGB 샘플', '{name} | {kind} → {size}³ RGB samples',
                   '{name} | {kind} → {size}³ RGBサンプル', '{name} | {kind} → {size}³ RGB 采样点'),
    'ignored_settings': (' | 제외: {items}', ' | Omitted: {items}', ' | 対象外：{items}', ' | 已忽略：{items}'),
    'wrong_extension': ('.cube 또는 .xmp 파일만 불러올 수 있습니다.', 'Only .cube and .xmp inputs are supported.',
                        '.cubeまたは.xmpファイルのみ読み込めます。', '仅支持导入 .cube 或 .xmp 文件。'),
    'xmp_warning_title': ('XMP 변환 주의', 'XMP conversion warning', 'XMP変換の注意', 'XMP 转换注意事项'),
    'xmp_warning_profile': ('Adobe XMP 프로파일의 RGB LUT를 가져옵니다. 외부 프로파일 단계와 추가 편집은 재현되지 않습니다.',
                            'The Adobe XMP RGB LUT is imported. External profile stages and extra edits are not reproduced.',
                            'Adobe XMPのRGB LUTを読み込みます。外部プロファイルの処理や追加編集は再現されません。',
                            '已读取 Adobe XMP 的 RGB LUT。无法还原外部配置文件处理阶段和额外调整。'),
    'xmp_warning_conversion': ('내장 색 공간 {space}을(를) 표시용 sRGB로 변환했습니다. 색역 제한이 발생할 수 있습니다.',
                               'Converted embedded color space {space} to display sRGB. Gamut clipping may occur.',
                               '埋め込み色空間 {space} を表示用sRGBに変換しました。色域外の値はクリップされる場合があります。',
                               '已将内嵌色彩空间 {space} 转换为显示用 sRGB，可能发生色域裁剪。'),
    'xmp_warning_preset': ('Lightroom 현상 프리셋은 표시용 RGB에서 근사 변환합니다. Adobe의 현상 결과와 같지 않습니다.',
                           'Lightroom develop presets are approximated in display RGB, not rendered by Adobe’s engine.',
                           'Lightroom現像プリセットは表示用RGBで近似します。Adobeの現像結果とは一致しません。',
                           'Lightroom 调整预设按显示 RGB 进行近似，并不等同于 Adobe 的处理结果。'),
    'xmp_warning_camera': ('참조한 카메라 프로파일은 포함되어 있지 않습니다: {profile}',
                           'Referenced camera profile is not embedded: {profile}',
                           '参照先のカメラプロファイルは内蔵されていません：{profile}',
                           '引用的相机配置文件未内嵌：{profile}'),
    'xmp_warning_look': ('참조한 크리에이티브 룩은 변환된 LUT에 포함되지 않습니다.',
                         'A referenced creative look is not included in the converted LUT.',
                         '参照先のクリエイティブルックは変換後のLUTに含まれません。',
                         '引用的创意外观未包含在转换后的 LUT 中。'),
    'xmp_warning_omitted': ('미지원/제외 설정: {items}', 'Unsupported/omitted settings: {items}',
                            '未対応・除外設定：{items}', '不支持/已忽略的设置：{items}'),
    'read_error': ('LUT / XMP 불러오기 오류', 'LUT / XMP import error', 'LUT / XMPの読み込みエラー', 'LUT / XMP 导入失败'),
    'photo_loading': ('{name} | 사진 읽기 / RAW 현상 중…', '{name} | Loading photo / developing RAW…',
                      '{name} | 画像読み込み / RAW現像中…', '{name} | 正在读取照片 / 处理 RAW…'),
    'photo_load_failed': ('사진 열기 실패 · 기존 미리보기를 유지합니다.', 'Could not open photo · Keeping previous preview.',
                          '画像を開けません · 前のプレビューを維持します。', '无法打开照片 · 保留之前的预览。'),
    'photo_error': ('사진 열기 오류', 'Photo loading error', '画像の読み込みエラー', '照片加载错误'),
    'raw_photo_note': ('{name} | RAW 현상 → sRGB · 카메라 WB · 자동 밝기 꺼짐',
                       '{name} | RAW developed → sRGB · camera WB · auto brightness off',
                       '{name} | RAW現像 → sRGB・カメラWB・自動明るさ補正オフ',
                       '{name} | RAW 处理 → sRGB · 相机白平衡 · 关闭自动亮度'),
    'preview_canon_progress': ('캐논 PF3 실제 현상 계산 중… · 완료될 때까지 이전 화면입니다.',
                               'Rendering Canon PF3… · Previous image remains until done.',
                               'Canon PF3をレンダリング中… · 完了まで前の画像を表示します。',
                               '正在渲染 Canon PF3… · 完成前保留上一次画面。'),
    'preview_source': ('원본 / RAW 기본 현상', 'Original / base RAW rendering', '元画像 / RAW基本現像', '原图 / RAW 基础渲染'),
    'preview_lut_target': ('LUT 목표 참고 (PF3 실제 현상과 구분)', 'LUT target reference (not actual PF3)',
                           'LUTの目標イメージ（PF3実レンダリングではありません）', 'LUT 目标参考（并非实际 PF3 效果）'),
    'preview_canon_unavailable': ('캐논 실제 현상 불가 · 고해상도 LUT 목표 참고 모드를 선택할 수 있습니다.',
                                  'Canon rendering unavailable · Try the high-resolution LUT reference mode.',
                                  'Canon実レンダリング不可 · 高解像度LUT参照モードをご利用ください。',
                                  '无法进行 Canon 实际渲染 · 请改用高分辨率 LUT 参考模式。'),
    'preview_canon_base': ('캐논 기준 스타일 현상', 'Canon base style rendering', 'Canon基本スタイルの現像', 'Canon 基础样式渲染'),
    'preview_canon_result': ('생성 PF3 실제 현상 (캐논 엔진)', 'Generated PF3 (Canon renderer)',
                             '生成PF3の実レンダリング（Canonエンジン）', '生成的 PF3 实际渲染（Canon 引擎）'),
    'preview_canon_report': ('원본 {width:,}×{height:,} px | 캐논 비교 {render_w}×{render_h} | 목표 LUT 대비 평균 RGB 오차 {mae:.1f}/255 (95% {p95:.1f}) · 근사 변환',
                             'Source {width:,}×{height:,} px | Canon comparison {render_w}×{render_h} | Mean RGB error vs LUT target {mae:.1f}/255 (95th {p95:.1f}) · approximate',
                             '元画像 {width:,}×{height:,} px | Canon比較 {render_w}×{render_h} | LUT目標との平均RGB誤差 {mae:.1f}/255（95% {p95:.1f}）・近似',
                             '原图 {width:,}×{height:,} px | Canon 对比 {render_w}×{render_h} | 相对目标 LUT 的平均 RGB 误差 {mae:.1f}/255（95% {p95:.1f}）· 近似'),
    'preview_canon_failed': ('캐논 실제 미리보기 실패: {error}', 'Canon preview failed: {error}',
                             'Canonプレビューに失敗：{error}', 'Canon 预览失败：{error}'),
    'preview_failed': ('미리보기 실패 · 고해상도 LUT 목표 참고 모드를 선택할 수 있습니다.',
                       'Preview failed · Try the high-resolution LUT reference mode.',
                       'プレビューに失敗 · 高解像度LUT参照モードをご利用ください。',
                       '预览失败 · 可使用高分辨率 LUT 参考模式。'),
    'lut_required_title': ('LUT 필요', 'LUT required', 'LUTが必要', '需要 LUT'),
    'lut_required': ('먼저 .cube 또는 .xmp 파일을 불러오세요.', 'First open a .cube or .xmp file.',
                     '先に.cubeまたは.xmpファイルを読み込んでください。', '请先打开 .cube 或 .xmp 文件。'),
    'save_success': ('완료', 'Saved', '保存完了', '保存成功'),
    'save_cube_success': ('33³ LUT 저장: {path}', '33³ LUT saved: {path}', '33³ LUTを保存しました：{path}', '已保存 33³ LUT：{path}'),
    'save_failure': ('실패', 'Error', '失敗', '失败'),
    'cube_required_title': ('CUBE 필요', 'CUBE required', 'CUBEが必要', '需要 CUBE'),
    'cube_required': ('Adobe XMP 프로파일 생성은 .cube 입력에서만 지원합니다.',
                      'Adobe XMP profiles can only be generated from .cube files.',
                      'Adobe XMPプロファイルの生成は.cube入力のみ対応します。',
                      '仅支持从 .cube 文件生成 Adobe XMP 配置文件。'),
    'xmp_saved_status': ('Adobe XMP 프로파일 생성 완료 | {size}³ LUT | {path}',
                         'Adobe XMP profile created | {size}³ LUT | {path}',
                         'Adobe XMPプロファイルの生成完了 | {size}³ LUT | {path}',
                         'Adobe XMP 配置文件已生成 | {size}³ LUT | {path}'),
    'xmp_saved_title': ('XMP 생성 완료', 'XMP created', 'XMP生成完了', 'XMP 已生成'),
    'xmp_saved_body': ('{path}\n\nAdobe Lightroom / Camera Raw에서 [프로파일 및 사전 설정 가져오기]를 사용하세요.\n원본 LUT 재샘플링 평균 RGB 오차: {mae:.2f}/255\n\n{warnings}',
                       '{path}\n\nIn Adobe Lightroom / Camera Raw, use [Import Profiles and Presets].\nMean RGB resampling error vs source LUT: {mae:.2f}/255\n\n{warnings}',
                       '{path}\n\nAdobe Lightroom / Camera Rawで［プロファイルとプリセットの読み込み］を使用してください。\n元LUTに対するリサンプリング平均RGB誤差：{mae:.2f}/255\n\n{warnings}',
                       '{path}\n\n请在 Adobe Lightroom / Camera Raw 中选择「导入配置文件和预设」。\n相对于原始 LUT 的重采样平均 RGB 误差：{mae:.2f}/255\n\n{warnings}'),
    'xmp_saved_warning': ('이 프로파일은 .cube의 색상 변환을 포함합니다. Lightroom 현상 슬라이더는 생성되지 않습니다.',
                          'This profile embeds the .cube color transform; it does not create editable Develop sliders.',
                          'このプロファイルには.cubeの色変換が含まれます。編集可能な現像スライダーは作成されません。',
                          '此配置文件嵌入 .cube 的色彩变换，不会生成可编辑的调整滑块。'),
    'xmp_failed': ('XMP 생성 실패', 'XMP export failed', 'XMPの生成に失敗', 'XMP 导出失败'),
    'dll_dialog_title': ('Picture Style Editor의 EdsCFParse.dll 선택', 'Select EdsCFParse.dll from Picture Style Editor',
                         'Picture Style EditorのEdsCFParse.dllを選択', '选择 Picture Style Editor 中的 EdsCFParse.dll'),
    'dll_found': ('Canon 엔진 발견', 'Canon engine found', 'Canonエンジンを検出', '找到 Canon 引擎'),
    'dll_not_found': ('Canon 엔진을 찾지 못했습니다', 'Canon engine not found', 'Canonエンジンが見つかりません', '未找到 Canon 引擎'),
    'os_unsupported': ('지원 OS', 'Unsupported system', '非対応OS', '不支持的系统'),
    'pf3_windows_only': ('PF3 생성은 Canon PSE Windows DLL이 필요합니다.',
                         'PF3 generation requires the Canon PSE Windows DLL.',
                         'PF3の生成にはCanon PSEのWindows DLLが必要です。',
                         '生成 PF3 需要 Canon PSE 的 Windows DLL。'),
    'pf3_saved_status': ('PF3 근사 변환 저장 · 모델 평균 RGB 오차 {mae:.1f}/255: {path}',
                         'Approximate PF3 exported · Mean model RGB error {mae:.1f}/255: {path}',
                         'PF3の近似変換を保存 · モデル平均RGB誤差 {mae:.1f}/255：{path}',
                         'PF3 近似转换已保存 · 模型平均 RGB 误差 {mae:.1f}/255：{path}'),
    'pf3_saved_title': ('PF3 생성 완료', 'PF3 created', 'PF3生成完了', 'PF3 已生成'),
    'pf3_xmp_caveat': ('XMP의 Lightroom/Camera Raw 보정과는 일치하지 않을 수 있습니다.\n',
                       'This may not match Lightroom/Camera Raw XMP adjustments.\n',
                       'Lightroom/Camera RawのXMP補正とは一致しない場合があります。\n',
                       '结果可能与 Lightroom/Camera Raw 的 XMP 调整不一致。\n'),
    'pf3_saved_body': ('{path}\n\n{bytes:,} bytes\nSHA256 {sha}…\n모델 평균 RGB 오차: {mae:.1f}/255 (근사치)\n{xmp_note}DPP에서 결과를 확인한 뒤 사용하세요.\n카메라 호환성은 아직 검증되지 않았습니다.',
                       '{path}\n\n{bytes:,} bytes\nSHA256 {sha}…\nMean model RGB error: {mae:.1f}/255 (estimate)\n{xmp_note}Check the result in Canon DPP before use.\nCamera compatibility remains unverified.',
                       '{path}\n\n{bytes:,} bytes\nSHA256 {sha}…\nモデル平均RGB誤差：{mae:.1f}/255（推定）\n{xmp_note}使用前にCanon DPPで結果を確認してください。\nカメラ実機との互換性は未検証です。',
                       '{path}\n\n{bytes:,} bytes\nSHA256 {sha}…\n模型平均 RGB 误差：{mae:.1f}/255（估算）\n{xmp_note}使用前请在 Canon DPP 中检查结果。\n尚未验证相机兼容性。'),
    'pf3_failed': ('PF3 생성 실패', 'PF3 export failed', 'PF3生成に失敗', 'PF3 导出失败'),
    'pf3_failure_hint': ('{error}\n\n캐논 Picture Style Editor를 설치했는지, DLL 버전과 Python/EXE의 비트 수가 일치하는지 확인하세요.',
                         '{error}\n\nCheck that Canon Picture Style Editor is installed and the DLL bitness matches Python/the EXE.',
                         '{error}\n\nCanon Picture Style Editorがインストールされているか、DLLとPython/EXEのビット数が一致するか確認してください。',
                         '{error}\n\n请确认已安装 Canon Picture Style Editor，且 DLL 与 Python/EXE 的位数一致。'),
    'xmp_warning_scene': ('RAW의 장면별 보정, 기본 카메라 프로파일, 화이트 밸런스, 로컬 마스크는 PF3로 옮길 수 없습니다.',
                          'Scene-aware RAW adjustments, base camera profiles, white balance and local masks cannot be carried into PF3.',
                          'RAWのシーン依存補正・基本カメラプロファイル・ホワイトバランス・ローカルマスクはPF3に移せません。',
                          'RAW 场景相关调整、基础相机配置文件、白平衡和局部蒙版无法转换为 PF3。'),
    'xmp_export_warning_import': ('Lightroom/Camera Raw에서의 실제 가져오기는 별도로 검증해야 합니다.',
                                  'Import into Lightroom/Camera Raw has not been independently verified.',
                                  'Lightroom/Camera Rawへの実際の読み込みは別途検証が必要です。',
                                  '尚未独立验证在 Lightroom/Camera Raw 中的实际导入。'),
    'xmp_export_warning_srgb': ('입력 LUT는 표시용 sRGB → sRGB로 가정합니다. Log/색역은 자동 감지하지 않습니다.',
                                'The input LUT is assumed to be display sRGB → sRGB. Log/gamut is not detected automatically.',
                                '入力LUTは表示用sRGB → sRGBと仮定します。Log/色域は自動検出しません。',
                                '假定输入 LUT 为显示 sRGB → sRGB，不会自动检测 Log/色域。'),
    'xmp_export_warning_resample': ('XMP RGBTable은 최대 32³ 노드입니다. 33³/65³ LUT는 재샘플링합니다.',
                                    'XMP RGBTable supports up to 32³ nodes. 33³/65³ LUTs are resampled.',
                                    'XMP RGBTableは最大32³ノードです。33³/65³ LUTはリサンプリングされます。',
                                    'XMP RGBTable 最多支持 32³ 节点。33³/65³ LUT 会被重新采样。'),
    # ComparisonView (preview toolbar, labels and working status)
    'fit': ('화면 맞춤', 'Fit', '画面に合わせる', '适应窗口'),
    'viewer_no_photo': ('사진을 열어 주세요. 휠: 확대/축소 · 드래그: 이동',
                        'Open a photo. Wheel: zoom · Drag: pan', '写真を開いてください。ホイール：ズーム・ドラッグ：移動',
                        '请打开照片。滚轮：缩放 · 拖动：平移'),
    'viewer_original': ('원본', 'Original', '元画像', '原图'),
    'viewer_look': ('LUT 미리보기', 'LUT preview', 'LUTプレビュー', 'LUT 预览'),
    'viewer_busy': ('{width:,} × {height:,} px | {zoom:.1f}% | 처리 중…',
                    '{width:,} × {height:,} px | {zoom:.1f}% | Rendering…',
                    '{width:,} × {height:,} px | {zoom:.1f}% | 処理中…',
                    '{width:,} × {height:,} px | {zoom:.1f}% | 处理中…'),
    'viewer_ready': ('{width:,} × {height:,} px | {zoom:.1f}% | 휠: 확대 · 드래그: 이동',
                     '{width:,} × {height:,} px | {zoom:.1f}% | Wheel: zoom · Drag: pan',
                     '{width:,} × {height:,} px | {zoom:.1f}% | ホイール：ズーム・ドラッグ：移動',
                     '{width:,} × {height:,} px | {zoom:.1f}% | 滚轮：缩放 · 拖动：平移'),
    'viewer_error': ('미리보기 오류: {error}', 'Preview error: {error}', 'プレビューエラー：{error}', '预览错误：{error}'),
}
_INDEX = {'ko': 0, 'en': 1, 'ja': 2, 'zh-CN': 3}


def tr(language: str, key: str, **kwargs) -> str:
    """Return a localized string, keeping placeholders explicit and testable."""
    template = _MESSAGES[key][_INDEX.get(language, 0)]
    return template.format(**kwargs)


def config_file() -> Path:
    override = os.environ.get('PICTURE_BRIDGE_CONFIG_DIR')
    if override:
        root = Path(override)
    elif os.name == 'nt':
        root = Path(os.environ.get('APPDATA', str(Path.home()))) / 'PictureBridge'
    else:
        root = Path.home() / '.config' / 'picture-bridge'
    return root / 'settings.json'


def load_language() -> str:
    try:
        language = json.loads(config_file().read_text(encoding='utf-8')).get('language')
        return language if language in LANGUAGES else DEFAULT_LANGUAGE
    except (OSError, ValueError, TypeError, AttributeError):
        return DEFAULT_LANGUAGE


def save_language(language: str) -> bool:
    if language not in LANGUAGES:
        raise ValueError(f'Unsupported language: {language}')
    try:
        path = config_file()
        path.parent.mkdir(parents=True, exist_ok=True)
        temp = path.with_suffix('.tmp')
        temp.write_text(json.dumps({'language': language}, ensure_ascii=False), encoding='utf-8')
        temp.replace(path)
        return True
    except OSError:
        return False


def validate_catalog() -> None:
    """Detect untranslated keys or mismatched substitutions in CI."""
    from string import Formatter
    for key, values in _MESSAGES.items():
        if len(values) != len(_INDEX):
            raise AssertionError(f'{key}: expected four languages')
        slots = [set(part for _, part, _, _ in Formatter().parse(value) if part) for value in values]
        if any(s != slots[0] for s in slots):
            raise AssertionError(f'{key}: placeholder mismatch {slots}')
        if any(not value.strip() for value in values):
            raise AssertionError(f'{key}: blank translation')
