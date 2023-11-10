import numpy as np
import pandas as pd
import panel as pn
from sklearn.metrics import accuracy_score, precision_recall_curve
from xgboost import XGBClassifier
from sklearn.preprocessing import LabelEncoder

pn.extension(sizing_mode="stretch_width", design='material', template="fast")

class XGBoostApp:
    def __init__(self, data):
        self.data = data
        self.df = self.preprocess_data()

        # Set up Panel widgets
        self.n_trees = pn.widgets.IntSlider(start=2, end=100, name="Number of trees")
        self.max_depth = pn.widgets.IntSlider(start=1, end=50, value=2, name="Maximum Depth")
        self.booster = pn.widgets.Select(options=['gbtree', 'gblinear', 'dart'], name="Booster")

        # Set up XGBoost model
        self.X = self.df.drop('Track Genre', axis=1)
        self.y = self.df['Track Genre']
        self.encoder = LabelEncoder()
        self.y_encoded = self.encoder.fit_transform(self.y)

        # Set up the layout
        self.layout = pn.Row(
            pn.Column(
                "XGBoost classification model.",
                self.X.head(),
                pn.bind(self.pipeline, self.n_trees, self.max_depth, self.booster),
                pn.bind(lambda n_trees, max_depth, booster: f'# <code>{n_trees=} | {max_depth=} | {booster=}</code>', self.n_trees, self.max_depth, self.booster),
            ),
            sizing_mode = "stretch_width"
        )

    def preprocess_data(self):
        # Drop columns that are not suitable for training
        df = self.data.drop(['Track ID', 'Artists', 'Album Name', 'Track Name'], axis=1)
        return df

    def pipeline(self, n_trees, max_depth, booster):
        model = XGBClassifier(max_depth=max_depth, n_estimators=n_trees, booster=booster)
        model.fit(self.X, self.y_encoded)
        accuracy = round(accuracy_score(self.y_encoded, model.predict(self.X)) * 100, 1)
        return pn.indicators.Number(
            name=f"Test score",
            value=accuracy,
            format="{value}%",
            colors=[(97.5, "red"), (99.0, "orange"), (100, "green")],
            align='center',
            sizing_mode="stretch_width"
        )
    
 