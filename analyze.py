import math

def set_player_data_from_df(df):
    players = df.index.values
    player_dict = {}
    for player in players:
        player_dict[player] = {
            'total_chance': 1 / len(players),
        }

    return players, player_dict


def get_game_int_and_episode_int(game_label):
    if 'o' not in game_label:
        # get ints from legacy format
        game_int = int(game_label.replace('nr', ''))
        episode_int = math.ceil(game_int / 3)

        return game_int, episode_int

    game_int = int(game_label[2])
    episode_int = int(game_label[1])
    return game_int, episode_int


def apply_bayes(prior_belief, chance_true, chance_false):
    new_chance = \
        prior_belief * chance_true \
        / \
        (
                prior_belief * chance_true
                +
                (chance_false * (1 - prior_belief))
        )

    return new_chance


def get_season_data_by_max_episode(season_data, max_episode, debug_player=''):
    df = season_data
    players, player_dict = set_player_data_from_df(df)
    games = df.columns

    for game in games:
        game_int, episode_int = get_game_int_and_episode_int(game)

        if episode_int > max_episode:
            continue

        episode_label = 'afl. ' + str(episode_int)

        if 'o' in list(df[game]):
            for player in players:
                player_value = df.iloc[df.index.get_loc(player), df.columns.get_loc(game)]
                if player_value == 'x':
                    player_dict[player][episode_label] = 0
                else:
                    player_dict[player][episode_label] = player_dict[player]['total_chance']
            continue

        game_players = len(df.query(game + ' != "x"'))
        mole_group_size = len(df.query(game + ' == "m"'))
        loser_group_size = len(df.query(game + ' == "a"'))

        for player in players:
            player_value = df.iloc[df.index.get_loc(player), df.columns.get_loc(game)]
            if player_value == 'x':
                player_dict[player][episode_label] = 0
                continue

            mole_chance = 1 / game_players
            if player_value == 'm':
                mole_chance = 1 / mole_group_size

            player_chance = 1 / (game_players - 1)
            if player_value == 'a':
                player_chance = 1/loser_group_size

            prior_mole_chance = player_dict[player]['total_chance']

            new_chance = apply_bayes(
                prior_belief=prior_mole_chance,
                chance_true=mole_chance,
                chance_false=player_chance
            )

            # enable to debug chance development
            if debug_player and player == debug_player:
                print('---')
                print(f'{player}, afl. {str(episode_int)}, opd. {str(game_int)}')
                print('prior belief: ', prior_mole_chance)
                print('mole chance: ', mole_chance)
                print('player chance: ', player_chance)
                print('updated belief: ', new_chance)

            player_dict[player][episode_label] = new_chance
            player_dict[player]['total_chance'] = new_chance

    return player_dict


def get_max_data_per_episode_from_player_data(player_data):
    episode_max_dict = {}

    for player, player_dict in player_data.items():
        for episode, episode_value in player_dict.items():
            if episode not in episode_max_dict:
                episode_max_dict[episode] = 0
            if episode_value > episode_max_dict[episode]:
                episode_max_dict[episode] = episode_value

    return episode_max_dict
