import itertools

class DIContainer:
    def __init__(self):
        self._deps = {}
    def register(self, name, obj):
        self._deps[name] = obj
    def get(self, name):
        return self._deps.get(name)

class InventoryItem:
    _next_number = itertools.count(1)
    def __init__(self, name):
        self.name = name
        self.number = next(InventoryItem._next_number)

class Table(InventoryItem):
    pass

class Computer(InventoryItem):
    pass

class Animal:
    _next_id = itertools.count(1001)
    def __init__(self, name, food, health):
        self.name = name or "Безымянный"
        self.food = int(food)
        self.health = int(health)
        self.id = next(Animal._next_id)
    def species(self):
        return self.__class__.__name__

class Herbivore(Animal):
    def __init__(self, name, food, health, kindness):
        super().__init__(name, food, health)
        self.kindness = int(kindness)
    def in_contact_zone(self):
        return self.kindness >= 6 and self.health > 40

class Predator(Animal):
    pass

class Monkey(Herbivore):
    pass

class Rabbit(Herbivore):
    pass

class Tiger(Predator):
    pass

class Wolf(Predator):
    pass

class VeterinaryClinic:
    def check(self, animal):
        if animal.health < 45:
            print(f"❌ {animal.name} ({animal.species()}) не прошёл осмотр (здоровье={animal.health})")
            return False
        return True

class Zoo:
    def __init__(self, vet):
        self.vet = vet
        self.animals = []
        self.items = []
    def add_item(self, item):
        self.items.append(item)
    def accept_animal(self, animal):
        if self.vet.check(animal):
            self.animals.append(animal)
            print(f"✅ {animal.name} ({animal.species()}) принят в зоопарк\n")
        else:
            print(f"🚫 {animal.name} отклонён\n")
    def show_stats(self):
        print(f"Животных в зоопарке: {len(self.animals)}")
        print(f"Общий расход корма в день: {sum(a.food for a in self.animals)} кг")
    def show_contact_zone(self):
        lst = [a for a in self.animals if isinstance(a, Herbivore) and a.in_contact_zone()]
        if not lst:
            print("Нет животных для контактного зоопарка")
        else:
            print("Контактный зоопарк:")
            for a in lst:
                print(f" - {a.name} ({a.species()}), доброта={a.kindness}, здоровье={a.health}")
    def show_inventory(self):
        print("Инвентарь:")
        for i in self.items:
            print(f" - {i.name} (№{i.number})")
        for a in self.animals:
            print(f" - {a.name} (животное #{a.id})")

def ask_int(prompt, default=None):
    while True:
        s = input(prompt).strip()
        if s == "" and default is not None:
            return default
        try:
            return int(s)
        except ValueError:
            print("Введите число!")

def create_animal(kind):
    name = input("Имя животного: ").strip()
    food = ask_int("Сколько кг еды в день: ", 3)
    health = ask_int("Здоровье (0-100): ", 70)
    if kind in ["monkey", "rabbit"]:
        kindness = ask_int("Доброта (0-10): ", 5)
        if kind == "monkey":
            return Monkey(name, food, health, kindness)
        return Rabbit(name, food, health, kindness)
    if kind == "tiger":
        return Tiger(name, food, health)
    if kind == "wolf":
        return Wolf(name, food, health)

def main():
    di = DIContainer()
    vet = VeterinaryClinic()
    di.register("vet", vet)
    zoo = Zoo(di.get("vet"))
    di.register("zoo", zoo)

    zoo.add_item(Table("Кормовой стол"))
    zoo.add_item(Computer("ПК администратора"))

    while True:
        print("\n1. Добавить животное")
        print("2. Показать статистику")
        print("3. Контактный зоопарк")
        print("4. Инвентарь")
        print("5. Добавить вещь")
        print("0. Выход")
        cmd = input("Выбор: ").strip()

        if cmd == "1":
            t = input("Тип (monkey/rabbit/tiger/wolf): ").lower().strip()
            if t not in ["monkey", "rabbit", "tiger", "wolf"]:
                print("Неизвестный тип")
                continue
            animal = create_animal(t)
            zoo.accept_animal(animal)

        elif cmd == "2":
            zoo.show_stats()

        elif cmd == "3":
            zoo.show_contact_zone()

        elif cmd == "4":
            zoo.show_inventory()

        elif cmd == "5":
            t = input("Вещь (table/computer): ").lower().strip()
            name = input("Название: ").strip() or "Без названия"
            if t == "table":
                zoo.add_item(Table(name))
            else:
                zoo.add_item(Computer(name))
            print("Добавлено.")

        elif cmd == "0":
            break
        else:
            print("Неверный ввод.")

if __name__ == "__main__":
    main()
