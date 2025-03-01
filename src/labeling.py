import os
import pandas as pd

def label_message(message):
    # Initialize labeled tokens list
    labeled_tokens = []
    
    tokens = message.split()
    
    for token in tokens:
        if token.lower() in ['baby', 'bottle']:  # Example: B-Product
            labeled_tokens.append((token, 'B-PRODUCT'))
        elif token.lower() == 'bottle':  # Example: I-Product
            labeled_tokens.append((token, 'I-PRODUCT'))
        elif token.lower() in ['addis', 'abeba', 'bole']:  # Example: B-LOC
            labeled_tokens.append((token, 'B-LOC'))
        elif token.lower() == 'abeba':  # Example: I-LOC
            labeled_tokens.append((token, 'I-LOC'))
        elif 'ዋጋ' in token:  # Example: B-PRICE
            labeled_tokens.append((token, 'B-PRICE'))
        elif token.isdigit():  # Example: I-PRICE (assumes numbers are part of price entities)
            labeled_tokens.append((token, 'I-PRICE'))
        else:
            labeled_tokens.append((token, 'O'))  # Default label for other tokens
    
    return labeled_tokens

def save_labeled_data(messages, output_file):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for message in messages:
            # Debug: Print each message being processed
            print(f"Processing message: {message}")
            
            labeled_message = label_message(message)
            for token, label in labeled_message:
                f.write(f"{token}\t{label}\n")  
            f.write("\n")  

    # Debug: Confirm the file has been written
    print(f"Labeled data saved to {output_file}")

def main():
    # Read preprocessed data
    input_file = 'preprocessed_telegram_data.csv' 
    output_file = 'data/labeled_data.conll'

    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Input file '{input_file}' does not exist.")
        return

    df = pd.read_csv(input_file)

    # Debug: Check the DataFrame's columns
    print("DataFrame columns:", df.columns)

    # Use the 'Processed_Message' column for labeling
    if 'Processed_Message' in df.columns:
        messages = df['Processed_Message'].tolist()  # Change to correct column name
    else:
        print(f"'Processed_Message' column not found in the data.")
        return

    # Save the labeled data
    save_labeled_data(messages, output_file)

if __name__ == '__main__':
    main()