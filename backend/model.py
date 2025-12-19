import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_spammers():
    # Load user features
    df = pd.read_csv("data/user_features.csv")

    # Select features for ML model
    X = df[['review_count', 'avg_rating', 'review_span_days']]

    # Train Isolation Forest
    model = IsolationForest(
        n_estimators=100,
        contamination=0.1,   # assume 10% spammers
        random_state=42
    )

    df['anomaly'] = model.fit_predict(X)

    # Convert anomaly score to spammer label
    df['spammer'] = df['anomaly'].apply(lambda x: 1 if x == -1 else 0)

    # Save results
    df[['user_id', 'spammer']].to_csv(
        "results/spammer_users.csv", index=False
    )

    print("✅ STEP 5 COMPLETED: Spammer detection finished")

if __name__ == "__main__":
    detect_spammers()
