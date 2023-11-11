# Spotify Track Data Applicaion

## Overview
Spotify Track App is a data application that allows users to explore, analyze, and predict Spotify tracks' data through interactive dashboards. The application is built using FastAPI, Panel, and Bokeh. It provides three dashboards, each offering a unique perspective on the Spotify tracks dataset.

## Requirements 
To run Spotiviz, follow these steps:
1. Create and activate a virtual environment:
   
python -m venv venv
venv/Scripts/activate
3. Install the required packages using the following command:

pip install -r requirements.txt
4. Start the application using Pansel Serve:

Panel serve file.py

## Dashboards : 
Spotify Track App offers the following dashboards:

Home Page: Navigate to the home page to get an overview of the application.

Dashboard 1 - Exploratory Dashboard: Explore the Spotify tracks dataset with various filters and visualizations. Uncover patterns, trends, and details of top songs, artists, and genres.

Access: [http://127.0.0.1:8000/firstdash](http://localhost:5006/eda_dashboard)
Dashboard 2 - Genre Prediction Dashboard: Predict and understand the genre of a track using machine learning models. Interact with predictions and discover the magic behind the music.
            - Clustering problem : Clustering aims to bring together the most similar genres for reasons such as a recommendation system.

Access: [http://127.0.0.1:8000/seconddash](http://localhost:5006/machine_learning)
Dashboard 3 - Further Analysis: For those who crave more, this dashboard provides a space for additional insights, allowing you to explore fascinating aspects of the dataset that go beyond genre prediction.

Access: [http://127.0.0.1:8000/seconddash](http://localhost:5006/further_analysis)
