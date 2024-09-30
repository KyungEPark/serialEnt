from util.functions import load_pickle, bertopic

df = load_pickle('data/processed/postmortem_df.pkl')

# Apply BERTopic and get the DataFrame with topics, the topic model, and embeddings
df_with_topics, topic_model, probs, topics_words = bertopic(df, min_cluster_size = 5, min_samples = 2)


# Print the DataFrame with topic assignments
print(df_with_topics.head())

# Print topic information (top words for each topic)
print("Topics and related words:")
for topic_id, words in topics_words.items():
    print(f"Topic {topic_id}:")
    for word, score in words:
        print(f"  {word}: {score}")

# Optionally, print topic details using built-in BERTopic methods
print(topic_model.get_topic_info())  # Overview of the topics