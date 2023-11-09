import pandas as pd
import plotly.express as px
import panel as pn
pn.extension('plotly')

class PieChart:
    def __init__(self, data):
        self.data = data  # Fix the variable name
        self.layout = self._create_dashboard()  # Rename to layout

    def _create_dashboard(self):
        # Groupez les pistes par genre et calculez la popularité moyenne pour chaque genre
        genre_popularity = self.data.groupby('Artists')['Popularity'].mean().reset_index()

        # Triez les genres en fonction de leur popularité moyenne (du plus élevé au plus bas)
        sorted_genre_popularity = genre_popularity.sort_values(by='Popularity', ascending=False)

        # Sélectionnez les 10 genres les plus populaires
        top_10_genres = sorted_genre_popularity.head(10)

        # Créez un Donut Chart avec Plotly Express
        fig = px.pie(top_10_genres, names='Artists', values='Popularity', hole=0.3, title='Artistes les plus populaires')
        fig.update_traces(textinfo='percent+label')

        # Créez un widget Panel pour afficher le graphique Plotly
        donut_chart = pn.pane.Plotly(fig)

        return donut_chart