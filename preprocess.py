## !pip install opendatasets
import opendatasets as od
od.download("https://www.kaggle.com/datasets/nikitricky/random-english-sentences")

file_path = "path to file"
def load_sentences_from_txt(file_path):
    with open(file_path, 'r') as file:
        sentences = file.readlines()  # Read all lines from the text file
    return [sentence.strip() for sentence in sentences]  # Remove any leading/trailing whitespace

import re

def preprocess_sentences(sentences):
    cleaned_sentences = []

    for sentence in sentences:
        sentence = sentence.lower().strip()  # Convert to lowercase and strip spaces
        sentence = re.sub(r'[^a-z\s]', '', sentence)  # Remove punctuation/numbers
        cleaned_sentences.append(sentence)

    return cleaned_sentences

import csv
from collections import Counter

def load_sentences_from_txt(file_path):
    """Load sentences from the input text file."""
    with open(file_path, 'r') as f:
        sentences = f.readlines()
    return [sentence.strip() for sentence in sentences]

def generate_ngrams(sentences):
    """Generate n-grams (1-grams to N-grams) from the given sentences."""
    phrase_counter = Counter()

    for sentence in sentences:
        words = sentence.split()  # Split the sentence into words

        # Generate n-grams from 1 to the length of the sentence
        for n in range(1, len(words) + 1):  # From 1-gram to N-gram
            for i in range(len(words) - n + 1):  # Sliding window of size n
                phrase = ' '.join(words[i:i + n])  # Create the n-gram
                phrase_counter[phrase] += 1  # Count frequency of each n-gram

    return phrase_counter

def save_ngrams_to_csv(ngrams, output_file_path):
    """Save the generated n-grams and their counts to a CSV file."""
    with open(output_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["N-Gram", "Count"])  # Write the header
        for ngram, count in ngrams.items():
            writer.writerow([ngram, count])

# Define the file paths
file_path = "path to file"
output_file_path = 'ngrams.csv'  # The output CSV file where n-grams will be saved

# Process and save the n-grams to the CSV file
sentences = load_sentences_from_txt(file_path)
ngrams = generate_ngrams(sentences)
save_ngrams_to_csv(ngrams, output_file_path)

print(f"N-Grams have been saved to {output_file_path}")

