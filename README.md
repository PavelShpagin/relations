# Ontology Lab (Python)

Clean Python implementation of an ontology with reasoning over relations. No external dependencies.

What it includes:
- 20+ classes with a 4+-level `is_a` hierarchy
- 3 relations: `is_a`, `part_of`, `has_property` (+ `instance_of` for individuals)
- 2+ instances for every practical (leaf-like) class
- Alias resolution for Ukrainian/English terms (e.g., `"собака"` -> `dog`)
- Connectivity queries such as: Is "собака" connected to "шерсть"? -> Yes, via `собака -> хвіст` and `хвіст -> шерсть`

## Quickstart

Requirements: Python 3.9+

Run tests:

```bash
python -m unittest
```

Run an ad-hoc query in a Python REPL:

```python
from src.ontology import connected_names
connected_names("собака", "шерсть")  # True
```

## Structure

- `src/ontology.py`: ontology data and reasoning functions
- `tests/test_ontology.py`: unit tests verifying requirements

## API Overview

- `resolve(name: str) -> str`: resolve UA/EN aliases to canonical tokens
- `is_a_transitive(child: str, ancestor: str) -> bool`
- `part_of_transitive(part: str, whole: str) -> bool`
- `has_part(whole: str, part: str) -> bool`
- `has_part_transitive(whole: str, part: str) -> bool`
- `connected(a: str, b: str) -> bool`
- `connected_names(name_a: str, name_b: str) -> bool`

Examples:

```python
from src.ontology import is_a_transitive, connected_names
is_a_transitive("dog", "entity")  # True
connected_names("горобець", "перо")  # True
```
