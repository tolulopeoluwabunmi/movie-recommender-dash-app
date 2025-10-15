import pandas as pd

def load_movie_full():
    """Load the pre-merged dataset with genres and ratings."""
    df = pd.read_csv("data/movie_full.csv")
    print("Loaded movie_full.csv with columns:", df.columns.tolist())
    return df

if __name__ == '__main__':
    df = load_movie_full()
    print(df.head())
