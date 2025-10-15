# Name: Brielle Natzic
# Student ID: 9322 2332
# Email: bnatzic@umich.edu
# Collaborators: None
# GenAI used: ChatGPT (used for guidance and code scaffolding; all code was reviewed, tested, and modified by me)
# Function authorship: All functions written, tested, and verified by Brielle Natzic

import pandas as pd
import statistics
import csv

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

def calc_pearson_bill_flipper_by_species(data):
    """Calculate Pearson correlation between bill_length_mm and flipper_length_mm by species."""
    result = []
    species_values = {}

    # Group bill and flipper lengths by species
    for row in data:
        species = row['species']
        bill = row['bill_length_mm']
        flipper = row['flipper_length_mm']
        if bill is not None and flipper is not None:
            if species not in species_values:
                species_values[species] = {'bills': [], 'flippers': []}
            species_values[species]['bills'].append(bill)
            species_values[species]['flippers'].append(flipper)

    for species, values in species_values.items():
        bills = values['bills']
        flippers = values['flippers']
        n = len(bills)
        if n < 2:  
            r = None
        else:
            mean_bill = sum(bills) / n
            mean_flipper = sum(flippers) / n
            numerator = sum((b - mean_bill)*(f - mean_flipper) for b, f in zip(bills, flippers))
            denominator = (sum((b - mean_bill)**2 for b in bills) * sum((f - mean_flipper)**2 for f in flippers))**0.5
            r = round(numerator / denominator, 2) if denominator != 0 else None
        result.append({'species': species, 'pearson_r': r})

    return result

# Test Functions

def test_calc_avg_body_mass_by_species_island():
    test_data = [
        {'species':'A', 'island':'X', 'body_mass_g':100},
        {'species':'A', 'island':'X', 'body_mass_g':200},
        {'species':'B', 'island':'Y', 'body_mass_g':None}  # includes missing value
    ]
    # General case
    print(calc_avg_body_mass_by_species_island(test_data))
    # Edge case: empty data
    print(calc_avg_body_mass_by_species_island([]))

def test_calc_percent_above_species_median_by_sex():
    test_data = [
        {'species':'A','sex':'M','body_mass_g':100},
        {'species':'A','sex':'F','body_mass_g':200},
        {'species':'A','sex':'M','body_mass_g':None}  # includes missing value
    ]
    # General case
    print(calc_percent_above_species_median_by_sex(test_data))
    # Edge case: all masses the same
    print(calc_percent_above_species_median_by_sex([
        {'species':'A','sex':'M','body_mass_g':100},
        {'species':'A','sex':'M','body_mass_g':100}
    ]))

def test_calc_pearson_bill_flipper_by_species():
    test_data = [
        {'species':'A','bill_length_mm':10,'flipper_length_mm':20},
        {'species':'A','bill_length_mm':20,'flipper_length_mm':None},  # includes missing value
        {'species':'B','bill_length_mm':5,'flipper_length_mm':15}
    ]
    # General case
    print(calc_pearson_bill_flipper_by_species(test_data))
    # Edge case: less than 2 data points
    print(calc_pearson_bill_flipper_by_species([
        {'species':'A','bill_length_mm':10,'flipper_length_mm':20}
    ]))

if __name__ == "__main__":
    # CSV filename
    input_file = "penguins.csv"
    
    # Load and clean the data
    data = load_data(input_file)
    data = clean_data(data)
    
    # Calculation A: average body mass by species and island
    avg_mass_results = calc_avg_body_mass_by_species_island(data)
    import csv
    with open("output_avg_body_mass_by_species_island.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["species","island","avg_body_mass_g"])
        writer.writeheader()
        writer.writerows(avg_mass_results)
    
    # Calculation B: % above species median by sex
    percent_above_results = calc_percent_above_species_median_by_sex(data)
    with open("output_percent_above_species_median_by_sex.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["species","sex","percent_above_median"])
        writer.writeheader()
        writer.writerows(percent_above_results)
    
    # Calculation C: Pearson correlation bill vs. flipper by species
    pearson_results = calc_pearson_bill_flipper_by_species(data)
    with open("output_pearson_bill_flipper_by_species.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["species","pearson_r"])
        writer.writeheader()
        writer.writerows(pearson_results)

