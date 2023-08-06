import abc
from collections.abc import Iterator
from typing import Self

from citation_report import Report

from .docket_model import Docket


class DocketReportCitation(Docket, Report, abc.ABC):
    """Note `Report` is defined in a separate library `citation-report`."""

    ...

    @classmethod
    @abc.abstractmethod
    def search(cls, raw: str) -> Iterator[Self]:
        raise NotImplementedError(
            "Each docket citation must have a search method that produces an"
            " Iterator of the class instance."
        )
