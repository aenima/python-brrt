from typing import TYPE_CHECKING, Tuple
from .base import PrintFormatter

if TYPE_CHECKING:
    from collections.abc import Iterator
    from brrt.dialects.base import PrinterDialect


class AlignedFormatter(PrintFormatter):

    def __init__(
        self,
        dialect: "PrinterDialect",
        align: str = "L",
        justify: bool = False,
        left_margin: int = 0,
        right_margin: int = 0,
    ):
        super().__init__(dialect)
        self.align = align
        self.justify = justify
        self.left_margin = left_margin
        self.right_margin = right_margin

    def format(self, text: str) -> "Iterator[bytes]":
        effective_line_length = (
            self.dialect.LINE_LENGTH - self.left_margin - self.right_margin
        )
        while text:
            this_line, text = self.split_first_line(text, effective_line_length)

            if self.justify:
                this_line = self.justify_line(this_line, effective_line_length)

            if self.align == "C":
                padding = " " * ((effective_line_length - len(this_line)) // 2)
            elif self.align == "R":
                padding = " " + (effective_line_length - len(this_line))
            else:
                padding = ""

            padding += " " * self.left_margin
            yield self.dialect.enc(padding + this_line + self.dialect.crlf)

    @staticmethod
    def split_first_line(
        text: str,
        line_length: int,
    ) -> Tuple[str, str]:
        """Splits off whole words up to line_length characters + remaining string"""
        word_split = text.split(" ")
        current_line = ""

        while word_split and (word := word_split.pop(0)):
            if len(current_line + word) + 1 > line_length:
                word_split.insert(0, word)
                break
            current_line += f" {word}"
        return current_line, " ".join(word_split)

    @staticmethod
    def justify_line(text: str, line_length: int) -> str:
        word_list = text.split()
        if len(word_list) == 1:
            return word_list[0].ljust(line_length)

        total_spaces = line_length - sum(len(word) for word in word_list)
        gaps = len(word_list) - 1
        space, extra = divmod(total_spaces, gaps)

        return (
            "".join(
                word + " " * (space + (i < extra))
                for i, word in enumerate(word_list[:-1])
            )
            + word_list[-1]
        )
