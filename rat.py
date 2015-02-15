class rat:
    DEFAULT_MAX_HEALTH = 100
    DEFAULT_SNIFF_DISTANCE = 5

    name = ""
    health = DEFAULT_MAX_HEALTH
    max_health = DEFAULT_MAX_HEALTH
    sniff_distance = DEFAULT_SNIFF_DISTANCE

    def __init__(self, name, max_health):
        self.name = name
        self.health = max_health
        self.max_health = max_health