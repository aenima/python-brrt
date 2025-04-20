#! /usr/bin/env python3

from argparse import ArgumentParser
from types import TracebackType
from typing import BinaryIO, Dict, Type

from brrt.dialects import PrinterDialect
from brrt.formatter import FORMATTERS, PrintFormatter
from brrt.shell import PrinterShell

DEMO_SENTENCE = "The five boxing wizards jump quickly"
DEMO_ADDITIONAL = "0123456789"
DEMO_STRING = f"{DEMO_SENTENCE.upper()} {DEMO_ADDITIONAL} {DEMO_SENTENCE.lower()}"


class DotMatrixPrinter:
    @classmethod
    def script(cls):
        parser = ArgumentParser(description="Printer Shell for Dot Matrix Printers")
        parser.add_argument("DEVICE", help="Device path to the printer")
        parser.add_argument("dialect", help="Printer dialect to use")
        parser.add_argument("--formatter", default="Aligned", help="Name of the formatter to configure")
        args = parser.parse_args()
        printer = cls.printer_factory(args.DEVICE, args.dialect, args.formatter)
        printer.shell()

    @classmethod
    def printer_factory(
        cls,
        device_path: str,
        printer_dialect: str,
        formatter: str = "Aligned",
        formatter_options: Dict[str, str] | None = None,
    ):
        formatter_options = formatter_options or {}
        dialect = PrinterDialect.dialect_factory(printer_dialect)
        formatter = FORMATTERS[formatter](dialect, **formatter_options)
        return cls(device_path, dialect, formatter)

    def __init__(self, device_path: str, dialect: PrinterDialect, formatter: PrintFormatter):
        self._device_path = device_path
        self.dialect = dialect
        self.formatter = formatter
        self.formatter.dialect = self.dialect
        self._fp: BinaryIO | None = None

    def open(self):
        if not self._fp or self._fp.closed:
            self._fp = open(self._device_path, "wb")

    def close(self):
        if self._fp:
            self._fp.close()

    def shell(self):
        with self:
            shell = PrinterShell(self)
            shell.prompt_loop()

    def demo(self):
        fonts = self.dialect.list_fonts()
        pitches = self.dialect.list_pitches()

        for font in fonts:
            self.send(self.dialect.enc(self.dialect.set_font(font)))
            for pitch in pitches:
                self.send(self.dialect.enc(self.dialect.set_pitch(pitch)))
                self.send(self.dialect.enc(f"{font} {pitch}" + self.dialect.crlf))
                self.send(self.dialect.enc(DEMO_STRING + self.dialect.crlf))

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type: Type[Exception], exc_val: Exception, exc_tb: TracebackType) -> bool:
        self.close()
        return False

    def _check(self):
        if not self._fp or self._fp.closed:
            raise IOError("Printer not opened!")

    def flush(self):
        self._fp.flush()

    def send(self, bytes_text: bytes, flush: bool = True):
        self._check()
        self._fp.write(bytes_text)
        if flush:
            self.flush()

    def print(self, text: str):
        for line in self.formatter.format(text):
            self.send(line)


if __name__ == "__main__":
    DotMatrixPrinter.script()
