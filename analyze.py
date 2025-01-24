import math

# todo: add docstrings.

class WidmBayes():
    def __init__(self, observations):
        """
        Create WIDM-Driessen-Bayes class
        add season observations data
        and sets variable for game context.

        :param observations:
        """
        self.observations = observations

        self.games = []
        self.players = []
        self.player_dict = {}

    def _set_game_context(self):
        """
        Use observations to set season context data.

        :return:
        """
        self.players = self.observations.index.values
        self.games = self.observations.columns

        for player in self.players:
            self.player_dict[player] = {
                'total_chance': 1 / len(self.players),
            }


    def _get_game_int_and_episode_int(
            self,
            game_label: str
    ) -> [int, int]:
        """
        Transform game label to game int and episode int values
        :param game_label: label of a game (e.g. "o-1-1").
        :return: [int, int]
        """
        if '-' in game_label:
            game_info = game_label.split('-')
            episode_int = int(game_info[1])
            game_int = int(game_info[2])

            return game_int, episode_int

        if 'o' not in game_label:
            # get ints from legacy format
            game_int = int(game_label.replace('nr', ''))
            episode_int = math.ceil(game_int / 3)

            return game_int, episode_int

        game_int = int(game_label[2])
        episode_int = int(game_label[1])
        return game_int, episode_int

    def _apply_bayes(self, prior_belief, chance_true, chance_false):
        new_chance = \
            prior_belief * chance_true \
            / \
            (
                    prior_belief * chance_true
                    +
                    (chance_false * (1 - prior_belief))
            )

        return new_chance

    def _analyse_player_in_game(
            self,
            episode_label,
            episode_int,

            game_label,
            game_int,

            game_group_size,
            mole_group_size,
            loser_group_size,

            debug_player=''
    ):
        df = self.observations

        for player in self.players:
            player_value = df.iloc[df.index.get_loc(player), df.columns.get_loc(game_label)]
            if player_value == 'x':
                self.player_dict[player][episode_label] = 0
                continue

            mole_chance = 1 / game_group_size
            if player_value == 'm':
                mole_chance = 1 / mole_group_size

            player_chance = 1 / (game_group_size - 1)
            if player_value == 'a':
                player_chance = 1 / loser_group_size

            prior_mole_chance = self.player_dict[player]['total_chance']

            new_chance = self._apply_bayes(
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

            self.player_dict[player][episode_label] = new_chance
            self.player_dict[player]['total_chance'] = new_chance

    def _analyse_games(self, max_episode, debug_player=''):
        df = self.observations

        for game_label in self.games:
            game_int, episode_int = self._get_game_int_and_episode_int(game_label)

            if episode_int > max_episode:
                continue

            episode_label = 'afl. ' + str(episode_int)

            if 'o' in list(df[game_label]):
                for player in self.players:
                    player_value = df.iloc[df.index.get_loc(player), df.columns.get_loc(game_label)]
                    if player_value == 'x':
                        self.player_dict[player][episode_label] = 0
                    else:
                        self.player_dict[player][episode_label] = self.player_dict[player]['total_chance']
                continue

            game_group_size = len(df[df[game_label] != 'x'])
            mole_group_size = len(df[df[game_label] == 'm'])
            loser_group_size = len(df[df[game_label] == 'a'])

            self._analyse_player_in_game(
                episode_label,
                episode_int,

                game_label,
                game_int,

                game_group_size,
                mole_group_size,
                loser_group_size,
                debug_player,
            )

    def run(
        self,
        max_episode: int = 10
    ):
        """
        Run WIDM-Driessen-Bayes model based on given observations.

        :param max_episode: the maximum episode to include in the plot
        :return: none
        """
        self._set_game_context()
        self._analyse_games(max_episode)
