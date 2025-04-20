from .aligner import AlignedFormatter
from .markdown import MarkdownFormatter
from .base import PrintFormatter

FORMATTERS = {"Aligned": AlignedFormatter, "Markdown": MarkdownFormatter}
