"""Application identity, shared by GUI, CLI and Adobe profile exporter."""

APP_NAME = "Picture Bridge"
APP_VERSION = "1.0"
APP_AUTHOR = "LimeT"
XMP_GROUP = APP_NAME


def display_name() -> str:
    return f"{APP_NAME} v{APP_VERSION}"
