from ..models import *


def update_player_stats(player_stats: Statistic):
    player_stats.captured_stones += 1
    player_stats.territory_points += 1  # is there a point in having one of the fields?


def versus_game_type_logic(game: Game, main_player_stats: Statistic, guest_player_stats: Statistic, stone: Stone):

    if game.start_with_color == 'Black' and not stone.color:  # if we as a user chose to be black and we lost a stone
        update_player_stats(guest_player_stats)
    elif game.start_with_color == 'White' and stone.color:  # if we as a user chose to be white and we lost a stone
        update_player_stats(guest_player_stats)
    else:  # a guest loses a stone
        update_player_stats(main_player_stats)


def check_liberties(game: Game, main_player_stats: Statistic, guest_player_stats: Statistic):

    # get game's stones:
    all_stones = Stone.objects.filter(game=game)

    # compare coordinates:
    for stone in all_stones:

        stone.has_left_neighbor()
        stone.has_right_neighbor()
        stone.has_upper_neighbor()
        stone.has_bottom_neighbor()

        if stone.is_captured():  # check and delete

            if game.game_type == 'Versus':
                versus_game_type_logic(game, main_player_stats, guest_player_stats, stone)
            elif game.game_type == 'Computer':
                pass  # TODO: implement single-player against the computer
            elif game.game_type == 'Multiplayer':
                pass  # TODO: implement multi-player


def proceed_game_logic(game: Game, main_player_stats: Statistic, guest_player_stats: Statistic):

    check_liberties(game, main_player_stats, guest_player_stats)
