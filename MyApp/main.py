import panel as pn

# Read HTML content from the file
with open("index.html", "r") as html_file:
    html_content = html_file.read()

# Create a Panel app with HTML content
homepage = pn.pane.HTML(html_content, sizing_mode='stretch_width')

# Serve the Panel app
pn.serve(homepage, title='Spotify Dashboard ')
