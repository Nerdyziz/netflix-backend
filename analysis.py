# backend/analysis.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io

# Load dataset
df = pd.read_csv("netflix_titles.csv")
df['country'] = df['country'].fillna('Unknown')
df['director'] = df['director'].fillna('Unknown')
df['cast'] = df['cast'].fillna('Unknown')
df['rating'] = df['rating'].fillna('Unknown')
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
df['decade'] = (df['release_year'] // 10) * 10
df['duration_num'] = df['duration'].str.extract(r'(\d+)').astype(float)
df['duration_type'] = np.where(df['duration'].str.contains('Season', case=False, na=False), 'Seasons', 'Minutes')

sns.set(style="whitegrid")

def save_plot():
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    plt.close()
    buffer.seek(0)
    return buffer

def netflix_analysis_menu(choice):
    if choice == 1:
        return df.info().__str__()
    
    elif choice == 2:
        plt.figure(figsize=(6,4))
        sns.countplot(data=df, x='type', hue='type', palette='Set2', legend=False)
        plt.title('Movies vs TV Shows')
        return save_plot()
    
    elif choice == 3:
        plt.figure(figsize=(10,5))
        country_counts = df['country'].value_counts().head(10)
        sns.barplot(y=country_counts.index, x=country_counts.values, hue=country_counts.index, palette='coolwarm', legend=False)
        plt.title('Top 10 Countries by Content')
        return save_plot()

    elif choice == 4:
        yearly_counts = df['release_year'].value_counts().sort_index()
        plt.figure(figsize=(12,5))
        sns.lineplot(x=yearly_counts.index, y=yearly_counts.values, marker='o', color='steelblue')
        plt.title('Release Trend Over the Years')
        return save_plot()

    elif choice == 5:
        genres = df['listed_in'].str.split(', ').explode().value_counts().head(15)
        plt.figure(figsize=(10,5))
        sns.barplot(y=genres.index, x=genres.values, hue=genres.index, palette='magma', legend=False)
        plt.title('Top 15 Genres')
        return save_plot()

    elif choice == 6:
        plt.figure(figsize=(8,4))
        sns.countplot(data=df, x='rating', hue='rating', order=df['rating'].value_counts().index, palette='viridis', legend=False)
        plt.title('Ratings Distribution')
        plt.xticks(rotation=45)
        return save_plot()

    elif choice == 7:
        avg_movie = df[df['type']=='Movie']['duration_num'].mean()
        avg_show = df[df['type']=='TV Show']['duration_num'].mean()
        return f"🎥 Avg Movie Duration: {avg_movie:.2f} mins | 📺 Avg TV Show Seasons: {avg_show:.2f}"
    
    else:
        return "❌ Invalid choice"
