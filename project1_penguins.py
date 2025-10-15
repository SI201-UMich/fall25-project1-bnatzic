# Name: Brielle Natzic
# Student ID: 9322 2332
# Email: bnatzic@umich.edu
# Collaborators: None
# GenAI used: ChatGPT (used for guidance and code scaffolding; all code was reviewed, tested, and modified by me)
# Function authorship: All functions written, tested, and verified by Brielle Natzic

import pandas as pd
import statistics

def load_data(filename):
    """Load the CSV dataset."""
    return pd.read_csv(filename)

def clean_data(data):
    """Clean the dataset by dropping rows with missing values in key columns."""
    # Only keep rows with valid species, island, sex, and body mass
    return data.dropna(subset=['species', 'island', 'sex', 'body_mass_g'])

def calc_avg_body_mass_by_species_island(data):
    """Calculate average body mass for each species on each island."""
    result = []
    species_island_masses = {}

    for row in data:
        species = row['species']
        island = row['island']
        mass = row['body_mass_g']
        if mass != None:  # skip missing values
            if species not in species_island_masses:
                species_island_masses[species] = {}
            if island not in species_island_masses[species]:
                species_island_masses[species][island] = []
            species_island_masses[species][island].append(mass)

    for species in species_island_masses:
        for island in species_island_masses[species]:
            masses = species_island_masses[species][island]
            avg_mass = sum(masses) / len(masses)
            result.append({'species': species, 'island': island, 'avg_body_mass_g': avg_mass})

    return result

def calc_percent_above_species_median_by_sex(data):
    """Calculate the % of individuals above species median body mass, split by sex."""
    result = []

    # Compute species median body mass
    species_medians = {}
    for row in data:
        species = row['species']
        mass = row['body_mass_g']
        if mass is not None:
            species_medians.setdefault(species, []).append(mass)
    
    for species in species_medians:
        species_medians[species] = statistics.median(species_medians[species])

    # Count above-median per species-sex
    counts = {}
    totals = {}
    for row in data:
        species = row['species']
        sex = row['sex']
        mass = row['body_mass_g']
        if mass is not None:
            key = (species, sex)
            totals[key] = totals.get(key, 0) + 1
            if mass > species_medians[species]:
                counts[key] = counts.get(key, 0) + 1

    # Compute percentages
    for key in totals:
        species, sex = key
        percent = 100 * counts.get(key, 0) / totals[key]
        result.append({'species': species, 'sex': sex, 'percent_above_median': round(percent, 2)})

    return result
