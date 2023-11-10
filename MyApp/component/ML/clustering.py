import sys
sys.path.append("D:\Master BDIA - M2\Data_Viz_Project\MyApp")

import panel as pn
import pandas as pd
import hvplot.pandas
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import silhouette_score,silhouette_samples
from Data.data_loader import preProcessed_data

plot_opts = dict(
    responsive=True, min_height=400,
)

def KMeansApp(data):
    data = preProcessed_data[:4000]

    df = data.drop(['Artists', 'Album Name', 'Track Name'], axis=1)

    pn.extension(sizing_mode="stretch_width")


    n_clusters = pn.widgets.IntSlider(start=2, end=15, name="Number of Clusters")

    initial_features = list(df.columns[:-1])

    x_feature_selector = pn.widgets.Select(name='Select X-Axis Feature:', options=initial_features, value=initial_features[1])
    y_feature_selector = pn.widgets.Select(name='Select Y-Axis Feature:', options=initial_features, value=initial_features[2])

    X = df.drop('Track Genre', axis=1)
    categorical_columns = X.select_dtypes(include=['object']).columns
    encoder = LabelEncoder()
    X[categorical_columns] = X[categorical_columns].apply(encoder.fit_transform)

    def reset_filters():
        # Reset filters for KMeansApp
        n_clusters.value = 2
        x_feature_selector.value = initial_features[1]
        y_feature_selector.value = initial_features[2]


    def pipeline(n_clusters, x_feature, y_feature):
        model = KMeans(n_clusters=n_clusters, n_init=10, random_state=0)
        y_pred = model.fit_predict(X)
        silhouette_avg = silhouette_score(X, y_pred)

        sample_silhouette_values = silhouette_samples(X, y_pred)

        silhouette_plot = pd.DataFrame({
            'Silhouette Coefficient': sample_silhouette_values,
            'Cluster label': y_pred
        }).hvplot.scatter(
            x='Cluster label',
            y='Silhouette Coefficient',
            c='Cluster label',
            cmap='nipy_spectral',
            height=600,
            #width=1000,
            **plot_opts,
            sizing_mode="stretch_width",
            title="Silhouette Plot for K-Means Clustering"
        )

        percentage_pane = pn.indicators.Number(
            name=f"Silhouette Score",
            value=silhouette_avg,
            format="{value:.2%}",
            align='center',
            sizing_mode="fixed",
            colors=[(97.5, "red"), (99.0, "orange"), (100, "green")]            
        )

        scatter_plot = pd.DataFrame({
            'X-Axis Feature': X[x_feature],
            'Y-Axis Feature': X[y_feature],
            'Cluster label': y_pred
        }).hvplot.scatter(
            x='X-Axis Feature',
            y='Y-Axis Feature',
            c='Cluster label',
            cmap='nipy_spectral',
            title=f"Scatter Plot with Cluster Labels (X-Axis: {x_feature}, Y-Axis: {y_feature})",
            height=600,
            #width=1200,
            **plot_opts, 
            sizing_mode="stretch_width",
            hover_cols=['Cluster label'],
            legend='bottom_right',  
        )

        return pn.Column(
            pn.Row(percentage_pane, silhouette_plot),
            pn.Row(scatter_plot)
        )
    

    # Only include the pipeline in the main layout, excluding filter widgets
    main_layout = pn.Column(
        "# KMeans Model.",
        "### Adjust your model parameters to get better results !",
        pn.bind(lambda n_clusters, x_feature, y_feature: f'# <code>{n_clusters=}, {x_feature=}, {y_feature=}</code>',
            n_clusters, x_feature_selector, y_feature_selector),
        pn.bind(pipeline, n_clusters, x_feature_selector, y_feature_selector)

    )

    # Create a column of widgets for the KMeans app in the sidebar
    kmeans_sidebar_widgets = pn.Column(
        pn.pane.Markdown('## Set-up KMeans parameters :'),
        n_clusters,
        x_feature_selector,
        y_feature_selector,
    )
    reset_params = reset_filters()
    # Return filter widgets and main layout separately
    return kmeans_sidebar_widgets, main_layout, reset_params