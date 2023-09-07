import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the cleaned data
df = pd.read_csv('c:/Users/ASUS/Desktop/web scraping/your_cleaned_data.csv')  # Replace with the path to your cleaned data file

# Basic data exploration
print(df.head())  # View the first few rows of the DataFrame
print(df.info())  # Get information about the DataFrame's structure
print(df.describe())  # Get summary statistics

# Data visualization
# Example 1: Create a histogram of IMDb ratings
sns.histplot(df['imdb'], bins=20, kde=True)
plt.xlabel('IMDb Ratings')
plt.ylabel('Frequency')
plt.title('Distribution of IMDb Ratings')
plt.show()

# Example 2: Create a bar plot of movie genres
genre_counts = df['genre'].explode().value_counts().sort_values(ascending=False)[:10]
sns.barplot(x=genre_counts.values, y=genre_counts.index, palette='viridis')
plt.xlabel('Count')
plt.ylabel('Genre')
plt.title('Top 10 Movie Genres')
plt.show()

# Example 3: Create a scatter plot of IMDb ratings vs. Metascores
sns.scatterplot(data=df, x='imdb', y='metascore', alpha=0.7)
plt.xlabel('IMDb Ratings')
plt.ylabel('Metascores')
plt.title('IMDb Ratings vs. Metascores')
plt.show()
