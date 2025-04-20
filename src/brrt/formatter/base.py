from abc import ABC, abstractmethod

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterator

    from brrt.dialects.base import PrinterDialect


class PrintFormatter(ABC):
    def __init__(self, dialect: "PrinterDialect | None" = None):
        self.dialect: "PrinterDialect" = dialect

    @abstractmethod
    def format(self, text: str) -> "Iterator[bytes]":
        pass
