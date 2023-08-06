import operator
from typing import Iterable

import funcy
from rdflib import URIRef

from iolanta.iolanta import Iolanta
from iolanta.models import NotLiteralNode


def select_instances(
    iri: NotLiteralNode,
    iolanta: Iolanta,
) -> Iterable[URIRef]:
    """Select instances, or rows, for the table."""
    rows = list(
        funcy.pluck(
            'instance',
            iolanta.query(
                '''
                SELECT ?instance WHERE {
                    $iri rdf:rest*/rdf:first ?instance .
                }
                ''',
                iri=iri,
            ),
        ),
    )

    return rows or list(
        map(
            operator.itemgetter('instance'),
            iolanta.query(
                query_text='''
                SELECT ?instance WHERE {
                    $iri table:class ?class .
                    ?instance a ?class .
                }
                ''',
                iri=iri,
            ),
        ),
    )
