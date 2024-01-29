import matplotlib.pyplot as plt
import pandas as pd
from analyze import get_max_data_per_episode_from_player_data

mol_color = '#39870c'


def plot_player_data(
        player_data,
        file_name=''
):
    episode_max = get_max_data_per_episode_from_player_data(player_data)

    plot_height = len(player_data)
    # correct with -1 to remove 'total chance'
    plot_width = len(player_data[list(player_data.keys())[0]]) - 1

    fig, axs = plt.subplots(plot_height, plot_width, sharex=True, sharey=True, figsize=(12,9))
    fig.subplots_adjust(wspace=-.2, hspace=0.05)
    font_size = 10
    for index, value in enumerate(player_data.items()):
        player = value[0]
        player_values= value[1]
        for index2, value2 in enumerate(player_values.items()):
            episode = value2[0]
            episode_score = value2[1]
            if episode != 'total_chance':
                ax = axs[index, index2 -1 ]
                color = '#aaaaaa'
                edge_color = 'none'
                if episode_score == episode_max[episode]:
                    color = mol_color
                    edge_color = mol_color
                if episode_score > episode_max[episode] * .8:
                    edge_color = mol_color
                ax.scatter(1, 1, s=episode_score*500, c=color, edgecolor=edge_color, lw=2)
                if index == 0:
                    ax.set_title(episode, fontsize=font_size)
                if index2 - 1 == 0:
                    ax.set_ylabel('\n'+player, rotation=0, fontsize=font_size)

                for spine in ['left', 'right', 'top']:
                    ax.spines[spine].set_visible(False)

                ax.spines['bottom'].set_color('#eeeeee')

                ax.get_xaxis().set_visible(False)
                ax.set_yticks([])

    if file_name:
        plt.savefig(f'{file_name}')
    else:
        plt.show()

    plt.close()


def plot_player_dev(
        player_data,
        start_ep,
        stop_ep,
        focus_player,
        label_players,
        exclude_players,
        file_name=''
):
    plt.xlim([-1, 2])
    plt.ylim([0, .6])
    for player in player_data:
        if player not in exclude_players and player + ' (x?)' not in exclude_players:
            data_point_1 = player_data[player]['afl. '+str(start_ep)]
            data_point_2 = player_data[player]['afl. '+str(stop_ep)]
            color = '#777'
            z_order = 1

            if player == focus_player:
                color = mol_color
                z_order = 2

            plt.plot(
                [data_point_1, data_point_2],
                marker='o',
                c=color,
                zorder=z_order
            )

            if player in label_players:
                annotate_label = player
                annotate_x = 1.05
                annotate_y = data_point_2
                plt.annotate(
                    annotate_label,
                    (annotate_x, annotate_y),
                    size=10,
                    va='center',
                    ha='left',
                    c=color
                )

    plt.axis('off')

    if file_name:
        plt.savefig(f'{file_name}')
    else:
        plt.show()

    plt.close()


def plot_result_per_episode(year, player_data):
    color_dict = {
        'dark': '#1E191A',
        'light': '#F4F3F8',
        'green': '#39870c',
        'grey': '#ccc'
    }

    player_df = pd.DataFrame(player_data).transpose()
    episodes = player_df.columns
    players = player_df.index

    x_values = []
    y_values = []
    for index, player in enumerate(players):
        x_values.append(index)
        y_values.append(1)

    for index, episode in enumerate(episodes):
        scores = player_df[episode] * 1500
        if sum(scores) == 0:
            continue

        if index == 0:
            scores = []
            for value in range(0, len(players)):
                scores.append(0.1 * 1500)

        color_list = []
        edge_color_list = []
        max_score = max(scores)

        for score in scores:
            color = color_dict['grey']
            edge_color = color_dict['dark']
            if score == max_score:
                color = color_dict['green']
                edge_color = color
            elif score > 0:
                color = color_dict['dark']

            color_list.append(color)
            edge_color_list.append(edge_color)

        fig = plt.figure(figsize=(8, 4), facecolor=color_dict['light'])
        ax = fig.subplots(1)

        ax.scatter(
             x=x_values,
             y=y_values,
             s=scores,
             facecolor=color_list,
             edgecolors=edge_color_list,
        )

        episode_label = episode
        if 'total' in episode_label:
            episode_label = 'afl. 0'

        ax.set_title(f'widm {str(year)} model: {episode_label}', loc='center', color=color_dict['dark'], weight='bold')
        ax.set_facecolor(color_dict['light'])
        ax.set_xlim([-1, 10])
        ax.set_ylim([0, 2])
        ax.axis('off')

        for i, txt in enumerate(players):
            annotate_label = txt
            annotate_x = x_values[i]
            annotate_y = y_values[i] - .25
            plt.annotate(
                annotate_label,
                (annotate_x, annotate_y),
                size=10,
                va='bottom',
                ha='center',
                c=color_list[i]
            )

        plt.savefig(f'plots/episodes/{str(year)} plot {episode_label}.png')