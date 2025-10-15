import unittest
from kpo import DIContainer, Zoo, VeterinaryClinic, Monkey, Rabbit, Tiger, Table

class TestDI(unittest.TestCase):
    def test_register_and_get(self):
        d = DIContainer()
        obj = VeterinaryClinic()
        d.register("vet", obj)
        self.assertIs(d.get("vet"), obj)

class TestVetClinic(unittest.TestCase):
    def test_check_pass(self):
        vet = VeterinaryClinic()
        a = Tiger("Шерхан", 5, 80)
        self.assertTrue(vet.check(a))
    def test_check_fail(self):
        vet = VeterinaryClinic()
        a = Tiger("Больной", 5, 20)
        self.assertFalse(vet.check(a))

class TestZoo(unittest.TestCase):
    def setUp(self):
        self.vet = VeterinaryClinic()
        self.zoo = Zoo(self.vet)
    def test_accept_animal_success(self):
        a = Rabbit("Кроля", 1, 70, 7)
        self.zoo.accept_animal(a)
        self.assertEqual(len(self.zoo.animals), 1)
    def test_accept_animal_fail(self):
        a = Rabbit("ЖизньюБитый", 2, 30, 7)
        self.zoo.accept_animal(a)
        self.assertEqual(len(self.zoo.animals), 0)
    def test_contact_zone(self):
        a1 = Monkey("Моня", 3, 70, 8)
        a2 = Rabbit("ЕгоРазбудилив5Утра", 1, 70, 3)
        self.zoo.animals = [a1, a2]
        lst = [a.name for a in self.zoo.animals if isinstance(a, type(a1)) and a.in_contact_zone()]
        self.assertIn("Моня", lst)
        self.assertNotIn("ЕгоРазбудилив5Утра", lst)
    def test_inventory_add(self):
        t = Table("Я-Стол")
        self.zoo.add_item(t)
        self.assertEqual(len(self.zoo.items), 1)

if __name__ == "__main__":
    unittest.main()
