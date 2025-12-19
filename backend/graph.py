import pandas as pd
import networkx as nx

def detect_spammer_groups():
    # Load data
    reviews = pd.read_csv("data/cleaned_reviews.csv")
    spammers = pd.read_csv("results/spammer_users.csv")

    # Get spammer user IDs
    spammer_ids = set(spammers[spammers['spammer'] == 1]['user_id'])

    # Filter reviews to only spam users
    spam_reviews = reviews[reviews['user_id'].isin(spammer_ids)]

    # Create graph
    G = nx.Graph()

    # Build connections: users reviewing same product
    for product_id, group in spam_reviews.groupby('product_id'):
        users = list(group['user_id'])
        for i in range(len(users)):
            for j in range(i + 1, len(users)):
                G.add_edge(users[i], users[j])

    # Find connected components (groups)
    communities = list(nx.connected_components(G))

    # Prepare result
    result = []
    for group_id, users in enumerate(communities):
        for user in users:
            result.append([user, group_id])

    # Save groups
    pd.DataFrame(
        result, columns=['user_id', 'group_id']
    ).to_csv("results/spammer_groups.csv", index=False)

    print("✅ STEP 6 COMPLETED: Spammer groups detected")

if __name__ == "__main__":
    detect_spammer_groups()
