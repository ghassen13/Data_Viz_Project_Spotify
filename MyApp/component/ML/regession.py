import sys
sys.path.append("D:\Master BDIA - M2\Data_Viz_Project\MyApp")

import panel as pn
import pandas as pd
import hvplot.pandas
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, learning_curve
from sklearn.metrics import r2_score, mean_squared_error
from Data.data_loader import preProcessed_data

plot_opts = dict(
    responsive=True, min_height=400,
)

def RandomRorest(data):
    data = preProcessed_data[:4000]

    df = data.drop(['Artists', 'Album Name', 'Track Name', 'Track ID'], axis=1)

    pn.extension(sizing_mode="stretch_width")

    # Removed the following line as it's not necessary
    # pn.state.template.param.update(title="RandomForest Regression Example")

    # Select features for regression
    features = list(df.columns[:-1])  # Exclude the last column which is the 'Target variable'

    target_variable_selector = pn.widgets.Select(name='Select Target Variable:', options=features, value=features[-1])

    # Get the initial features for the scatter plot
    initial_features = list(df.columns[:-1])  # Exclude the last column which is the 'Target variable'

    x_feature_selector = pn.widgets.Select(name='Select X-Axis Feature:', options=initial_features, value=initial_features[0])

    X = df[initial_features]
    y = df[features[-1]]

    # Encode categorical columns if any
    categorical_columns = X.select_dtypes(include=['object']).columns
    encoder = LabelEncoder()
    X[categorical_columns] = X[categorical_columns].apply(encoder.fit_transform)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    
    # Reset Function
    def reset_filters():
        target_variable_selector.value = features[-1]
        x_feature_selector.value = initial_features[0]
    
    
    def pipeline(target_variable, x_feature):

        # Select the target variable dynamically
        y = df[target_variable]

        # Encode categorical columns if any
        categorical_columns = X.select_dtypes(include=['object']).columns
        encoder = LabelEncoder()
        X[categorical_columns] = X[categorical_columns].apply(encoder.fit_transform)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

        model = RandomForestRegressor(n_estimators=100, random_state=0)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        r2 = r2_score(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)

        # Create a scatter plot to show the predicted values against the actual values
        scatter_plot = pd.DataFrame({
            'Actual Values': y_test,
            'Predicted Values': y_pred
        }).hvplot.scatter(
            x='Actual Values',
            y='Predicted Values',
            title=f"Scatter Plot of Actual vs. Predicted Values",
            height=600,
            **plot_opts, 
            legend='top_right',
        )

        # Display the R-squared and Mean Squared Error
        r2_pane = pn.indicators.Number(
            name=f"R-squared",
            value=r2,
            format="{value:.2%}",
            align='center',
        )

        mse_pane = pn.indicators.Number(
            name=f"Mean Squared Error",
            value=mse,
            align='center',
            format="{value:.2%}", 
        )

        # Feature Importance Plot
        feature_importance_plot = pd.DataFrame({
            'Feature': X_train.columns,
            'Importance': model.feature_importances_
        }).sort_values(by='Importance', ascending=False).hvplot.bar(
            x='Feature',
            y='Importance',
            title='Feature Importance Plot',
            height=600,
            rot=45,
            xlabel='Feature',
            ylabel='Importance',
            color='blue',
            legend=False,
            **plot_opts,
        )

        # Learning Curve Plot
        train_sizes, train_scores, test_scores = learning_curve(
            model, X, y, cv=5, scoring='neg_mean_squared_error', train_sizes=np.linspace(0.1, 1.0, 10)
        )

        learning_curve_df = pd.DataFrame({
            'Training Size': train_sizes,
            'Training Score': -np.mean(train_scores, axis=1),
            'Validation Score': -np.mean(test_scores, axis=1),
        })

        learning_curve_plot = learning_curve_df.hvplot.line(
            x='Training Size',
            y=['Training Score', 'Validation Score'],
            title=f'Learning Curve for Target Variable: {target_variable}',
            height=600,
            xlabel='Training Size',
            ylabel='Mean Squared Error',
            legend='top_left',
            color=['red', 'green'],
            grid=True,
            **plot_opts,
        )

        return pn.Column(
            pn.Row(r2_pane, mse_pane),
            pn.Row(scatter_plot),
            pn.Row(feature_importance_plot),
            pn.Row(learning_curve_plot)
        )

    main_layout = pn.Column(
        "# Random Forest Model.",
        "### Adjust the target variable and select features for the X-Axis to run RandomForest regression. The R-squared, Mean Squared Error, Scatter Plot of Actual vs. Predicted Values, Feature Importance Plot, and Learning Curve will adjust accordingly.",
        pn.bind(lambda target_variable, x_feature: f'# <code>{target_variable=}, {x_feature=}</code>',
                target_variable_selector, x_feature_selector),
        pn.bind(pipeline, target_variable_selector, x_feature_selector),

    )
    # Create a column of widgets for the KMeans app in the sidebar
    Rm_sidebar_widgets = pn.Column(
    pn.pane.Markdown('## Set-up Random Foresrt Model parameters :'),
    target_variable_selector,
    x_feature_selector,
    width=320,
    )
    reset_filter = reset_filters()

    # Return filter widgets and main layout separately
    return Rm_sidebar_widgets, main_layout, reset_filter

