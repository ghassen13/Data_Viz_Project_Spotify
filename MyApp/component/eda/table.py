import panel as pn

class DataTable:
    def __init__(self, data):
        self.data = data
        self.filtered_data = data.copy()

        # Create a Tabulator widget for displaying the DataFrame
        self.data_table = pn.widgets.DataFrame(self.filtered_data, height=500, sizing_mode='stretch_width')

        # Create a CategorySelector for filtering by track genre
        self.genre_selector = pn.widgets.Select(name='Select Genre', options=['All'] + sorted(self.filtered_data['Track Genre'].unique()))
        self.genre_selector.param.watch(self._update_table, 'value')

        # Initialize describe pane with the initial data
        self.describe_pane = self.create_describe_pane()

        # Combine the Table, Selector, and Describe Pane using Panel
        self.layout = pn.Column(
            pn.pane.HTML("<h2>Data Table</h2>"),
            self.genre_selector,
            self.data_table,
            pn.Spacer(height=40),
            pn.pane.HTML("<h2>Data Table</h2>"),
            self.describe_pane
        )

    def _update_table(self, event):
        selected_genre = event.new

        if selected_genre == 'All':
            self.filtered_data = self.data.copy()
        else:
            self.filtered_data = self.data[self.data['Track Genre'] == selected_genre]

        # Update the Table with the filtered data
        self.data_table.value = self.filtered_data

        # Update the Describe Pane with the new data.describe()
        self.describe_pane.object = self.filtered_data.describe().to_string()

    def create_describe_pane(self):
        # Create a new DataFrame widget for the describe pane
        describe_pane = pn.widgets.DataFrame(self.filtered_data.describe(), height=500, sizing_mode='stretch_width')
        return describe_pane