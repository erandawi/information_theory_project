import os
import re
import json
import sys
import string
from bs4 import BeautifulSoup
from collections import defaultdict

import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

from src.exception.exception import InformaitonThoeryProjectException
from src.logging.logger import logging

# Download NLTK data if not already present
nltk.download('punkt')

class IndexBuilder:
    def __init__(self, directory="data/scraped", index_file="data/index/index.json"):
        self.directory = directory
        self.index_file = index_file
        self.index = defaultdict(set)  # inverted index: word -> set of doc_ids
        self.stemmer = PorterStemmer()

        if not os.path.exists(self.directory):
            raise InformaitonThoeryProjectException("Scraped directory not found", sys)

    def clean_and_tokenize(self, text):
        text = text.lower()  # normalization: lowercase
        text = re.sub(r'\d+', '', text)  # remove digits
        text = text.translate(str.maketrans('', '', string.punctuation))  # remove punctuation
        tokens = word_tokenize(text)  # tokenize
        tokens = [self.stemmer.stem(token) for token in tokens if len(token) > 1]  # stemming & filtering short tokens
        return tokens

    def build_index(self):
        logging.info(f"Starting index build from {self.directory}")
        try:
            for filename in os.listdir(self.directory):
                if filename.endswith(".html"):
                    filepath = os.path.join(self.directory, filename)
                    with open(filepath, 'r', encoding='utf-8') as file:
                        soup = BeautifulSoup(file, 'html.parser')
                        text = soup.get_text()
                        tokens = self.clean_and_tokenize(text)
                        for token in tokens:
                            self.index[token].add(filename)  # map token to doc
            logging.info("Indexing completed")
        except Exception as e:
            raise InformaitonThoeryProjectException(f"Error while indexing documents: {e}", sys)

    def save_index(self):
        try:
            os.makedirs(os.path.dirname(self.index_file), exist_ok=True)
            # Convert sets to lists for JSON serialization
            json_index = {term: list(doc_ids) for term, doc_ids in self.index.items()}
            with open(self.index_file, 'w', encoding='utf-8') as f:
                json.dump(json_index, f, indent=2)
            logging.info(f"Inverted index saved to {self.index_file}")
        except Exception as e:
            raise InformaitonThoeryProjectException(f"Error saving index file: {e}", sys)
