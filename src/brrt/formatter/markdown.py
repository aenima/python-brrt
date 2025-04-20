from typing import TYPE_CHECKING

from brrt.formatter.aligner import AlignedFormatter


if TYPE_CHECKING:
    from collections.abc import Iterator

    from brrt.dialects.base import PrinterDialect


class MarkdownFormatter(AlignedFormatter):
    def format(self, text: str) -> "Iterator[bytes]":
        pars0r = _StateMachineTokeniz0r(self.dialect)

        for current_line in super().format(text):
            yield pars0r.parse(current_line)


class _StateMachineTokeniz0r:
    BOLD_TOKEN = "*"
    BOLD_STYLE = "bold"

    ITALIC_TOKEN = "-"
    ITALIC_STYLE = "italic"

    UNDERSCORE_TOKEN = "_"
    UNDERSCORE_STYLE = "underscore"

    LEFT_ALIGN_TOKEN = "\\"
    LEFT_ALIGN_STYLE = "L"

    RIGHT_ALIGN_TOKEN = "/"
    RIGHT_ALIGN_STYLE = "R"

    CENTER_ALIGN_TOKEN = "|"
    CENTER_ALIGN_STYLE = "C"

    JUST_ALIGN_TOKEN = "§"

    def __init__(self, dialect: "PrinterDialect"):
        self._state = set()
        self._dialect = dialect

    def parse(self, next_line: str) -> str:
        output_line = ""
        while next_line and (token := next_line.pop(0)):
            match token:
                case self.BOLD_TOKEN:
                    output_line += self._modify_style(self.BOLD_TOKEN, self.BOLD_STYLE)
                case self.ITALIC_TOKEN:
                    output_line += self._modify_style(self.BOLD_TOKEN, self.BOLD_STYLE)
                case self.UNDERSCORE_TOKEN:
                    output_line += self._modify_style(
                        self.UNDERSCORE_TOKEN, self.UNDERSCORE_STYLE
                    )
                case _:
                    output_line += token
        return output_line

    def _modify_style(self, token: str, style: str) -> str:
        if token in self._state:
            self.state.remove(token)
            return self.dialect.unset_style(style)
        else:
            self.state.add(token)
            return self.dialect.set_style(style)
