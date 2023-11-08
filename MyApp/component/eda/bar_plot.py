import panel as pn
import pandas as pd

class BarPlotter:
    def __init__(self, data):
        self.data = data
        self.filtered_data = data.copy()

        # Create filter options
        filter_options = list(self.data[["Album Name", "Track Name", "Track Genre", 'Artists']])
        self.filter_selector = pn.widgets.Select(name='Select Filter', options=filter_options, value=filter_options[0])

        # Use pn.bind to dynamically update the plot based on widget changes
        self.plot = pn.bind(self._create_plot, self.filter_selector)

        # Combine the Plot and Selector using Panel
        self.layout = pn.Column(
            pn.Row(self.filter_selector),
            pn.Row(self.plot)
        )

    @pn.depends('filter_selector.value')
    def _create_plot(self, filter_value):
        if filter_value not in self.data.columns:
            return None  # Handle the case where the selected column doesn't exist

        # Get the top 10 values for the selected column based on popularity
        top_values = self.data.groupby(filter_value)['Popularity'].mean().nlargest(10).index.tolist()

        # Filter the data for the top 10 values
        filtered_data_top10 = self.data[self.data[filter_value].isin(top_values)]

        # Use hvplot to create the Barplot
        bar_plot = filtered_data_top10.hvplot.bar(
            x=filter_value,
            y="Popularity",
            xlabel="",
            ylabel="Popularity",
            title=f'Top 10 Popularity by {filter_value}',
            rot=45,
            height=500,
            width=800
        )

        return bar_plot