import panel as pn
import holoviews as hv

pn.extension(sizing_mode="stretch_width")

class ScatterPlotter:
    def __init__(self, data):
        self.data = data
        self.filtered_data = data.copy()

        # Filter the top 10 genres based on popularity
        self.top_genres = self.data.groupby('Track Genre')['Popularity'].mean().nlargest(14).index.tolist()
        self.filtered_data = self.data[self.data['Track Genre'].isin(self.top_genres)]

        filter_attributes = list(data.drop(['Track ID', 'Key', 'Mode', 'Explicit', 'Artists', 'Album Name', 'Track Name', 'Track Genre'], axis=1))

        # Create selectors for filtering by track genre, x-axis, and y-axis
        self.genre_selector = pn.widgets.Select(name='Select Genre', options=['All'] + sorted(self.filtered_data['Track Genre'].unique()))
        self.x_axis_selector = pn.widgets.Select(
            name='Select X-axis',
            options=sorted(filter_attributes),
            value="Tempo"
        )
        self.y_axis_selector = pn.widgets.Select(
            name='Select Y-axis',
            options=sorted(filter_attributes),
            value="Loudness"
        )

        # Use pn.bind to dynamically update the plot based on widget changes
        self.plot = pn.bind(self._create_plot, self.x_axis_selector, self.y_axis_selector, self.genre_selector)

        # Combine the Plot and Selector using Panel
        self.layout = pn.Column(
            pn.Row(self.genre_selector, self.x_axis_selector, self.y_axis_selector),
            pn.Row(self.plot)
        )

    def _create_plot(self, x_axis, y_axis, genre):
        selected_genres = genre

        if 'All' in selected_genres:
            filtered_data = self.data.copy()
        else:
            filtered_data = self.data[self.data['Track Genre'].isin(selected_genres)]

        # Use hvplot to create the initial scatterplot without the legend
        plot = filtered_data.hvplot.scatter(
            x=x_axis,
            y=y_axis,
            by='Track Genre',  # Color points by genre
            cmap='Category20',
            legend='top_right',  # Position the legend
            height=700,
            #width=1200,
            sizing_mode="stretch_width",
            title=f'{x_axis} vs {y_axis} Distribution'
        )

        # Modify the legend to only include selected genres
        if isinstance(plot, hv.core.overlay.NdOverlay):
            for genre in selected_genres:
                if genre in plot.keys():
                    continue
                plot.pop(genre)

        return plot
