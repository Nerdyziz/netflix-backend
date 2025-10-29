from flask import Flask, jsonify
from flask_cors import CORS
import io
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

app = Flask(__name__)
CORS(app)

# Load dataset
df = pd.read_csv("netflix_titles.csv")

# Clean up
df['country'] = df['country'].fillna('Unknown')
df['director'] = df['director'].fillna('Unknown')
df['cast'] = df['cast'].fillna('Unknown')
df['rating'] = df['rating'].fillna('Unknown')
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
df['duration_num'] = df['duration'].str.extract(r'(\d+)').astype(float)
df['duration_type'] = np.where(df['duration'].str.contains('Season', case=False, na=False), 'Seasons', 'Minutes')

# Helper function to convert matplotlib figure → Base64
def fig_to_base64():
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close()
    return base64.b64encode(buf.getvalue()).decode('utf-8')

@app.route('/plot/type')
def plot_type_distribution():
    plt.figure(figsize=(6,4))
    sns.countplot(data=df, x='type', hue='type', palette='Set2', legend=False)
    plt.title('Movies vs TV Shows on Netflix')
    return jsonify({'image': fig_to_base64()})

@app.route('/plot/countries')
def plot_top_countries():
    plt.figure(figsize=(10,5))
    country_counts = df['country'].value_counts().head(10)
    sns.barplot(y=country_counts.index, x=country_counts.values, hue=country_counts.index,
                palette='coolwarm', legend=False)
    plt.title('Top 10 Content-Producing Countries')
    plt.xlabel('Number of Titles')
    plt.ylabel('Country')
    return jsonify({'image': fig_to_base64()})

@app.route('/plot/release_trend')
def plot_release_trend():
    yearly_counts = df['release_year'].value_counts().sort_index()
    plt.figure(figsize=(12,5))
    sns.lineplot(x=yearly_counts.index, y=yearly_counts.values, marker='o', color='steelblue')
    plt.title('Number of Releases Over the Years')
    plt.xlabel('Release Year')
    plt.ylabel('Number of Titles')
    return jsonify({'image': fig_to_base64()})

@app.route('/plot/genres')
def plot_genre_distribution():
    genres = df['listed_in'].str.split(', ').explode().value_counts().head(15)
    plt.figure(figsize=(10,5))
    sns.barplot(y=genres.index, x=genres.values, hue=genres.index, palette='magma', legend=False)
    plt.title('Top 15 Genres on Netflix')
    plt.xlabel('Number of Titles')
    plt.ylabel('Genre')
    return jsonify({'image': fig_to_base64()})

@app.route('/plot/ratings')
def plot_rating_distribution():
    plt.figure(figsize=(8,4))
    sns.countplot(data=df, x='rating', hue='rating',
                  order=df['rating'].value_counts().index,
                  palette='viridis', legend=False)
    plt.title('Distribution of Ratings')
    plt.xticks(rotation=45)
    return jsonify({'image': fig_to_base64()})

@app.route('/plot/duration')
def average_duration_analysis():
    avg_movie = df[df['type']=='Movie']['duration_num'].mean()
    avg_show = df[df['type']=='TV Show']['duration_num'].mean()
    plt.figure(figsize=(5,4))
    sns.barplot(x=['Movies (min)', 'TV Shows (seasons)'], y=[avg_movie, avg_show], palette='Set1')
    plt.title('Average Duration Comparison')
    return jsonify({'image': fig_to_base64()})

@app.route('/plot/directors')
def top_directors():
    top_dir = df[df['director'] != 'Unknown']['director'].value_counts().head(10)
    plt.figure(figsize=(10,5))
    sns.barplot(y=top_dir.index, x=top_dir.values, hue=top_dir.index, palette='cubehelix', legend=False)
    plt.title('Top 10 Directors by Number of Titles')
    plt.xlabel('Number of Titles')
    plt.ylabel('Director')
    return jsonify({'image': fig_to_base64()})


if __name__ == '__main__':
    app.run(debug=True)
