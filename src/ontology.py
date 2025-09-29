"""
Ontology and reasoning implemented in Python.

Requirements satisfied:
- 20+ classes
- 3+ relations: is_a, part_of, has_property (+ instance_of)
- 4 levels of hierarchy under one relation (entity -> ... -> dog)
- 2+ instances for every practical (leaf-like) class
- Query engine to answer connectivity like: is "собака" connected to "шерсть"?

Clean, dependency-free, Python 3 standard library only.
"""

from __future__ import annotations

from collections import deque, defaultdict
from typing import Dict, Iterable, List, Set, Tuple


# -------------------------------
# Core data: classes and relations
# -------------------------------

# Classes (>= 20)
CLASSES: Set[str] = {
    "entity",
    "physical_object",
    "organism",
    "animal",
    "plant",
    "vertebrate",
    "invertebrate",
    "mammal",
    "bird",
    "fish",
    "reptile",
    "amphibian",
    "arthropod",
    "canine",
    "feline",
    "dog",
    "wolf",
    "fox",
    "cat",
    "lion",
    "sparrow",
    "eagle",
    "salmon",
    "tuna",
    "snake",
    "lizard",
    "spider",
    "beetle",
    "oak",
    "rose",
    "body_part",
    "appendage",
    "tail",
    "leg",
    "wing",
    "head",
    "eye",
    "fur",
    "feather",
    "fin",
    "scale",
    "skin",
}


# is_a edges: child -> parent
IS_A: Set[Tuple[str, str]] = {
    ("physical_object", "entity"),
    ("organism", "physical_object"),
    ("animal", "organism"),
    ("plant", "organism"),
    ("vertebrate", "animal"),
    ("invertebrate", "animal"),
    ("mammal", "vertebrate"),
    ("bird", "vertebrate"),
    ("fish", "vertebrate"),
    ("reptile", "vertebrate"),
    ("amphibian", "vertebrate"),
    ("arthropod", "invertebrate"),
    ("canine", "mammal"),
    ("feline", "mammal"),
    ("dog", "canine"),
    ("wolf", "canine"),
    ("fox", "canine"),
    ("cat", "feline"),
    ("lion", "feline"),
    ("sparrow", "bird"),
    ("eagle", "bird"),
    ("salmon", "fish"),
    ("tuna", "fish"),
    ("snake", "reptile"),
    ("lizard", "reptile"),
    ("spider", "arthropod"),
    ("beetle", "arthropod"),
    ("oak", "plant"),
    ("rose", "plant"),
    ("body_part", "physical_object"),
    ("appendage", "body_part"),
    ("tail", "appendage"),
    ("leg", "appendage"),
    ("wing", "appendage"),
    ("head", "body_part"),
    ("eye", "body_part"),
    ("fur", "body_part"),
    ("feather", "body_part"),
    ("fin", "appendage"),
    ("scale", "body_part"),
    ("skin", "body_part"),
}


# part_of edges: part -> whole
PART_OF: Set[Tuple[str, str]] = {
    ("head", "vertebrate"),
    ("eye", "head"),
    ("leg", "vertebrate"),
    ("skin", "vertebrate"),
    ("tail", "mammal"),
    ("tail", "reptile"),
    ("wing", "bird"),
    ("fin", "fish"),
    ("feather", "bird"),
    ("fur", "mammal"),
    ("scale", "reptile"),
}


# has_property edges: subject -> property
HAS_PROPERTY: Set[Tuple[str, str]] = {
    ("tail", "fur"),      # mammal tails are often furry
    ("wing", "feather"),  # bird wings have feathers
    ("snake", "scale"),   # snakes are covered with scales
    ("fish", "fin"),      # fish have fins
}


# Instances: instance -> class
INSTANCE_OF: Set[Tuple[str, str]] = {
    ("rex", "dog"), ("bim", "dog"),
    ("murka", "cat"), ("simba", "cat"),
    ("akela", "wolf"), ("ghost", "wolf"),
    ("alisa", "fox"), ("todd", "fox"),
    ("mufasa", "lion"), ("nala", "lion"),
    ("chirpy", "sparrow"), ("jack", "sparrow"),
    ("freedom", "eagle"), ("storm", "eagle"),
    ("silver", "salmon"), ("red", "salmon"),
    ("bluefin", "tuna"), ("yellowfin", "tuna"),
    ("kaa", "snake"), ("viper", "snake"),
    ("gecko", "lizard"), ("iguana", "lizard"),
    ("charlotte", "spider"), ("aragog", "spider"),
    ("scarab", "beetle"), ("ladybug", "beetle"),
    ("oak1", "oak"), ("oak2", "oak"),
    ("rose1", "rose"), ("rose2", "rose"),
}


# Practical (leaf-like) classes expected to have 2+ instances
PRACTICAL_CLASSES: Set[str] = {
    "dog", "cat", "wolf", "fox", "lion",
    "sparrow", "eagle", "salmon", "tuna",
    "snake", "lizard", "spider", "beetle",
    "oak", "rose",
}


# Aliases (Ukrainian and English) to canonical atoms
ALIASES: Dict[str, str] = {
    # Animals
    "собака": "dog", "пес": "dog", "dog": "dog",
    "кіт": "cat", "кішка": "cat", "cat": "cat",
    "вовк": "wolf", "wolf": "wolf",
    "лисиця": "fox", "fox": "fox",
    "лев": "lion", "lion": "lion",
    "птах": "bird", "bird": "bird",
    "риба": "fish", "fish": "fish",
    "ссавець": "mammal", "mammal": "mammal",
    "хребетний": "vertebrate", "vertebrate": "vertebrate",
    "безхребетний": "invertebrate", "invertebrate": "invertebrate",
    "плазун": "reptile", "reptile": "reptile",
    "земноводне": "amphibian", "amphibian": "amphibian",
    "горобець": "sparrow", "sparrow": "sparrow",
    "орел": "eagle", "eagle": "eagle",
    "лосось": "salmon", "salmon": "salmon",
    "тунець": "tuna", "tuna": "tuna",
    "змія": "snake", "snake": "snake",
    "ящірка": "lizard", "lizard": "lizard",
    "павук": "spider", "spider": "spider",
    "жук": "beetle", "beetle": "beetle",
    "дуб": "oak", "oak": "oak",
    "троянда": "rose", "rose": "rose",
    # Parts / properties
    "хвіст": "tail", "tail": "tail",
    "шерсть": "fur", "fur": "fur",
    "перо": "feather", "feather": "feather",
    "крило": "wing", "wing": "wing",
    "око": "eye", "eye": "eye",
    "голова": "head", "head": "head",
    "луска": "scale", "scale": "scale",
    "шкіра": "skin", "skin": "skin",
}


# -------------------------------
# Utilities
# -------------------------------

def resolve(name: str) -> str:
    """Resolve Ukrainian/English alias or canonical name to canonical token.

    Raises KeyError if the term is unknown.
    """
    if not isinstance(name, str):
        raise TypeError("name must be a string")
    key = name.strip()
    if key in ALIASES:
        return ALIASES[key]
    # Allow direct canonical token if present in classes or instances
    if key in CLASSES:
        return key
    instance_classes = {inst for inst, _ in INSTANCE_OF} | {cls for _, cls in INSTANCE_OF}
    if key in instance_classes:
        return key
    raise KeyError(f"Unknown term: {name}")


def build_index(edges: Iterable[Tuple[str, str]]) -> Dict[str, Set[str]]:
    index: Dict[str, Set[str]] = defaultdict(set)
    for a, b in edges:
        index[a].add(b)
    return index


IS_A_INDEX = build_index(IS_A)
PART_OF_INDEX = build_index(PART_OF)
HAS_PROPERTY_INDEX = build_index(HAS_PROPERTY)
INSTANCE_OF_INDEX = build_index(INSTANCE_OF)


# -------------------------------
# Reasoning: transitive closures
# -------------------------------

def is_a_transitive(child: str, ancestor: str) -> bool:
    child = resolve(child)
    ancestor = resolve(ancestor)
    if child == ancestor:
        return True
    visited: Set[str] = set()
    queue: deque[str] = deque([child])
    while queue:
        node = queue.popleft()
        if node in visited:
            continue
        visited.add(node)
        for parent in IS_A_INDEX.get(node, ()):  # direct parents
            if parent == ancestor:
                return True
            queue.append(parent)
    return False


def part_of_transitive(part: str, whole: str) -> bool:
    """True if part is part_of whole via transitive part relations and
    inheritance along is_a (both on part and on whole).
    """
    part = resolve(part)
    whole = resolve(whole)

    # Standard BFS over part_of
    visited: Set[str] = set()
    queue: deque[str] = deque([part])
    while queue:
        node = queue.popleft()
        if node in visited:
            continue
        visited.add(node)

        # direct part_of
        for w in PART_OF_INDEX.get(node, ()):  # node part_of w
            if w == whole or is_a_transitive(whole, w):
                return True
            queue.append(w)

        # climb up the part side via is_a and retry
        for super_part in IS_A_INDEX.get(node, ()):  # node is_a super_part
            if (super_part, whole) in PART_OF or any(
                w == whole or is_a_transitive(whole, w) for w in PART_OF_INDEX.get(super_part, ())
            ):
                return True
            queue.append(super_part)

    return False


def has_part(whole: str, part: str) -> bool:
    whole = resolve(whole)
    part = resolve(part)
    return (part, whole) in PART_OF


def has_part_transitive(whole: str, part: str) -> bool:
    whole = resolve(whole)
    part = resolve(part)

    # Inherit has_part down subclass of whole and up subclass of part
    # We perform BFS starting from the whole, following:
    # - direct has_part edges (inverse of part_of)
    # - subclass links down from current whole
    # - subclass links up from parts (via IS_A on the part side)
    visited: Set[str] = set()
    queue: deque[str] = deque([whole])
    while queue:
        node = queue.popleft()
        if node in visited:
            continue
        visited.add(node)

        # direct parts of node
        direct_parts = {p for (p, w) in PART_OF if w == node}
        if part in direct_parts:
            return True
        # if any subclass of the target part is a direct part, accept
        for p in direct_parts:
            if is_a_transitive(part, p):
                return True

        # traverse down the whole's subclasses (inverse is_a)
        subclasses = {c for (c, parent) in IS_A if parent == node}
        queue.extend(subclasses)

        # also traverse through parts to their parts (nested parts)
        for p in direct_parts:
            child_wholes = {w for (pp, w) in PART_OF if pp == p}
            queue.update(child_wholes)

    return False


def neighbors(term: str) -> Iterable[str]:
    """Neighbors for connectivity search. We consider edges as undirected for
    the purpose of answering user queries about any relationship chain.
    Includes:
    - is_a, part_of, has_property, instance_of (both directions)
    - plus transitive leaps for is_a and part_of via helper checks
    """
    term = resolve(term)

    # direct forward edges
    for nxt in IS_A_INDEX.get(term, ()):  # term -> parent
        yield nxt
    for nxt in PART_OF_INDEX.get(term, ()):  # part -> whole
        yield nxt
    for nxt in HAS_PROPERTY_INDEX.get(term, ()):  # term -> property
        yield nxt
    for nxt in INSTANCE_OF_INDEX.get(term, ()):  # instance -> class
        yield nxt

    # direct reverse edges (treat as undirected connectivity)
    for child, parent in IS_A:
        if parent == term:
            yield child
    for part, whole in PART_OF:
        if whole == term:
            yield part
    for subj, prop in HAS_PROPERTY:
        if prop == term:
            yield subj
    for inst, cls in INSTANCE_OF:
        if cls == term or inst == term:
            # allow both ways
            yield inst
            yield cls


def connected(a: str, b: str) -> bool:
    a = resolve(a)
    b = resolve(b)
    if a == b:
        return True

    visited: Set[str] = set()
    queue: deque[str] = deque([a])
    while queue:
        node = queue.popleft()
        if node in visited:
            continue
        visited.add(node)
        for nxt in neighbors(node):
            if nxt == b:
                return True
            if nxt not in visited:
                queue.append(nxt)
    return False


# Convenience for explicit example queries
def connected_names(name_a: str, name_b: str) -> bool:
    return connected(name_a, name_b)


__all__ = [
    "CLASSES",
    "IS_A",
    "PART_OF",
    "HAS_PROPERTY",
    "INSTANCE_OF",
    "PRACTICAL_CLASSES",
    "ALIASES",
    "resolve",
    "is_a_transitive",
    "part_of_transitive",
    "has_part",
    "has_part_transitive",
    "connected",
    "connected_names",
]

