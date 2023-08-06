from citation_report import Report

from .models import Constructor, Docket, Num

separator = r"[,\.\s-]*"
l_digits = r"\bL\-\d+"
digits_alone = r"\d+"

acronyms = r"""
    \s?
    (
        SBC # B.M. SBC-591, December 1, 1977
    )
    \s?
"""
letter = rf"""
    (
        \b
        {acronyms}
    )?
    [\d-]{{3,}} #  at least two digits and a dash
    ( # don't add \b  to capture "-Ret.""
        {acronyms}
    )?
"""

bm_key = rf"""
    (
        (
            b
            {separator}
            m
            {separator}
        )|
        (
            \b
            bar
            \s+
            matter
            \s*
        )
    )
"""

bm_num = rf"""
    (
        {bm_key}
        {Num.BM.allowed}
    )
"""

required = rf"""
    (?P<bm_init>
        {bm_num}
    )
    (?P<bm_middle>
        (
            ({letter})|
            ({l_digits})|
            ({digits_alone})
        )
    )
    (?:
        (
            [\,\s,\-\&]|
            and
        )*
    )?
"""

optional = rf"""
    (?P<bm_init_optional>
        {bm_num}
    )?
    (?P<bm_middle_optional>
        ({letter})|
        ({l_digits})|
        ({digits_alone})
    )?
    (?:
        (
            [\,\s,\-\&]|
            and
        )*
    )?
"""

bm_phrases = rf"""
    (?P<bm_phrase>
        ({required})
        ({optional}){{1,3}}
    )
"""


constructed_bm = Constructor(
    label="Bar Matter",
    short_category="BM",
    group_name="bm_phrase",
    init_name="bm_init",
    docket_regex=bm_phrases,
    key_regex=bm_key,
    num_regex=Num.BM.allowed,
)


class CitationBarMatter(Docket, Report):
    ...

    @classmethod
    def search(cls, text: str):
        for result in constructed_bm.detect(text):
            yield cls(**result)
