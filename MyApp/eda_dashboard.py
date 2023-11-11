import panel as pn
from bokeh.models import CustomJS


from component.eda.tempo_plot import TempoPlotter
from component.eda.table import DataTable
from component.eda.duration_plot import DurationPlotter
from component.eda.scatter_plot import ScatterPlotter
from component.eda.bar_plot import BarPlotter
from component.eda.heatmap import HeatmapPlotter
from component.eda.piechart import PieChart

from Data.data_loader import preProcessed_data
data = preProcessed_data

# Set the background color
background_color = "#000000"  # black color
text_color = "#1DB954"
# Set the background image

logo_url = "logo-removebg-preview.png"


# Instantiate Functions
tempo_plotter = TempoPlotter(data)
data_table = DataTable(data)
duration_plotter = DurationPlotter(data)
Scatter_Plotter = ScatterPlotter(data)
Bar_plotter = BarPlotter(data)
Pie_chart = PieChart(data)
Heatmap_Plotter = HeatmapPlotter(data)


# FILTERS

# Add a RangeSlider to interactively change the tempo range in the sidebar
tempo_slider = pn.widgets.RangeSlider(name='Tempo Range', start=0, end=250, value=tempo_plotter.tempo_range,css_classes=['custom-slider'])
tempo_slider.param.watch(tempo_plotter.update_plot, 'value')

# Create a CategorySelector for filtering by track genre
genre_selector = pn.widgets.Select(name='Select Genre', options=['All'] + sorted(data_table.data['Track Genre'].unique()), css_classes=['custom-select'])
genre_selector.param.watch(data_table._update_table, 'value')

# Create a RangeSlider for popularity
popularity_filter = pn.widgets.RangeSlider(name='Popularity Range', start=data['Popularity'].min(), end=data['Popularity'].max(), step=1, value=(data['Popularity'].min(), data['Popularity'].max()))
popularity_filter.param.watch(data_table._update_table, 'value')


# BUTTONS

# Create a button to reset filters
def reset_filters(event):
    # Reset the values of the filters
    tempo_slider.value = tempo_plotter.tempo_range
    genre_selector.value = 'All'
    popularity_filter.value = (data['Popularity'].min(), data['Popularity'].max())


reset_button = pn.widgets.Button(
    name="Reset Filters", 
    button_type="danger", 
)
reset_button.on_click(reset_filters)






# LAYOUT SECTION

pn.extension(sizing_mode="stretch_width")



# MAIN LAYOUT

main_layout1 = pn.Column(
    data_table.layout,
    styles={}, sizing_mode="stretch_width"  
)
main_layout2 = pn.Column(
    Scatter_Plotter.layout,
    duration_plotter.layout,
    tempo_plotter.layout,
    Heatmap_Plotter.layout,
    styles={}, sizing_mode="stretch_width"
)
main_layout3 = pn.Column(
    Bar_plotter.layout,
    Pie_chart.layout,
    styles={}, sizing_mode="stretch_width"
)

# Create the template 
template = pn.template.FastListTemplate(
    site="SPOTIFY",
    title='Dashboard APP',
    header_color="#1DB954",
    header_background=background_color,  
    main=[main_layout1, main_layout2, main_layout3],
    logo=logo_url,
    
)


# SIDEBAR

template.sidebar.append(pn.pane.HTML('##  In the Exploratory Data Analysis (EDA) dashboard, you can provide a brief description of the purpose of the dashboard, the data being explored, and any insights or analysis that users can gain from it.'))
# Add the reset button to the sidebar
template.sidebar.append(pn.Column("<h2>Reset Filters</h2>", reset_button))
# Add the tempo slider to the sidebar
template.sidebar.append(pn.Column("<h2>Tempo Slider</h2>", tempo_slider))
# Add the CategorySelector to the sidebar
template.sidebar.append(pn.Column("<h2>Genre Selector</h2>", genre_selector))
template.sidebar.append(pn.Column("<h2>Popularity Filter</h2>", popularity_filter))
 

# NAVIGATION BAR

# Create tabs for navigation
tabs = pn.Tabs(
    ("Table", main_layout1),
    ("Explanatory Data Analysis for Numerical Data", main_layout2),
    ("Explanatory Data Analysis for Categorical Data", main_layout3),

)
template.main[:] = [tabs]

# Display the template
template.servable()