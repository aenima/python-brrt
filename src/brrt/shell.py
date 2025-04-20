from re import Match, compile
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from brrt.printer import DotMatrixPrinter

HEX_ESCAPE_REGEX = compile(r"\\x([0-9a-fA-F]+)")


class PrinterShell:
    def __init__(self, printer: "DotMatrixPrinter"):
        self._printer = printer
        d = printer.dialect
        self._greeting = f"Printer Shell {d.manufacturer} {d.model_name} @ {printer._fp.name}\n"
        self._prompt = f"{printer._fp.name} -> "

    def prompt_loop(self):
        print("-" * len(self._greeting))
        print(self._greeting)
        try:
            while True:
                self.prompt()
        except (SystemExit, EOFError):
            self._cprint("--> KTHXBYE!")

    def prompt(self):
        try:
            user_input = input(self._prompt)
            self._process_input(user_input)
        except KeyboardInterrupt:
            pass

    def _process_input(self, user_input: str):
        user_input = user_input.rstrip()

        if user_input[0] == "/":
            # This is a command
            user_input = user_input[1:]
            if remainder := self._match_cmd(user_input, "list "):
                self._command_list(remainder)
            elif remainder := self._match_cmd(user_input, "set "):
                self._command_set(remainder)
            elif remainder := self._match_cmd(user_input, "unset "):
                self._command_unset(remainder)
            elif remainder := self._match_cmd(user_input, "reload"):
                try:
                    self._printer.dialect.reload()
                except Exception as err:
                    self._cprint(f"Error while reloading printer dialect: {err}")
                else:
                    self._cprint("Reloaded printer dialect!")
            elif remainder := self._match_cmd(user_input, "demo"):
                self._printer.demo()
            else:
                self._cprint("Unsupported command!")
        else:
            # This is raw input to the printer
            # Lets do some parsing for escapes, and then send it on
            if user_input.startswith(r"\/"):
                # We use '/' as start for a command. To start a printed line
                # with '/', escape the '/'.
                user_input = "/" + user_input[2:]

            user_input = user_input.replace(r"\e", "\x1b")
            user_input = user_input.replace(r"\r", "\r")
            user_input = user_input.replace(r"\n", "\n")
            user_input = user_input.replace(r"\t", "\t")
            user_input = HEX_ESCAPE_REGEX.sub(self._sub_escape, user_input)

            user_input += "\r\n"
            self._pprint(user_input)

    def _match_cmd(self, user_input: str, cmd: str) -> str | None | bool:
        if user_input[: len(cmd)] == cmd:
            return user_input[len(cmd) :].strip() or True
        return None

    def _command_list(self, remainder: str):
        for item_name, function in [
            ("font", self._printer.dialect.list_fonts),
            ("style", self._printer.dialect.list_styles),
        ]:
            if self._match_cmd(remainder, item_name):
                items = function()
                self._cprint(f"Supported {item_name.capitalize()}s: {','.join(items)}")
                break
        else:
            self._cprint(f"Unknown item '{remainder}'!")

    def _command_set(self, remainder: str):
        for item_name, set_function, list_function in [
            ("font", self._printer.dialect.set_font, self._printer.dialect.list_fonts),
            ("style", self._printer.dialect.set_style, self._printer.dialect.list_styles),
            ("pitch", self._printer.dialect.set_pitch, self._printer.dialect.list_pitches),
        ]:
            if item := self._match_cmd(remainder, item_name):

                # Ensure that matching is done case-insensitive and that
                # unique prefixes are enough to select the proper item.
                available_items = list_function()
                candidates = [av_item for av_item in available_items if av_item.lower().startswith(item.lower())]
                if len(candidates) == 1:
                    self._pprint(set_function(candidates[0]))
                    self._cprint(f"Set {item_name} {candidates[0]}")
                else:
                    self._cprint(f"{item_name.capitalize()} not found!")
                break
        else:
            self._cprint(f"Cannot set '{remainder}'")

    def _command_unset(self, remainder: str):
        if remainder[:5] == "style":
            style = remainder[5:].strip()
            try:
                self._pprint(self._printer.dialect.unset_style(style))
            except KeyError:
                self._cprint("Style not found!")
        else:
            self._cprint(f"Cannot unset '{remainder}'")

    @staticmethod
    def _sub_escape(match: Match) -> str:
        n = int(match.group(1), 16)
        return chr(n)

    def _cprint(self, text: str):
        print("\n".join(f"  {line}" for line in text.split("\n")))

    def _pprint(self, text: str):
        self._printer.send(self._printer.dialect.enc(text))
