import re
from re import Pattern

from citation_date import report_date

from .publisher import OFFG, PHIL, SCRA

PUBLISHERS_REGEX = rf"""
    (?P<publisher>
        {SCRA.regex_exp}| # contains SCRA_PUB group name
        {PHIL.regex_exp}| # contains PHIL_PUB group name
        {OFFG.regex_exp} # contains OG_PUB group name
    )
"""
"""A partial regex string containing the Publisher options available."""


volume = r"""
    \b
    (?P<volume>
        [12]? # makes possible from 1000 to 2999
        \d{1,3}
        (
            \-A| # See Central Bank v. CA, 159-A Phil. 21, 34 (1975);
            a
        )?
    )
    \b
"""

page = r"""
    \b
    (?P<page>
        [12345]? # makes possible from 1000 to 5999
        \d{1,3}  # 49 Off. Gazette 4857
    )
    \b
"""

volpubpage = rf"""
    (?P<volpubpage>
        {volume}
        \s+
        {PUBLISHERS_REGEX}
        \s+
        {page}
    )
"""

filler = r"""
    (?P<filler>
        [\d\-\.]{1,10}
    )
"""

extra = rf"""
    (?:
        (?:
            [\,\s,\-]*
            {filler}
        )?
        [\,\s]*
        {report_date}
    )?
"""

REPORT_REGEX = rf"{volpubpage}{extra}"

REPORT_PATTERN: Pattern = re.compile(REPORT_REGEX, re.X | re.I)
