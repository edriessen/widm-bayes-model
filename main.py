import pandas as pd
from analyze import WidmBayes
from visualize import plot_player_data

df_observations = pd.read_excel(
    f'input_data/2025 widm observations.xlsx',
    index_col='Kandidaat'
)

widm_model = WidmBayes(observations=df_observations)
widm_model.run(max_episode=10)

# save output if wanted
new_df = pd.DataFrame(widm_model.player_dict)
new_df.transpose().to_excel('output_data/2025_codeerik_results.xlsx')

plot_player_data(
    player_data=widm_model.player_dict,
    max_episode=3,
    file_name=f'plots/2025_new_plot_REFACTOR_ep',
)

