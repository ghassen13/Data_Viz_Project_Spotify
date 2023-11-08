import panel as pn
import hvplot.pandas 

class DurationPlotter:
    def __init__(self, data):
        self.data = data
        self.filtered_data = data.copy()

        # Specify the columns you want in the filter widget
        filter_attributes = list(data.drop(['Track ID', 'Artists', 'Album Name', 'Track Name', 'Track Genre', 'Time Signature', 'Key', 'Mode', 'Explicit','Duration (ms)'], axis=1))

        # Create filter widget with specified options
        self.filter_widget = pn.widgets.Select(
            name='Select Attribute for X-axis',
            options=filter_attributes,
            value="Tempo"
        )

        # Combine the Plot and Selector using Panel
        self.layout = pn.Column(self.filter_widget, self._create_plot)

        # Use pn.depends to dynamically update the plot based on widget changes
        @pn.depends(value=self.filter_widget.param.value)
        def reactive_plot(value):
            return self._create_plot(value)

        # Display the reactive plot
        self.layout.append(reactive_plot)

    def _create_plot(self, value):
        # Use hvplot to create the initial plot
        return self.data.groupby(value)['Duration (ms)'].mean().hvplot.line(
            xlabel=value,
            ylabel='Average Duration (ms)',
            height=500,
            width=1200,
            sizing_mode='stretch_width',
        )