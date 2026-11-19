from random import randint
import requests
from datetime import datetime, timedelta


class Pokemon:
    pokemons = {}

    # Инициализация объекта (конструктор)
    def __init__(self, pokemon_trainer):

        self.pokemon_trainer = pokemon_trainer

        self.pokemon_number = randint(1, 1000)
        self.img = self.get_img()
        self.name = self.get_name()

        self.hunger = 100

        self.power = randint(10, 20)
        self.hp = randint(100, 200)

        self.last_feed_time = datetime.now()

        Pokemon.pokemons[pokemon_trainer] = self

    def feed(self, feed_interval=20, hp_increase=10):
        current_time = datetime.now()
        delta_time = timedelta(seconds=feed_interval)
        if (current_time - self.last_feed_time) > delta_time:
            self.hp += hp_increase
            self.last_feed_time = current_time
            return f"Здоровье покемона увеличено. Текущее здоровье: {self.hp}"
        else:
            return f"Следующее время кормления покемона: {self.last_feed_time + delta_time}"

    # Метод для получения картинки покемона через API
    def get_img(self):
        url = f"https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data["sprites"]["front_default"]
        else:
            return "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTLcyG0ovVKlCryBdxLBN4pKDh3PwSpW77Nbo2D64gBwpPlJX2WVkBRzYk&s=10"

    # Метод для получения имени покемона через API
    def get_name(self):
        url = f"https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data["forms"][0]["name"]
        else:
            return "Pikachu"

    # Метод класса для получения картинки покемона
    def show_img(self):
        return self.img

    def attack(self, enemy):
        if self.hunger < 10:
            return f"{self.name} слишком голоден, чтобы атаковать! Покорми его."
        self.hunger -= 10

        if isinstance(
            enemy, Wizard
        ):  # Проверка на то, что enemy является типом данных Wizard
            chance = randint(1, 5)
            if chance == 1:
                return "Покемон-волшебник применил щит в сражении"
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"Сражение @{self.pokemon_trainer} с @{enemy.pokemon_trainer}"
        else:
            enemy.hp = 0
            return f"Победа @{self.pokemon_trainer} над @{enemy.pokemon_trainer}! "

    def feed_food(self):
        if self.hunger >= 100:
            return f"{self.name} уже сыт!"
        self.hunger = min(100, self.hunger + 20)
        return f"Ты покормил {self.name}. Сытость: {self.hunger}/100"

    # Метод класса для получения информации
    def info(self):
        if isinstance(self, Wizard):
            kind = "волшебника"
        elif isinstance(self, Fighter):
            kind = "бойца"
        else:
            kind = "покемона"
        return (
            f"Имя твоего {kind}: {self.name}\n"
            f"Сытость: {self.hunger}/100\n"
            f"Мощь твоего покемона: {self.power}\n"
            f"Здоровье его: {self.hp}"
        )


class Wizard(Pokemon):
    def feed(self):
        return super().feed(feed_interval=30, hp_increase=20)


class Fighter(Pokemon):
    def feed(self):
        return super().feed(feed_interval=10, hp_increase=10)

    def attack(self, enemy):
        super_power = randint(5, 15)
        self.power += super_power
        result = super().attack(enemy)
        self.power -= super_power
        return result + f"\nБоец применил супер-атаку силой:{super_power} "


if __name__ == "__main__":
    import time

    pokemon = Pokemon("Ash")
    wizard = Wizard("Gandalf")
    fighter = Fighter("Conan")

    print("--- Ждем 3 секунды (time.sleep) ---")
    time.sleep(3)

    print(pokemon.info())
    print(pokemon.feed(2, 10))
    print(pokemon.attack(wizard))
    print(fighter.attack(pokemon))
    print(wizard.attack(fighter))
