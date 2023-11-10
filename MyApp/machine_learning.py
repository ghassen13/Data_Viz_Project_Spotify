import panel as pn

from component.ML.classification import XGBoostApp
from component.ML.classification_svm import SVMApp

from Data.data_loader import preProcessed_data
data = preProcessed_data



xgboost_app = XGBoostApp(data)
SVM_app = SVMApp(data)


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
    SVM_app.layout,
      styles={}, sizing_mode="stretch_width"
)

# Create the template
template = pn.template.FastListTemplate(
    site="SPOTIFY",
    title='Dashboard APP',
    header_color="#1DB954",
    collapsed_sidebar=False,
    header_background=background_color,
    sidebar_width=330,
    corner_radius=5,  
    main=[main_layout1, main_layout2],
    logo=logo_url,

)


# Create a column of widgets
sidebar_widgets = pn.Column(
    pn.pane.Markdown('Set up XGBoost Parameters : '),
    xgboost_app.booster, xgboost_app.n_trees, xgboost_app.max_depth
    )

# Add the column to the sidebar
template.sidebar.append(sidebar_widgets)

# NAVIGATION BAR

# Create tabs for navigation
tabs = pn.Tabs(
    ("Classification Models", main_layout1),
    ("Regression Models", main_layout2),
)
 


template.main[:] = [tabs]


template.servable()