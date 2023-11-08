import sys
sys.path.append('D:/Master BDIA - M2/Data_Viz_Project/MyApp')

import plotly.express as px
#from Data.data_loader import load_data
from Data.data_loader import preProcessed_data
import matplotlib.pyplot as plt
import seaborn as sns
import panel as pn
import hvplot.pandas

data = preProcessed_data

def data_show():
    # Create a panel layout
    layout = pn.Column()
    # Afficher la DataFrame
    data_display = pn.panel(data.head())
    layout.append(data_display)
    return layout

def plot_popularity_analysis():
    layout = pn.Column()
    plt.figure(figsize=(16, 8))
    sns.histplot(data['popularity'], bins=20, kde=True)
    plt.title('Popularity Distribution')
    plt.xlabel('Popularity')
    plt.ylabel('Frequency')
    popularity_plot =  pn.pane.Matplotlib(plt.gcf(), width=750)
    layout.append(popularity_plot)
    return layout

def plot_duration_analysis():
    layout = pn.Column()
    plt.figure(figsize=(16, 8))
    sns.histplot(data['duration_ms'] / 60000, bins=20, kde=True)
    plt.title('Song Duration Distribution')
    plt.xlabel('Duration (minutes)')
    plt.ylabel('Frequency')
    duration_plot  = pn.pane.Matplotlib(plt.gcf(), width=750)
    layout.append(duration_plot)
    return layout

def plot_energy_danceability():
    layout = pn.Column()
    plt.figure(figsize=(16, 8))
    sns.scatterplot(x='energy', y='danceability', data=data)
    plt.title('Energy vs Danceability')
    plt.xlabel('Energy')
    plt.ylabel('Danceability')
    enrgyDanceability_plot = pn.pane.Matplotlib(plt.gcf(), width=750)
    layout.append(enrgyDanceability_plot)
    return layout

def plot_energy_loudness():
    layout = pn.Column()
    plt.figure(figsize=(16, 8))
    sns.scatterplot(x='energy', y='loudness', data=data)
    plt.title('Energy vs Loudness')
    plt.xlabel('Energy')
    plt.ylabel('Loudness')
    enrgyLoudness_plot = pn.pane.Matplotlib(plt.gcf(), width=750)
    layout.append(enrgyLoudness_plot)
    return layout

def plot_tempo():
    layout = pn.Column()
    plt.figure(figsize=(16, 8))
    sns.histplot(data['tempo'], bins=20, kde=True)
    plt.title('Tempo Distribution')
    plt.xlabel('Tempo')
    plt.ylabel('Frequency')

    tempo_plot = pn.pane.Matplotlib(plt.gcf(), width=950)
    layout.append(tempo_plot)
    return layout
