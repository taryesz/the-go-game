from django.db import models
from django.contrib.auth.models import AbstractUser


class Player(AbstractUser):

    first_name = models.CharField(max_length=20, null=False, blank=False)
    last_name = models.CharField(max_length=20, null=False, blank=False)

    username = models.CharField(max_length=20, unique=True, null=False, blank=False)

    profile_picture = models.ImageField(default="default_user_pfp.png", null=True, blank=True)
    email = models.EmailField(null=False, blank=False)

    date_joined = models.DateTimeField(auto_now_add=True)

    friends_with = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='friends')
    # symmetrical can be False if the friendship works one way, and not both
    # if True, no need to use related_name='friends'
    # null=True has no effect on this field, because it's not a "normal" field

    dark_mode = models.BooleanField(default=False)

    LANGUAGES = (
        ('English', 'English'),
        ('Ukrainian', 'Ukrainian'),
        ('Polish', 'Polish'),
    )

    language = models.CharField(max_length=15, choices=LANGUAGES, default="English")

    def __str__(self):
        return str(self.username)

    def get_date_joined(self):
        return str(self.date_joined)

    def get_last_online(self):
        return str(self.last_login)


class Game(models.Model):

    TYPE = (
        ('Versus', 'Versus'),
        ('Computer', 'Computer'),
        ('Multiplayer', 'Multiplayer'),
    )

    SIZE = (
        (19, '19'),
        (13, '13'),
        (9, '9'),
    )

    COLOR = (
        ('Black', 'Black'),
        ('White', 'White'),
    )

    @staticmethod
    def calculate_max_length_of_options(options: tuple) -> int:

        max_length_of_options: int = 0

        for item in options:
            if len(item[0]) > max_length_of_options:
                max_length_of_options = len(item[0])

        return max_length_of_options

    game_type = models.CharField(max_length=calculate_max_length_of_options(TYPE), choices=TYPE, default="Versus")

    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)

    board_size = models.PositiveIntegerField(choices=SIZE, default=19)

    start_with_color = models.CharField(max_length=calculate_max_length_of_options(COLOR), choices=COLOR, default="Black")

    def __str__(self):
        return str(self.id)


class Statistic(models.Model):

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    OUTCOME = (
        ('Victory', 'Victory'),
        ('Loss', 'Loss'),
        ('Tie', 'Tie'),
    )

    @staticmethod
    def calculate_max_length_of_options(options: tuple) -> int:

        max_length_of_options: int = 0

        for item in options:
            if len(item[0]) > max_length_of_options:
                max_length_of_options = len(item[0])

        return max_length_of_options

    outcome = models.CharField(max_length=calculate_max_length_of_options(OUTCOME), choices=OUTCOME, blank=True)

    duration = models.PositiveIntegerField(blank=True, null=True)

    captured_stones = models.PositiveIntegerField(blank=True, default=0)
    territory_points = models.PositiveIntegerField(blank=True, default=0)

    last_move = models.BooleanField(default=True)

    def __str__(self):
        return str(str(self.game.id) + " - " + self.player.username)


class Stone(models.Model):

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    x_coord = models.PositiveIntegerField()
    y_coord = models.PositiveIntegerField()
    color = models.BooleanField(default=False)

    def __str__(self):
        return str(self.x_coord) + "x" + str(self.y_coord) + ": " + ("White" if self.color else "Black")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.adjacency_truth_table: list[bool] = []
        self.neighborhood: list[Stone] = []
        self.__set_stone_type()

    def has_left_neighbor(self) -> bool:

        LEFT_NEIGHBOR_X = self.x_coord - 1
        LEFT_NEIGHBOR_Y = self.y_coord

        all_stones = Stone.objects.filter(game=self.game)

        for existing_stone in all_stones:

            if existing_stone.x_coord == LEFT_NEIGHBOR_X and existing_stone.y_coord == LEFT_NEIGHBOR_Y:
                self.__fill_adjacency_truth_table(True)
                self.__fill_neighborhood(existing_stone)
                return True

        self.__fill_adjacency_truth_table(False)
        return False

    def has_right_neighbor(self) -> bool:

        RIGHT_NEIGHBOR_X = self.x_coord + 1
        RIGHT_NEIGHBOR_Y = self.y_coord

        all_stones = Stone.objects.filter(game=self.game)

        for existing_stone in all_stones:

            if existing_stone.x_coord == RIGHT_NEIGHBOR_X and existing_stone.y_coord == RIGHT_NEIGHBOR_Y:
                self.__fill_adjacency_truth_table(True)
                self.__fill_neighborhood(existing_stone)
                return True

        self.__fill_adjacency_truth_table(False)
        return False

    def has_upper_neighbor(self) -> bool:

        UPPER_NEIGHBOR_X = self.x_coord
        UPPER_NEIGHBOR_Y = self.y_coord - 1

        all_stones = Stone.objects.filter(game=self.game)

        for existing_stone in all_stones:

            if existing_stone.x_coord == UPPER_NEIGHBOR_X and existing_stone.y_coord == UPPER_NEIGHBOR_Y:
                self.__fill_adjacency_truth_table(True)
                self.__fill_neighborhood(existing_stone)
                return True

        self.__fill_adjacency_truth_table(False)
        return False

    def has_bottom_neighbor(self) -> bool:

        BOTTOM_NEIGHBOR_X = self.x_coord
        BOTTOM_NEIGHBOR_Y = self.y_coord + 1

        all_stones = Stone.objects.filter(game=self.game)

        for existing_stone in all_stones:

            if existing_stone.x_coord == BOTTOM_NEIGHBOR_X and existing_stone.y_coord == BOTTOM_NEIGHBOR_Y:
                self.__fill_adjacency_truth_table(True)
                self.__fill_neighborhood(existing_stone)
                return True

        self.__fill_adjacency_truth_table(False)
        return False

    def __fill_neighborhood(self, neighbor: 'Stone') -> None:
        self.neighborhood.append(neighbor)

    def __fill_adjacency_truth_table(self, value: bool) -> None:
        self.adjacency_truth_table.append(value)

    def __check_if_corner(self) -> bool:

        if self.x_coord == 1 and self.y_coord == 1:
            return True
        elif self.x_coord == self.game.board_size and self.y_coord == 1:
            return True
        elif self.x_coord == 1 and self.y_coord == self.game.board_size:
            return True
        elif self.x_coord == self.game.board_size and self.y_coord == self.game.board_size:
            return True
        else:
            return False

    def __check_if_border(self) -> bool:

        if self.x_coord == 1 and self.y_coord in range(2, self.game.board_size):
            return True
        elif self.x_coord == self.game.board_size and self.y_coord in range(2, self.game.board_size):
            return True
        elif self.x_coord in range(2, self.game.board_size) and self.y_coord == 1:
            return True
        elif self.x_coord in range(2, self.game.board_size) and self.y_coord == self.game.board_size:
            return True
        else:
            return False

    def __set_stone_type(self) -> None:

        if self.__check_if_corner():
            self.type = 'corner'
        elif self.__check_if_border():
            self.type = 'border'
        else:
            self.type = 'middle'

    def is_captured(self) -> bool:

        truth_counter = 0

        # check how many neighbors the stone has
        for value in self.adjacency_truth_table:
            if value:
                truth_counter += 1

        # check colors to see if the neighboring stones are team or opponents
        for neighbor in self.neighborhood:
            if neighbor.color is self.color:
                truth_counter -= 1

        if self.type == 'corner' and truth_counter == 2:  # each corner stone can have max two neighbors
            return True
        elif self.type == 'border' and truth_counter == 3:  # each border stone can have max three neighbors
            return True
        elif self.type == 'middle' and truth_counter == 4:  # each middle stone can have max four neighbors
            return True
        else:  # if the neighbor turns out to be our team player
            return False

    def print(self):
        print("========================================")
        print(f"STONE @: {self.x_coord}, {self.y_coord} | COLOR: {self.color}")
        print(f"NEIGHBORS: {self.adjacency_truth_table}")
