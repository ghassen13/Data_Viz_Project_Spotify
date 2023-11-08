import panel as pn
import hvplot.pandas 

class DurationPlotter:
    def __init__(self, data):
        self.data = data
        self.filtered_data = data.copy()

        # Create a blank plot
        self.plot = self._create_plot()

        # Combine the Plot and Selector using Panel 
        self.layout = pn.Column(self.plot)

    def _create_plot(self):
        # Use hvplot to create the initial plot
        return self.data.groupby('Track Genre')['Duration (ms)'].mean().hvplot.line(
            xlabel='Track Genre', 
            ylabel='Average Duration (ms)', 
            height=500, 
            width=1200,  # Set the width policy to 'max_width'
            sizing_mode='stretch_width', 
            title='Average Track Duration by Genre'
        )

    def _update_plot(self, event):
        selected_genre = event.new

        if selected_genre == 'All':
            self.filtered_data = self.data.copy()
        else:
            self.filtered_data = self.data[self.data['Track Genre'] == selected_genre]

        # Update the plot with the filtered data
        self.plot.data = self.filtered_data.groupby('Track Genre')['Duration (ms)'].mean().hvplot.line(
            xlabel='Track Genre', 
            ylabel='Average Duration (ms)', 
            width=1200,  # Set the width policy to 'max_width'
            sizing_mode='stretch_width'
        )