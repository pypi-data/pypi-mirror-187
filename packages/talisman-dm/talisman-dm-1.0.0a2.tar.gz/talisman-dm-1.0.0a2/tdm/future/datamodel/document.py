import uuid
from abc import ABCMeta
from collections import defaultdict
from copy import deepcopy
from typing import Callable, Dict, FrozenSet, Iterable, Optional, Type, TypeVar

from frozendict import frozendict

from tdm.abstract.datamodel.document import DocumentMetadata
from tdm.future.abstract.datamodel import AbstractDirective, AbstractFact, AbstractNode, AbstractNodeLink


# FIXME: This class should be rewritten
# TODO: Maybe interface is not needed here
class TalismanDocument(metaclass=ABCMeta):
    __slots__ = ('_id', '_root', '_content', '_links', '_facts', '_directives', '_metadata')

    def __init__(
            self,
            content: Iterable[AbstractNode],
            root: AbstractNode,
            links: Iterable[AbstractNodeLink],
            facts: Iterable[AbstractFact],
            directives: Iterable[AbstractDirective],
            metadata: Optional[DocumentMetadata],  # should be removed in future
            *, id_: str):
        self._id = id_ or self.generate_id()
        self._content = frozendict({node.id: node for node in content})
        self._root = root
        self._links = _group(links, lambda f: type(f))
        self._facts = _group(facts, lambda f: type(f))
        # TODO: in future we should remove directives and implement it as facts (concept fact with filter?)
        self._directives = _group(directives, lambda f: type(f))

        self._metadata = deepcopy(metadata)

    @property
    def id(self) -> str:
        return self._id

    @property
    def content(self) -> Dict[str, AbstractNode]:
        return self._content

    @property
    def root(self) -> AbstractNode:
        return self._root

    @property
    def links(self) -> Dict[Type[AbstractNodeLink], Iterable[AbstractNodeLink]]:
        return self._links

    @property
    def facts(self) -> Dict[Type[AbstractFact], Iterable[AbstractFact]]:
        return self._facts

    @property
    def directives(self) -> Dict[Type[AbstractDirective], Iterable[AbstractDirective]]:
        return self._directives

    def __hash__(self):
        return hash((self._id, self._links, self._facts))

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, TalismanDocument):
            return NotImplemented
        return self._id == o._id and self._content == o._content and self._root == o._root and \
            self._links == o._links and self._facts == o._facts and self._directives == o._directives and \
            self._metadata == o._metadata

    @staticmethod
    def generate_id():
        return str(uuid.uuid4())


_E = TypeVar('_E')
_K = TypeVar('_K')


def _group(elems: Iterable[_E], key: Callable[[_E], _K]) -> Dict[_K, FrozenSet[_E]]:
    result = defaultdict(list)
    for elem in elems:
        result[key(elem)].append(elem)
    return frozendict({k: frozenset(v) for k, v in result.items()})
