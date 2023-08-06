from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import List, Optional, Union

from dominate.tags import html_tag
from rdflib.term import BNode, Node, URIRef

from iolanta import renderer
from iolanta.iolanta import Iolanta
from iolanta.models import NotLiteralNode
from ldflex import LDFlex
from ldflex.ldflex import QueryResult, SPARQLQueryArgument


@dataclass
class Facet:
    """Base facet class."""

    iri: NotLiteralNode
    iolanta: Iolanta
    environment: Optional[URIRef] = None
    stored_queries_path: Path = Path(__file__).parent / 'sparql'

    @property
    def ldflex(self) -> LDFlex:
        """Extract LDFLex instance."""
        return self.iolanta.ldflex

    @cached_property
    def uriref(self) -> NotLiteralNode:
        """Format as URIRef."""
        if isinstance(self.iri, BNode):
            return self.iri

        return URIRef(self.iri)

    def query(
        self,
        query_text: str,
        **kwargs: SPARQLQueryArgument,
    ) -> QueryResult:
        """SPARQL query."""
        return self.ldflex.query(
            query_text=query_text,
            **kwargs,
        )

    def render(self, iri: NotLiteralNode, environments: List[NotLiteralNode]):
        """Shortcut to render something via iolanta."""
        return renderer.render(
            node=iri,
            iolanta=self.iolanta,
            environments=environments,
        )

    def stored_query(self, file_name: str, **kwargs: SPARQLQueryArgument):
        """Execute a stored SPARQL query."""
        query_text = (self.stored_queries_path / file_name).read_text()
        return self.query(
            query_text=query_text,
            **kwargs,
        )

    def html(self) -> Union[str, html_tag]:
        """Render the facet."""
        raise NotImplementedError()

    @property
    def language(self):
        # return self.iolanta.language
        return 'en'

    def __str__(self):
        """Render."""
        return str(self.html())
