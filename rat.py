class rat:
    DEFAULT_MAX_HEALTH = 100
    DEFAULT_SNIFF_DISTANCE = 5

    color = 1
    name = ""
    health = DEFAULT_MAX_HEALTH
    max_health = DEFAULT_MAX_HEALTH
    sniff_distance = DEFAULT_SNIFF_DISTANCE
    row = 0
    col = 0

    def __init__(self, color, row, col, name, max_health):
        self.color = color
        self.name = name
        self.health = max_health
        self.max_health = max_health
        self.row = row
        self.col = col
