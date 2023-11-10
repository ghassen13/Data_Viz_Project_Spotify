import panel as pn
import pandas as pd

pn.extension(sizing_mode='stretch_width')
plot_opts = dict(
    responsive=True, min_height=400,
    # Align the curves' color with the template's color
    color=pn.template.FastListTemplate.accent_base_color
)

class BarPlotter:
    def __init__(self, data):
        self.data = data
        self.filtered_data = data.copy()

        # Create filter options
        filter_options = list(self.data[["Album Name", "Track Name", "Track Genre", 'Artists']])
        self.filter_selector = pn.widgets.Select(name='Select Filter', options=filter_options, value=filter_options[3])

        # Initialize an empty plot using HoloViews
        self.bar_plot_pane = pn.pane.HoloViews()

        # Combine the Plot and Selector using Panel
        self.layout = pn.Column(
            pn.Row(self.filter_selector),
            pn.Row(self.bar_plot_pane, sizing_mode='stretch_width')
        )

        # Register callback for widget changes
        self.filter_selector.param.watch(self._update_plot, 'value')

        # Initial plot
        self._update_plot()

    def _create_plot(self):
        filter_value = self.filter_selector.value

        if filter_value not in self.data.columns:
            return None  # Handle the case where the selected column doesn't exist

        # Get the top 10 values for the selected column based on popularity
        top_values = self.data.groupby(filter_value)['Popularity'].mean().nlargest(15).index.tolist()

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
            height=700,
            #width=1250,
            **plot_opts,
            sizing_mode='stretch_width'
        )

        return bar_plot

    def _update_plot(self, event=None):
        # Triggered when the filter_selector value changes
        bar_plot = self._create_plot()

        # Update the Pane with the new plot
        self.bar_plot_pane.object = bar_plot