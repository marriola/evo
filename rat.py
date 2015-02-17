import random

def mutate(value, range):
    return value + random.randint(-range, range)    

class Rat:
    NAMES = ["Bonnie", "Clyde", "Zeke", "Biff", "Randy", "Jax", "Walter", "Gale", "Nova", "Boof", "Sam", "Huell"]

    NEW_SPECIES_RATE = 25
    DEFAULT_MAX_HEALTH = 200
    DEFAULT_SNIFF_DISTANCE = 5
    DEFAULT_HEALTH_DECAY = 1

    color = 1
    name = ""
    health = DEFAULT_MAX_HEALTH
    max_health = DEFAULT_MAX_HEALTH
    health_decay = DEFAULT_HEALTH_DECAY
    sniff_distance = DEFAULT_SNIFF_DISTANCE
    direction = None
    row = 0
    col = 0
    generation = 0

    def __init__(self, color, row, col, name, max_health, health_decay, sniff_distance, generation=1):
        self.generation = generation
        self.color = color
        self.name = name
        self.health = max_health / 2
        self.max_health = max_health
        self.health_decay = health_decay
        self.sniff_distance = sniff_distance
        self.row = row
        self.col = col
        self.direction = random.randint(1, 8)

    def reproduce(self):
        self.health /= 2
        color = self.color
        if random.randint(0, Rat.NEW_SPECIES_RATE) == 0:
            color = random.randint(1, 16)

        return Rat(color, self.row, self.col, Rat.NAMES[random.randint(0, len(Rat.NAMES))], mutate(self.max_health, 20), 1, mutate(self.sniff_distance, 5), self.generation + 1)
