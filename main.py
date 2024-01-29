import pandas as pd
from analyze import get_season_data_by_max_episode
from visualize import (
    plot_player_data,
    plot_player_dev,
    plot_result_per_episode
)

###
# analyse
###
df_observations = pd.read_excel(
    'input_data/2024 widm observations.xlsx',
    index_col='Kandidaat'
)

player_data = get_season_data_by_max_episode(
    season_data=df_observations,
    max_episode=9,
    # debug_player='Kees',
)

new_df = pd.DataFrame(player_data)
new_df.transpose().to_excel('output_data/2024_codeerik_results.xlsx')

###
# visualize
###
plot_player_data(
    player_data=player_data,
    file_name='plots/2024_results_ep4.png',
)

plot_player_dev(
    player_data=player_data,
    start_ep=3,
    stop_ep=4,
    focus_player='Kees',
    label_players=['Kees', 'Rian', 'Fons'],
    exclude_players=['Babs (x?)', 'Jip (x?)', 'Justin (x?)'],
    file_name='plots/slopes/2024_ep_2_to_3.png'
)

plot_result_per_episode(
    year=2024,
    player_data=player_data
)
