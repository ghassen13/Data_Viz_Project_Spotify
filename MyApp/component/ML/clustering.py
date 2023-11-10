import sys
sys.path.append("D:\Master BDIA - M2\Data_Viz_Project\MyApp")

import panel as pn
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import silhouette_score
from Data.data_loader import preProcessed_data



data = preProcessed_data

df = data.drop(['Artists', 'Album Name', 'Track Name'], axis=1)


pn.extension(sizing_mode="stretch_width", design='material', template="fast")

pn.state.template.param.update(title="K-Means Clustering Example")

n_clusters = pn.widgets.IntSlider(start=2, end=10, name="Number of Clusters")

X = df.drop('Track Genre', axis=1)
# Encode categorical columns if any
categorical_columns = X.select_dtypes(include=['object']).columns
encoder = LabelEncoder()
X[categorical_columns] = X[categorical_columns].apply(encoder.fit_transform)


# K-Means est un algorithme de clustering non supervisé, donc nous n'avons pas besoin d'une variable cible (y).

def pipeline(n_clusters):
    model = KMeans(n_clusters=n_clusters, n_init =10, random_state=0)
    y_pred = model.fit_predict(X)
    silhouette_avg = silhouette_score(X, y_pred)
    return pn.indicators.Number(
        name=f"Silhouette Score",
        value=silhouette_avg,
        format="{value}",
        align='center'
    )

pn.Row(
    pn.Column(n_clusters, width=320).servable(area='sidebar'),
    pn.Column(
        "Example of applying K-Means clustering using your dataset (df).",
        "Adjust the number of clusters to run K-Means clustering. The silhouette score will adjust accordingly.",
        pn.bind(pipeline, n_clusters),
        pn.bind(lambda n_clusters: f'# <code>{n_clusters=}</code>', n_clusters),
    ).servable(),
)