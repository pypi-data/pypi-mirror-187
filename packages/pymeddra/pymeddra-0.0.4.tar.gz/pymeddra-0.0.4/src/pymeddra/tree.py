from __future__ import annotations
from pydantic import BaseModel, validator
from typing import Union, Optional, Dict, DefaultDict, List
from enum import Enum
from collections import defaultdict


class Level(Enum):
    ROOT = 0
    SOC = 1
    HLTG = 2
    HLT = 3
    LLT = 4

    def __add__(self, other: int) -> Union[Level, None]:
        if self.ROOT.value <= self.value + other <= self.LLT.value:
            return Level(self.value + other)
        else:
            return None

    def __lt__(self, other: Node) -> bool:
        return self.value < other.value

    def __le__(self, other: Node) -> bool:
        return self.value <= other.value

    def __gt__(self, other: Node) -> bool:
        return self.value > other.value

    def __ge__(self, other: Node) -> bool:
        return self.value >= other.value

    def __sub__(self, other: Node) -> int:
        return self.value - other.value


class Node(BaseModel):
    id: str
    term: str
    level: Level

    parent: Node = None
    children: Dict[str, Node] = {}

    # maps for efficient nested children lookups
    # typically only used for the root node
    id_to_nodes: Optional[DefaultDict[str, List[Node]]] = None
    term_to_nodes: Optional[DefaultDict[str, List[Node]]] = None

    # text normalizer to build lookup tables
    # typically only used for the root node
    normalizer: function = lambda x: x

    def get_parent_at_level(self, target_level: Level) -> Union[Node, None]:
        # check if current node is deeper than target_level
        level_diff = target_level - self.level
        if level_diff > 0:
            return None
        else:
            node = self
            for _ in range(-level_diff):
                node = node.parent
            return node

    def get_children_at_level(self, target_level: Level) -> List[Node]:
        raise NotImplementedError

    def lookup_id(self, id: str) -> Union[List[Node], None]:
        # create lookup tables if they do not exists
        if self.id_to_nodes == None:
            self.set_lookup_tables()
        # lookup

        if id in self.id_to_nodes:
            return self.id_to_nodes[id]
        else:
            return None

    def lookup_term(self, term: str) -> Union[List[Node], None]:
        # create lookup tables if they do not exists
        if self.term_to_nodes == None:
            raise RuntimeError("First set the lookup tables using 'set_lookup_tables'.")
        # lookup
        term = self.normalizer(term)
        if term in self.term_to_nodes:
            return self.term_to_nodes[term]
        else:
            return None

    def set_lookup_tables(self, normalizer: function = lambda x: x) -> None:
        # set normalizer
        self.normalizer = normalizer

        # get a flat list of all nodes
        self.term_to_nodes = defaultdict(list)
        self.id_to_nodes = defaultdict(list)

        # breadth-first traversal
        candidates = [self]
        while len(candidates):
            candidate = candidates.pop(0)
            # track nodes
            self.term_to_nodes[self.normalizer(candidate.term)].append(candidate)
            self.id_to_nodes[candidate.id].append(candidate)
            # add candidate's children to candidate list
            if candidate.children:
                candidates.extend(candidate.children.values())
        return None

    def is_equivalent_node(self, other: Node) -> bool:
        # return true if two nodes are the same, siblings or in a parent-child relation
        return (
            (self == other)
            or (self.parent == other)
            or (self == other.parent)
            or (self.parent == other.parent)
        )

    def terms_equivalent(self, term1: str, term2:str) -> bool:
        # lookup both terms
        term1_nodes = self.lookup_term(term1)
        term2_nodes = self.lookup_term(term2)
        # compare all nodes
        for node1 in term1_nodes:
            for node2 in term2_nodes:
                if node1.is_equivalent_node(node2):
                    return True
        return False

    def __key(self):
        return (self.id, self.term, self.parent, len(self.children))

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other: Node) -> bool:
        # undeep equals operator, does not check children
        return self.__key() == other.__key()

    def __str__(self) -> str:
        return f"Node(id={self.id}, term={self.term}, level={self.level}, parent={self.parent.term if self.parent else None}, #children={len(self.children)})"

    def __repr__(self) -> str:
        return self.__str__()
