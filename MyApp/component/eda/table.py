import panel as pn
import pandas as pd


class DataTable:
    def __init__(self, data):
        self.data = data
        self.filtered_data = data.copy()
        

        # Create a Table for displaying the DataFrame
        self.data_table = pn.widgets.Tabulator(self.filtered_data, height=500,sizing_mode='stretch_width')
        
        # Create a CategorySelector for filtering by track genre
        self.genre_selector = pn.widgets.Select(name='Select Genre', options=['All'] + sorted(self.filtered_data['Track Genre'].unique()))
        self.genre_selector.param.watch(self._update_table, 'value')
        
        # Combine the Table and Selector using Panel
        self.layout = pn.Column(self.genre_selector, self.data_table)

    def _update_table(self, event):
        selected_genre = event.new

        if selected_genre == 'All':
            self.filtered_data = self.data.copy()
        else:
            self.filtered_data = self.data[self.data['Track Genre'] == selected_genre]

        # Update the Table with the filtered data
        self.data_table.value = self.filtered_data
