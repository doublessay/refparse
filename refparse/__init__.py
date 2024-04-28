__version__ = "0.4.0"

from typing import Literal, Optional
from .wos import ParseWos
from .scopus import ParseScopus
from .cssci import ParseCssci


def parse(ref: Optional[str], source: Literal["wos", "scopus", "cssci"]) -> Optional[dict[str, Optional[str]]]:
    if ref:
        if source == "wos":
            return ParseWos(ref).parse()
        elif source == "scopus":
            return ParseScopus(ref).parse()
        elif source == "cssci":
            return ParseCssci(ref).parse()
        else:
            raise ValueError("Please input valid <source>.")
    else:
        return None
