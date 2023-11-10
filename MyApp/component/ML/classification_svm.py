import panel as pn
from sklearn import svm
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix
import hvplot.pandas

pn.extension(sizing_mode="stretch_width", design='material', template="fast")

class SVMApp:
    def __init__(self, data):
        self.data = data
        self.df = self.preprocess_data()

        # Set up Panel widgets
        self.kernel_input = pn.widgets.Select(name='Kernel', options=['linear', 'poly', 'rbf', 'sigmoid'], value='linear')
        self.C_input = pn.widgets.FloatSlider(name='C', start=0.1, end=10.0, value=1.0, step=0.1)

        # Set up SVM model
        self.X = self.df.drop('Track Genre', axis=1)
        self.y = self.df['Track Genre']
        self.encoder = LabelEncoder()
        self.y_encoded = self.encoder.fit_transform(self.y)

        # Set up the layout
        self.layout = pn.Row(
            pn.Column(
                "Support Vector Machine classification model.",
                self.X.head(),
                pn.bind(self.pipeline, self.kernel_input, self.C_input),
                pn.bind(lambda kernel, C: f'# <code>{kernel=} | {C=}</code>', self.kernel_input, self.C_input),
            ),
            sizing_mode="stretch_width"
        )

    def preprocess_data(self):
        # Drop columns that are not suitable for training
        df = self.data.drop(['Track ID', 'Artists', 'Album Name', 'Track Name'], axis=1)
        return df

    def pipeline(self, kernel, C):
        model = svm.SVC(kernel=kernel, C=C)
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


