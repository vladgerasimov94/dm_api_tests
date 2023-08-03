import random
from string import ascii_letters, digits

import allure


def random_string(begin: int = 1, end: int = 30) -> str:
    with allure.step("Генерация рандомной строки"):
        symbols = ascii_letters + digits
        string = ""
        for _ in range(random.randint(begin, end)):
            string += random.choice(symbols)
        return string
