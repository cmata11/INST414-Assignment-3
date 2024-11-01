import pandas as pd
import ast

# Read the CSV file and print initial info
df = pd.read_csv("TMDB_movies.csv")
print("\nInitial DataFrame Info:")
print(df.head(1))  # Print first row to verify data structure

# Create a clean copy with necessary columns
movies_df = df[["title", "vote_average", "genres"]].copy()

# Function to safely evaluate genres string and extract names
def process_genres(genres_str):
    try:
        genres_list = ast.literal_eval(genres_str)
        return [genre['name'] for genre in genres_list]
    except Exception as e:
        print(f"Error processing genres: {str(e)}")
        print(f"Problematic genres string: {genres_str}")
        return []

# Create genre names column
movies_df.loc[:, 'genre_names'] = movies_df['genres'].apply(process_genres)

# Function to get top 10 movies by genre
def get_top_10_by_genre(movie_title):
    print(f"\nSearching for movie: {movie_title}")
    
    # Check if movie exists
    movie_mask = movies_df['title'] == movie_title
    if not any(movie_mask):
        print(f"Movie '{movie_title}' not found in dataset. Available titles (first 5):")
        print(movies_df['title'].head())
        return
    
    # Get target movie's genres
    target_genres = movies_df.loc[movie_mask, 'genre_names'].iloc[0]
    print(f"Found movie. Genres: {target_genres}")
    
    # Filter similar movies
    similar_movies = movies_df[
        movies_df['genre_names'].apply(lambda x: any(genre in target_genres for genre in x))
    ]
    print(f"\nFound {len(similar_movies)} movies with similar genres")
    
    # Get top 10
    top_10 = similar_movies.nlargest(10, 'vote_average')[['title', 'vote_average']]
    
    if len(top_10) == 0:
        print("No similar movies found!")
        return
        
    print(f"\nTop 10 highest rated movies sharing genres with {movie_title}")
    print(f"Genres: {', '.join(target_genres)}")
    print("\nRank  Title                                           Rating")
    print("-" * 65)
    
    for i, (_, row) in enumerate(top_10.iterrows(), 1):
        print(f"{i:<5} {row['title']:<45} {row['vote_average']:.1f}")

# Print sample of data before processing
print("\nSample of raw genres data:")
print(movies_df['genres'].head())

# Print sample of processed genres
print("\nSample of processed genres:")
print(movies_df['genre_names'].head())

# Get top 10 for Interstellar
get_top_10_by_genre("Interstellar")