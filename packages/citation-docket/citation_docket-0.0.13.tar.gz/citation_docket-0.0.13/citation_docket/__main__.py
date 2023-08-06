from collections.abc import Iterator

from .regexes import (
    CitationAdministrativeCase,
    CitationAdministrativeMatter,
    CitationBarMatter,
    CitationGeneralRegister,
)


def extract_dockets(
    raw: str,
) -> Iterator[
    CitationAdministrativeCase
    | CitationAdministrativeMatter
    | CitationBarMatter
    | CitationGeneralRegister
]:
    """Extract from `raw` text all raw citations which
    should include their Docket and Report component parts.

    Examples:
        >>> text = "Bagong Alyansang Makabayan v. Zamora, G.R. Nos. 138570, 138572, 138587, 138680, 138698, October 10, 2000, 342 SCRA 449"
        >>> docket = next(extract_dockets(text))
        CitationGeneralRegister(publisher='SCRA', volume='342', page='449', volpubpage='342 SCRA 449', report_date=None, context='G.R. Nos. 138570, 138572, 138587, 138680, 138698', short_category='GR', category='General Register', ids='138570, 138572, 138587, 138680, 138698', docket_date=datetime.date(2000, 10, 10))
        >>> str(docket)
        'GR 138570, Oct. 10, 2000'

    Args:
        raw (str): Text to look for dockets and reports

    Yields:
        Iterator[ CitationAdministrativeCase | CitationAdministrativeMatter | CitationBarMatter | CitationGeneralRegister ]: _description_
    """  # noqa: E501
    for citation in [
        CitationAdministrativeCase,
        CitationAdministrativeMatter,
        CitationBarMatter,
        CitationGeneralRegister,
    ]:
        yield from citation.search(raw)
