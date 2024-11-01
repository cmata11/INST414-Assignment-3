import pandas as pd

# Read the CSV file
df = pd.read_csv("TMDB_movies.csv")

# Select specific columns
selected_columns = [
    "title",
    "vote_average",
    "vote_count",
    "release_date",
    "adult",
    "genres",
    "production_companies"
]

# Create new dataframe with selected columns
movies_df = df[selected_columns]

# Convert release_date to datetime
movies_df['release_date'] = pd.to_datetime(movies_df['release_date'])

# Display first few rows to verify
print(movies_df.head())

# Display basic information about the dataframe
print("\nDataframe Info:")
print(movies_df.info())