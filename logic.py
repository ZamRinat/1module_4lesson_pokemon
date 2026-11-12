from random import randint
import requests


class Pokemon:
    pokemons = {}

    # Инициализация объекта (конструктор)
    def __init__(self, pokemon_trainer):

        self.pokemon_trainer = pokemon_trainer

        self.pokemon_number = randint(1, 1000)
        self.img = self.get_img()
        self.name = self.get_name()

        self.hunger = 100

        Pokemon.pokemons[pokemon_trainer] = self

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

    def feed(self):
        if self.hunger >= 100:
            return f"{self.name} уже сыт!"
        self.hunger = min(100, self.hunger + 20)
        return f"Ты покормил {self.name}. Сытость: {self.hunger}/100"

    # Метод класса для получения информации
    def info(self):
        return f"Имя твоего покемона: {self.name}, сытость: {self.hunger}/100"

    # Метод класса для получения картинки покемона
    def show_img(self):
        return self.img
