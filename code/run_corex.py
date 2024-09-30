from util.functions import load_pickle, corex_topic_modeling

df = load_pickle('data/processed/postmortem_df.pkl')
# Call the corex_bertopic function
df_with_topics, corex_topics = corex_topic_modeling(df, n_hidden=5)

print(df_with_topics)
print(corex_topics)