import pandas as pd

def extract_features():
    # Load cleaned dataset
    df = pd.read_csv("data/cleaned_reviews.csv")

    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Group by user and extract features
    features = df.groupby('user_id').agg(
        review_count=('rating', 'count'),
        avg_rating=('rating', 'mean'),
        first_review=('timestamp', 'min'),
        last_review=('timestamp', 'max')
    ).reset_index()

    # Calculate review span in days
    features['review_span_days'] = (
        features['last_review'] - features['first_review']
    ).dt.days + 1

    # Drop unnecessary columns
    features.drop(columns=['first_review', 'last_review'], inplace=True)

    # Save features
    features.to_csv("data/user_features.csv", index=False)

    print("✅ STEP 4 COMPLETED: User features extracted")

if __name__ == "__main__":
    extract_features()
