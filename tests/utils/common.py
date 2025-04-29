import string
import random


def generate_rand_str(length=10) -> str:
    characters = string.digits + string.ascii_letters
    sequence = ''.join(random.choice(characters) for _ in range(length))
    return sequence
