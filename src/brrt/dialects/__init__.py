from pathlib import Path
from yaml import safe_load
from typing import List


_CURRENT_DIR = Path(__file__).parent
DEFAULT_ENCODING = "ascii"
DEFAULT_CR = "\n"
DEFAULT_LF = "\r"
ESC = "\x1b"


class PrinterDialect:

    @staticmethod
    def list_dialects() -> List[str]:
        return [str(dialect_file)[:-4] for dialect_file in _CURRENT_DIR.glob("*.yml")]

    @classmethod
    def dialect_factory(cls, dialect_name):
        file_path = _CURRENT_DIR / f"{dialect_name}.yml"
        return cls(str(file_path))

    def __init__(self, dialect_file: str):
        self._dialect_file = dialect_file
        self._load()

    def _load(self):
        with open(self._dialect_file) as f:
            dialect = safe_load(f)

        self.model_name = dialect["model_name"]
        self.manufacturer = dialect["manufacturer"]
        self.line_length = dialect["line_length"]
        self.encoding = dialect.get("encoding", DEFAULT_ENCODING)

        self.commands = dialect["commands"]

        self.fonts = dialect["fonts"]
        self.styles = dialect["styles"]
        self.pitches = dialect["pitch"]

        self.lf = dialect.get("lf", DEFAULT_LF)
        self.cr = dialect.get("cr", DEFAULT_CR)
        self.crlf = f"{self.cr}{self.lf}"

    def __getattr__(self, name):
        if name in self.commands:
            return self.commands[name]
        raise AttributeError(f"The command {name} is not available for this printer.")

    def reload(self):
        self._load()

    def enc(self, text: str) -> bytes:
        return text.encode(self.encoding)

    def list_fonts(self) -> List[str]:
        return list(self.fonts.keys())

    def set_font(self, font: str) -> str:
        return self.fonts[font]

    def list_styles(self) -> List[str]:
        return list(self.styles.keys())

    def set_style(self, style: str) -> str:
        return self.styles[style][0]

    def unset_style(self, style: str) -> str:
        return self.styles[style][1]

    def list_pitches(self) -> List[str]:
        return list(self.pitches.keys())

    def set_pitch(self, pitch: str) -> str:
        return self.pitches[pitch]
