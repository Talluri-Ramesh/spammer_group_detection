import pandas as pd
import re

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z\s]', '', text)
    return text

def preprocess():
    # Load Amazon Reviews dataset
    df = pd.read_csv("data/raw_reviews.csv")

    # Rename columns to project format
    df = df.rename(columns={
        "UserId": "user_id",
        "ProductId": "product_id",
        "Score": "rating",
        "Text": "review_text",
        "Time": "timestamp"
    })

    # Keep only required columns
    df = df[['user_id', 'product_id', 'rating', 'review_text', 'timestamp']]

    # Remove missing values
    df.dropna(subset=['user_id', 'product_id', 'rating', 'timestamp'], inplace=True)

    # Clean review text
    df['review_text'] = df['review_text'].apply(clean_text)

    # Convert timestamp (Unix time → datetime)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

    # Remove duplicates
    df.drop_duplicates(subset=['user_id', 'product_id', 'review_text'], inplace=True)

    # Sort by time
    df.sort_values(by='timestamp', inplace=True)

    # Save cleaned dataset
    df.to_csv("data/cleaned_reviews.csv", index=False)

    print("✅ STEP 3 COMPLETED: Amazon reviews preprocessed successfully")

if __name__ == "__main__":
    preprocess()
