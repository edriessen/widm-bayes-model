# source: https://github.com/bzm10/ColorKit/blob/main/ColorKit/colorkit.py
def cmyk_to_rgb(c, m, y, k):
    c, m, y, k = c / 100.0, m / 100.0, y / 100.0, k / 100.0

    # CMYK -> CMY -> RGB
    r = (1 - c) * (1 - k)
    g = (1 - m) * (1 - k)
    b = (1 - y) * (1 - k)

    return (r, g, b)


def get_max_data_per_episode_from_player_data(player_data):
    episode_max_dict = {}

    for player, player_dict in player_data.items():
        for episode, episode_value in player_dict.items():
            if episode not in episode_max_dict:
                episode_max_dict[episode] = 0
            if episode_value > episode_max_dict[episode]:
                episode_max_dict[episode] = episode_value

    return episode_max_dict
