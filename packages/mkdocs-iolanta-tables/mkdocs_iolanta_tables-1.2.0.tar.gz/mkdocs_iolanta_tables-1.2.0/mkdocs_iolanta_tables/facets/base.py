from abc import ABC
from dataclasses import dataclass
from pathlib import Path
from typing import List

import funcy

from iolanta.facet import Facet
from iolanta.models import NotLiteralNode


@dataclass
class IolantaTablesFacet(ABC, Facet):
    """Base for mkdocs-iolanta-tables facets."""

    stored_queries_path: Path = Path(__file__).parent / 'sparql'

    def list_columns(
        self,
        column_list: NotLiteralNode,
    ) -> List[NotLiteralNode]:
        """List of column IRIs for a table."""
        rows = self.stored_query(
            'columns.sparql',
            column_list=column_list,
        )

        return list(
            funcy.pluck(
                'column',
                rows,
            ),
        )
