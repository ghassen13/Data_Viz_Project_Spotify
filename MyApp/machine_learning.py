import panel as pn


# Set the background color
background_color = "#000000"  # black color



pn.extension(sizing_mode="stretch_width")

CSS = """
div.card-margin:nth-child(1) {
    max-height: 300px;
}
div.card-margin:nth-child(2) {
    max-height: 400px;
}
"""

# Main Layouts
main_layout1 = pn.Column(
    styles={"background": "red"}, sizing_mode="stretch_both"
      
)

main_layout2 = pn.Column(
      styles={"background": "#1DB954"}, sizing_mode="stretch_both"
)




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
    main=[main_layout1, main_layout2]
)

# Add the tempo slider to the sidebar
template.sidebar.append(pn.pane.Markdown("Hello Forom SidaBar"))

template.servable()
