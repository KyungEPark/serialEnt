import pandas as pd
from bertopic import BERTopic
from corextopic import corextopic as ct
# https://github.com/gregversteeg/corex_topic
from sklearn.feature_extraction.text import CountVectorizer
import openai
from sklearn.cluster import KMeans
import os
from dotenv import load_dotenv, find_dotenv
from sentence_transformers import SentenceTransformer
import torch
import numpy as np
from hdbscan import HDBSCAN

def load_pickle(path):
    return pd.read_pickle(path)

def bertopic(df: pd.DataFrame, min_cluster_size = 5, min_samples = 2) -> (pd.DataFrame, BERTopic, list, dict):
    # Ensure all values in 'text' column are strings, handle missing values
    df['text'] = df['text'].astype(str).fillna('')  # Convert to string and replace NaN with an empty string
    
    # Use SentenceTransformer to generate document embeddings
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Move model to GPU if available (optional, SentenceTransformer can handle this internally)
    if torch.cuda.is_available():
        embedding_model = embedding_model.to(torch.device('cuda'))
    
    # Generate embeddings for the text data
    embeddings = embedding_model.encode(df['text'].tolist(), show_progress_bar=True)
    
    # Ensure embeddings are not empty
    assert embeddings is not None and len(embeddings) > 0, "Embeddings are empty!"

    # Stopword removal
    vectorizer_model = CountVectorizer(stop_words='english')

    # Decide number of clusters you would like
    hdbscan_model = HDBSCAN(min_cluster_size=min_cluster_size, min_samples=min_samples)
    
    # Initialize the BERTopic model (do not pass the embedding_model here)
    topic_model = BERTopic(vectorizer_model=vectorizer_model, hdbscan_model=hdbscan_model, verbose=True)
    
    # Perform topic modeling using the generated embeddings
    topics, probs = topic_model.fit_transform(df['text'], embeddings)
    
    # Add the topic assignments as a new column to the DataFrame
    df['topic'] = topics
    
    # Retrieve the topics and related words
    topics_words = {}
    for topic_id in set(topics):
        topic_words = topic_model.get_topic(topic_id)  # Get the top words for this topic
        if topic_words:
            topics_words[topic_id] = topic_words
    
    # Return the DataFrame, the fitted topic model, topic probabilities, and the topics with words
    return df, topic_model, probs, topics_words


def corex_topic_modeling(df: pd.DataFrame, n_hidden=5):
    # Step 1: Ensure 'text' column is properly formatted
    df['text'] = df['text'].astype(str).fillna('')
    
    # Step 2: Use CountVectorizer to prepare data for Corex
    vectorizer = CountVectorizer(stop_words='english', max_features=5000)  # Limit to 5000 most common words
    X = vectorizer.fit_transform(df['text'])  # Vectorize text into word counts
    words = list(vectorizer.get_feature_names_out())  # Get the words from the vectorizer

    # Step 3: Initialize and fit Corex model
    corex_model = ct.Corex(n_hidden=n_hidden, seed=42)  # Corex with 'n_hidden' topics
    corex_model.fit(X, words=words, docs=df['text'].tolist())
    
    # Step 4: Extract topics and words from Corex
    topics_corex = corex_model.get_topics()
    corex_topics = []
    for i, topic in enumerate(topics_corex):
        topic_words = [word for word, score, *rest in topic if score > 0] # Select words with positive scores
        corex_topics.append(f"Topic {i+1}: {', '.join(topic_words)}")
    
    # Step 5: Assign each document to its most likely topic
    topic_probabilities = corex_model.p_y_given_x
    # Assign the topic with the highest probability to each document
    topic_assignments = np.argmax(topic_probabilities, axis=1)
    df['topic'] = topic_assignments  # Add topic assignments to the DataFrame
    
    return df, corex_topics