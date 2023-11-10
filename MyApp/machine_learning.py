import panel as pn
from panel.template import FastListTemplate

from component.ML.classification import XGBoostApp
from component.ML.clustering import KMeansApp
from component.ML.regession import RandomRorest

from Data.data_loader import preProcessed_data
data = preProcessed_data



xgboost_app = XGBoostApp(data)
kmeans_sidebar, KMeans_App, reset_kmeans_filters = KMeansApp(data)
Rm_sidebar, RandomRorest_App, reset_Rm_filters = RandomRorest(data)



# Set the background color
background_color = "#000000"  # black color
logo_url = "logo-removebg-preview.png"

pn.extension(sizing_mode="stretch_width")





# Main Layouts
main_layout1 = pn.Column(
    xgboost_app.layout,
    styles={}, sizing_mode="stretch_width"
)

main_layout2 = pn.Column(
    KMeans_App,
    styles={}, sizing_mode="stretch_width"
)

main_layout3 = pn.Column(
    RandomRorest_App,
    styles={}, sizing_mode="stretch_width"
)


# Create the template
template = pn.template.FastListTemplate(
    site="SPOTIFY",
    title='Dashboard App',
    header_color="#1DB954",
    collapsed_sidebar=False,
    header_background=background_color,
    sidebar_width=330,
    corner_radius=5,  
    main=[main_layout1, main_layout2, main_layout3],
    logo=logo_url,

)

# RESET BUTTON 
def reset_filters(event):
    xgboost_app.reset_filters(),
    reset_Rm_filters,
    reset_kmeans_filters,

# Create the refresh button for XGBoostApp
refresh_button = pn.widgets.Button(name="Refresh Filters", button_type="primary")
refresh_button.on_click(reset_filters)


# Create a column of widgets for the XGBoost app
xgboost_sidebar_widgets = pn.Column(
    pn.pane.Markdown('## Set-up XGBoost Parameters : '),
    xgboost_app.booster, xgboost_app.n_trees, xgboost_app.max_depth
)


# Add the columns to the sidebar
template.sidebar.extend([refresh_button, xgboost_sidebar_widgets, kmeans_sidebar, Rm_sidebar])
# NAVIGATION BAR

# Create tabs for navigation
tabs = pn.Tabs(
    ("Classification Models", main_layout1),
    ("Clustering Models", main_layout2),
    ("Regression Models", main_layout3),
)
 


template.main[:] = [tabs]


template.servable()