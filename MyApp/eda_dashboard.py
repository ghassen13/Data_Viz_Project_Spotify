import panel as pn
import sys

sys.path.append('D:/Master BDIA - M2/Data_Viz_Project/MyApp')
from EDA import data_show, plot_popularity_analysis,plot_duration_analysis,plot_energy_danceability,plot_energy_loudness
from component.eda.tempo_plot import TempoPlotter
from component.eda.table import DataTable
from component.eda.duration_plot import DurationPlotter
from component.eda.energy_loudness import EnergyLoudnessPlotter

from Data.data_loader import preProcessed_data
data = preProcessed_data

# Set the background color
background_color = "#000000"  # black color
text_color = "#1DB954"

# Link the external CSS file to the Panel app
pn.config.raw_css.append('styles.css')


# Set the background image
background_image_url = "https://png.pngtree.com/thumb_back/fh260/background/20230626/pngtree-spotify-logo-in-3d-rendering-image_3684274.jpg"  # replace with the actual path or URL

# Create the template with a black background, sidebar, and specific sidebar width
template = pn.template.FastListTemplate(
    title='Spotify Dashboard',
    header_color="#1DB954",
    collapsed_sidebar=False,
    header_background=background_color,
    sidebar_width=330,
    corner_radius=5,
    font='Roboto',
    font_weight='bold',
    sidebar_background="#33333",  
    footer_background="#ffffff",
)

# Instantiate TempoPlotter
tempo_plotter = TempoPlotter(data)
data_table = DataTable(data)
duration_plotter = DurationPlotter(data)
energy_loudness_plotter = EnergyLoudnessPlotter(data)


# Add a RangeSlider to interactively change the tempo range in the sidebar
tempo_slider = pn.widgets.RangeSlider(name='Tempo Range', start=0, end=250, value=tempo_plotter.tempo_range,css_classes=['custom-slider'])
tempo_slider.param.watch(tempo_plotter.update_plot, 'value')

# Create a CategorySelector for filtering by track genre
genre_selector = pn.widgets.Select(name='Select Genre', options=['All'] + sorted(data_table.data['Track Genre'].unique()), css_classes=['custom-select'])
genre_selector.param.watch(data_table._update_table, 'value')



# Create a FasList grid layout for better control
main_layout = pn.Column(
    data_table.layout,
    duration_plotter.layout,
    tempo_plotter.layout,
    energy_loudness_plotter.layout,
    
)

# Add the tempo slider to the sidebar
template.sidebar.append(tempo_slider)
# Add the CategorySelector to the sidebar
template.sidebar.append(genre_selector)

# Append the layout to the main area
template.main.append(main_layout)

# Display the template
template.servable()