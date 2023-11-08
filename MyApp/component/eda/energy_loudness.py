import panel as pn

class EnergyLoudnessPlotter:
    def __init__(self, data):
        self.data = data
        self.filtered_data = data.copy()

        # Filter the top 10 genres based on popularity
        self.top_genres = self.data.groupby('Track Genre')['Popularity'].mean().nlargest(14).index.tolist()
        self.filtered_data = self.data[self.data['Track Genre'].isin(self.top_genres)]

        # Create a legend filter using CheckboxGroup
        self.legend_filter = pn.widgets.CheckBoxGroup(name='Legend Filter', options=self.top_genres, value=self.top_genres)
        self.legend_filter.param.watch(self._update_legend, 'value')

        # Create a blank scatterplot
        self.plot = self._create_plot()

        # Combine the Scatterplot, Legend Filter, and Selector using Panel
        self.layout = pn.Column(self.plot, self.legend_filter)

        # Watch the value attribute of the legend filter and call _update_plot when it changes
        self.legend_filter.param.watch(self._update_plot, 'value')

    def _create_plot(self):
        # Use hvplot to create the initial scatterplot
        return self.filtered_data.hvplot.scatter(
            x='Energy', 
            y='Loudness', 
            c='Track Genre', 
            cmap='Category20', 
            legend='top_right', 
            legend_position='right',
            height=500, 
            width=1200, 
            title='Energy vs Loudness Distribution'
        )

    def _update_legend(self, event):
        selected_genres = event.new

        if 'All' in selected_genres:
            self.filtered_data = self.data.copy()
        else:
            self.filtered_data = self.data[self.data['Track Genre'].isin(selected_genres)]

        # Update the scatterplot with the filtered data
        self.plot.data = self.filtered_data.hvplot.scatter(
            x='Energy', 
            y='Loudness', 
            c='Track Genre', 
            cmap='Category20', 
            legend='top_right',
            legend_position='right'
        )

    def _update_plot(self, event):
        selected_genres = self.legend_filter.value

        if 'All' in selected_genres:
            self.filtered_data = self.data.copy()
        else:
            self.filtered_data = self.data[self.data['Track Genre'].isin(selected_genres)]

        # Update the scatterplot with the filtered data
        self.plot.data = self.filtered_data.hvplot.scatter(
            x='Energy', 
            y='Loudness', 
            c='Track Genre', 
            cmap='Category20', 
            legend='top_right',
            legend_position='right'
        )