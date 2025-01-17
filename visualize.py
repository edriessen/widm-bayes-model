import matplotlib.pyplot as plt
import pandas as pd
from analyze import get_max_data_per_episode_from_player_data
from _utils import cmyk_to_rgb

mol_color = '#39870c'
mol_color = cmyk_to_rgb(75, 21, 73, 0) # green
gray_color = cmyk_to_rgb(28, 18, 20, 0) # neutral gray
bg_color = cmyk_to_rgb(2, 7, 44, 0) # naplesyellow
font_size = 14


def plot_player_data(
        player_data,
        file_name='',
        max_episode=1,
):
    episode_max = get_max_data_per_episode_from_player_data(player_data)

    fig, ax = plt.subplots(
        sharex=True,
        sharey=True,
        figsize=(11,11),
        # facecolor=bg_color,
    )
    ax.set_facecolor('none')
    fig.subplots_adjust(left=.2, right=.9, top=.9, bottom=.05)

    for index, value in enumerate(player_data.items()):
        player = value[0]
        player_values= value[1]

        ax.text(
            x=.5,
            y=index,
            s=player,
            fontsize=font_size,
            va='center',
            ha='right',
        )


        for index2, value2 in enumerate(player_values.items()):
            episode = value2[0]
            episode_score = value2[1]


            if episode != 'total_chance':
                # ax = axs[index, index2 -1 ]
                episode_int = int(episode.split(' ')[1])
                if index == 0:
                    ax.text(
                        x=episode_int,
                        y=-1.5,
                        s=episode,
                        ha='center',
                        va='bottom',
                        fontsize=font_size,
                    )

                color = gray_color

                if episode_int <= max_episode:
                    episode_max_score = episode_max[episode]

                    if episode_score == episode_max_score:
                        color = mol_color

                    episode_max_score = episode_max[episode]
                    episode_score_rel = episode_score/episode_max_score

                    scatter_r = 1500

                    lw_val = 1
                    ax.scatter(
                        episode_int, index,
                        s=episode_score*scatter_r,
                        color=color,
                        edgecolor='black',
                        lw=lw_val,
                        zorder=5
                    )


                    if episode_score_rel > 0:
                        ax.scatter(
                            episode_int, index,
                            s=episode_max_score*scatter_r,
                            color='white',
                            edgecolor='black',
                            lw=lw_val,
                            zorder=2
                        )

                ax.plot(
                    [episode_int, episode_int],
                    [-1, len(player_data)],
                    lw=lw_val, color='black', zorder=1,
                    # marker='_',
                    solid_capstyle='round',
                )

                for spine in ['left', 'bottom', 'top', 'right']:
                    ax.spines[spine].set_visible(False)

                ax.get_xaxis().set_visible(False)
                ax.set_yticks([])

    ax.set_ylim(len(player_data)+3, -2)

    for index, label in enumerate([
        'grootste molkans in afl.',
        'speler heeft grootste molkans in afl.',
        'speler heeft niet de grootste molkans in afl.']
    ):
        ax.text(
            x=1.25,
            y=len(player_data)+1+(.5*index),
            s=label,
            va='center',
            ha='left',
            fontsize=12
        )
        # scatter
        fill_color = 'white'
        edge_color = 'black'

        if index == 1:
            fill_color = mol_color

        if index == 2:
            fill_color = '#aaaaaa'

        ax.scatter(
            [1],
            [len(player_data)+1+(.5*index)],
            color=fill_color,
            edgecolor=edge_color,
            s=125,
        )
    # ax.legend(
    #     ncol=1,
    #     loc=2,
    #     bbox_to_anchor=(-.1, -.075),
    #     fontsize=font_size,
    #     frameon=False
    # )


    if file_name:
        plt.savefig(f'{file_name}{str(max_episode)}.png')
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