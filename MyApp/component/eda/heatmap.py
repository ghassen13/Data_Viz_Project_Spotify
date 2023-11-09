import panel as pn
import pandas as pd
import holoviews as hv
import hvplot.pandas

class HeatmapPlotter:
    def __init__(self, data):
        self.data = data
        self.filtered_data = data.copy()

        # Create filter options
        filter_options = list(self.data.columns)
        self.filter_selector = pn.widgets.Select(name='Select Filter', options=filter_options, value=filter_options[0])

        # Create an empty plot to be updated later
        self.heatmap_pane = pn.pane.HoloViews()

        # Combine the Heatmap and Selector using Panel
        self.layout = pn.Column(
            pn.Row(self.filter_selector),
            pn.Row(self.heatmap_pane)
        )

        # Register callback for widget changes
        self.filter_selector.param.watch(self._create_heatmap, 'value')

        # Initial heatmap
        self._create_heatmap()

    def _create_heatmap(self, event=None):
        filter_value = self.filter_selector.value

        # Select only numeric columns
        numeric_data = self.filtered_data.select_dtypes(include='number')

        # Compute the correlation matrix
        correlation_matrix = numeric_data.corr()

        # Multiply the correlation values by 100 to get percentages
        correlation_matrix_percentage = correlation_matrix * 100

        # Use hvplot to create the Heatmap
        heatmap = correlation_matrix_percentage.hvplot.heatmap(
            cmap='viridis',
            colorbar=True,
            title=f'Correlation Matrix Heatmap',
            sizing_mode='stretch_width',
            height=500,
            xticks=None,
            yticks=None,
            fmt="%.0f%%",
            cmap_limits=(correlation_matrix_percentage.min().min(), correlation_matrix_percentage.max().max())
        )

        # Update the existing HoloViews pane with the new heatmap
        self.heatmap_pane.object = heatmap
