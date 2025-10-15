# Name: Brielle Natzic
# Student ID: 9322 2332
# Email: bnatzic@umich.edu
# Collaborators: None
# GenAI used: ChatGPT (used for guidance and code scaffolding; all code was reviewed, tested, and modified by me)
# Function authorship: All functions written, tested, and verified by Brielle Natzic

import pandas as pd

def load_data(filename):
    """Load the CSV dataset."""
    return pd.read_csv(filename)

def clean_data(data):
    """Clean the dataset by dropping rows with missing values in key columns."""
    # Only keep rows with valid species, island, sex, and body mass
    return data.dropna(subset=['species', 'island', 'sex', 'body_mass_g'])



