import unittest

from src.ontology import (
    CLASSES,
    IS_A,
    PART_OF,
    HAS_PROPERTY,
    INSTANCE_OF,
    PRACTICAL_CLASSES,
    resolve,
    is_a_transitive,
    part_of_transitive,
    has_part,
    has_part_transitive,
    connected_names,
)


class TestOntology(unittest.TestCase):
    def test_class_count(self):
        self.assertGreaterEqual(len(CLASSES), 20)

    def test_three_relations_present(self):
        self.assertGreater(len(IS_A), 0)
        self.assertGreater(len(PART_OF), 0)
        self.assertGreater(len(HAS_PROPERTY), 0)

    def test_four_level_hierarchy(self):
        # entity <- physical_object <- organism <- animal <- vertebrate <- mammal <- canine <- dog
        self.assertTrue(is_a_transitive("dog", "entity"))
        self.assertTrue(is_a_transitive("canine", "animal"))
        self.assertTrue(is_a_transitive("mammal", "animal"))

    def test_instances_for_practical_classes(self):
        # Ensure at least two instances for each practical class
        class_to_instances = {}
        for inst, cls in INSTANCE_OF:
            class_to_instances.setdefault(cls, set()).add(inst)
        for cls in PRACTICAL_CLASSES:
            self.assertGreaterEqual(len(class_to_instances.get(cls, set())), 2, msg=f"Class {cls} has < 2 instances")

    def test_part_of_transitive(self):
        # eye part_of head, head part_of vertebrate -> eye part_of vertebrate
        self.assertTrue(part_of_transitive("eye", "vertebrate"))

    def test_has_part_transitive(self):
        # bird has_part wing, and wing has feather by property; but has_part should follow part relations
        self.assertTrue(has_part("bird", "wing"))
        self.assertTrue(has_part_transitive("bird", "wing"))

    def test_connected_example_ua(self):
        # Чи "собака" пов'язана з "шерсть"? так, через хвіст -> шерсть
        self.assertTrue(connected_names("собака", "шерсть"))

    def test_connected_cross_relations(self):
        # snake connected to scale via property
        self.assertTrue(connected_names("snake", "scale"))
        # sparrow connected to feather via wing -> feather
        self.assertTrue(connected_names("sparrow", "feather"))

    def test_resolve_aliases(self):
        self.assertEqual(resolve("кіт"), "cat")
        self.assertEqual(resolve("пес"), "dog")


if __name__ == "__main__":
    unittest.main()

