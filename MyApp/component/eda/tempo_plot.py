import sys
sys.path.append('D:/Master BDIA - M2/Data_Viz_Project/MyApp')

#from Data.data_loader import load_data
from Data.data_loader import preProcessed_data
import panel as pn
import hvplot.pandas


data = preProcessed_data

class TempoPlotter:
    def __init__(self, data):
        self.data = data
        self.tempo_range = (0, 250)

        # Create initial plot
        self.tempo_plot = self._create_plot()

        # Combine the plot using Panel
        self.layout = pn.Column(self.tempo_plot)

    def _create_plot(self):
        filtered_data = self.data[(self.data['Tempo'] >= self.tempo_range[0]) & (self.data['Tempo'] <= self.tempo_range[1])]
        tempo_plot = filtered_data.hvplot.hist(
            y='Tempo', 
            bins=20, 
            kde=True, 
            height=500, 
            width=1200, 
            title='Tempo Distribution')
        return tempo_plot
    
    def _handle_zoom(self, plot, element):
        x_range = plot.handles['x_range']
        self.tempo_range = (x_range.start, x_range.end)

        # Update the plot using the new tempo range
        self._update_plot()

    def update_plot(self, event):
        self.tempo_range = event.new
        filtered_data = self.data[(self.data['Tempo'] >= self.tempo_range[0]) & (self.data['Tempo'] <= self.tempo_range[1])]

        # Recreate the plot using hvplot
        new_plot = filtered_data.hvplot.hist(y='Tempo', bins=20, kde=True, height=500, width=800, title='Tempo Distribution')

        # Update the layout with the new plot
        self.layout[0] = new_plot