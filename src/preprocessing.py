import pandas as pd  # type: ignore
import re
import nltk  # type: ignore

# Download required NLTK datasets
nltk.data.path.append('./nltk_data')
nltk.download('punkt_tab', download_dir=r'C:\Users\User\Amharic-LLM-for-Named-Entity-Recognition\nltk_data')  # Required for tokenization

# Load Amharic stopwords
def load_amharic_stopwords():
    with open(r'data/amharic_stopwords.txt', 'r', encoding='utf-8') as file:  # Use raw string or forward slashes
        stopwords = file.read().splitlines()
    return set(stopwords)

from nltk.tokenize import word_tokenize 

# Preprocess text data: Tokenizing and Normalizing
def preprocess_text(text):
    if pd.isna(text) or not isinstance(text, str):  # Check for NaN and if the input is a string
        return ''  # Return an empty string for non-string inputs

    # Normalize by removing non-Amharic characters (keeping Amharic letters, numbers, punctuation)
    cleaned_text = re.sub(r'[^\u1200-\u137F\s]', '', text)
    
    # Tokenize text into words
    tokens = word_tokenize(cleaned_text)
    
    # Remove stopwords
    stop_words = load_amharic_stopwords()
    tokens = [word for word in tokens if word not in stop_words]
    
    return ' '.join(tokens)

# Load the raw CSV data and preprocess
def preprocess_data(input_csv, output_csv):
    # Read data
    df = pd.read_csv(input_csv)
    
    # Preprocess each message
    df['Processed_Message'] = df['Message'].apply(preprocess_text)
    
    # Separate metadata (e.g., channel title, username) from content
    df_processed = df[['Channel Title', 'Channel Username', 'ID', 'Processed_Message', 'Date', 'Media Path']]
    
    # Save the preprocessed data to a new CSV file
    df_processed.to_csv(output_csv, index=False)
    print(f"Preprocessed data saved to {output_csv}")

if __name__ == "__main__":
    # Preprocess the telegram data CSV and save it
    preprocess_data('data/telegram_data.csv', 'data/preprocessed_telegram_data.csv')