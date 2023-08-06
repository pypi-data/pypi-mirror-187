from typing import Union

from dominate.tags import html_tag, tbody

from iolanta.facet import Facet
from mkdocs_iolanta_tables.facets.queries import select_instances


class BodyRows(Facet):
    """Build table body when it is specified by table:rows property."""

    def html(self) -> Union[str, html_tag]:
        """Render as HTML."""
        instances = select_instances(
            iri=self.iri,
            iolanta=self.iolanta,
        )

        rendered_rows = [
            self.render(
                instance,
                environments=[self.iri],
            )
            for instance in instances
        ]

        return tbody(*rendered_rows)
