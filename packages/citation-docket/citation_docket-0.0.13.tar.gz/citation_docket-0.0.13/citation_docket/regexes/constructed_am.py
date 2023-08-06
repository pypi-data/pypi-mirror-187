from citation_report import Report

from .models import Constructor, Docket, Num

separator = r"[,\.\s-]*"
digit = r"\d{3}[\d-]*"  # e.g. 323-23, 343-34
acronyms = r"""
    \s?
    (
        A|
        B|
        P|
        R|
        P|
        J|
        OCA|
        O\.C\.A\.|
        SDC|
        CTA|
        RTC|
        CFI|
        RTJ|
        MTJ|
        MJ|
        CJ|
        CTJ|
        CAR|
        CCC|
        CFI|
        JDRC|
        OMB|
        TEL|
        METC|
        MCTC|
        MTCC|
        MTC|
        HOJ|
        RET(?:\.)?|
        SCC?|
        SC(?:\-PHILJA)?|
        CA(?:\-J)?|
        SB(?:\-J)?
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


ipi = r"""
    (
        (IPI)|(I\.P\.I\.)
    )
"""

am_key = rf"""
    (
        (
            a
            {separator}
            m
            {separator}
        )|
        (
            \b
            adm(in)?(istrative)?
            {separator}
            (?:
                \b
                (
                    Matter|
                    Mat\. # ADM. MAT. NO. P-97-1241
                )
                \s* # optional space
            )?
        )
    )
"""

am_oca_ipi_num = rf"""
    (
        {am_key}?
        OCA
        \s*
        (
            IPI|
            I\.P\.I\.
        )
        \s*
        {Num.AM.allowed}
    )
"""

am_num = rf"""
    (
        {am_key}
        {Num.AM.allowed}
    )
"""

required = rf"""
    (?P<am_init>
        {am_oca_ipi_num}| # AM OCA IPI No. / OCA IPI No.
        {am_num}| # AM No.
        {am_key} # AM
    )
    (?P<am_middle>
        (
            ({letter})|
            ({digit})
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
    (?P<am_init_optional>
        {am_oca_ipi_num}|
        {am_num}
    )?
    (?P<am_middle_optional>
        {letter}|
        {digit}
    )?
    (?:
        (
            [\,\s,\-\&]|
            and
        )*
    )?
"""

am_phrases = rf"""
    (?P<am_phrase>
        ({required})
        ({optional}){{1,3}}
    )
"""


constructed_am = Constructor(
    label="Administrative Matter",
    short_category="AM",
    group_name="am_phrase",
    init_name="am_init",
    docket_regex=am_phrases,
    key_regex=am_key,
    num_regex=Num.AM.allowed,
)


class CitationAdministrativeMatter(Docket, Report):
    """Get all dockets matching the `AM` docket pattern, inclusive of their optional Report object.

    Examples:
        >>> text = "A.C. No. P-88-198, February 25, 1992, 206 SCRA 491."
        >>> next(CitationAdministrativeCase.search(text))
        'CitationAdministrativeCase(publisher='SCRA', volume='206', page='491', volpubpage='206 SCRA 491', report_date=None, context='A.C. No. P-88-198', short_category='AC', category='Administrative Case', ids='P-88-198', docket_date=datetime.date(1992, 2, 25))'

    Args:
        text (str): Text to look for citation objects

    Yields:
        Iterator[Self]: Combination of Docket and Report pydantic model.
    """  # noqa E501

    ...

    @classmethod
    def search(cls, text: str):
        for result in constructed_am.detect(text):
            yield cls(**result)
