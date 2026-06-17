import json
import csv
from collections import defaultdict
import itertools

def extract_countries(authorships):
    """Estrae i paesi dagli autori"""
    countries = []
    for a in authorships or []:
        # I paesi sono già in a['countries']
        country_list = a.get("countries", [])
        countries.extend(country_list)
    
    return list(set(countries))  # Rimuove duplicati

# Carica il file JSON
with open("project_work.json", "r", encoding="utf-8") as f:
    data = json.load(f)

results = data.get("results", [])

# === OPZIONE 1: Formato VOSviewer (Network File) ===
# Crea una rete di co-authorship tra paesi
country_network = defaultdict(int)
country_papers = defaultdict(int)

for item in results:
    countries = extract_countries(item.get("authorships"))
    
    # Conta i paper per paese
    for country in countries:
        country_papers[country] += 1
    
    # Conta le collaborazioni tra paesi
    for country1, country2 in itertools.combinations(sorted(set(countries)), 2):
        key = f"{country1}|{country2}"
        country_network[key] += 1

# Salva il file di rete per VOSviewer
with open("country_network.txt", "w", encoding="utf-8") as f:
    f.write("Country1\tCountry2\tWeight\n")
    for (countries, weight) in sorted(country_network.items(), key=lambda x: -x[1]):
        country1, country2 = countries.split("|")
        f.write(f"{country1}\t{country2}\t{weight}\n")

print(f"✓ Network file creato: country_network.txt ({len(country_network)} collaborazioni)")

# === OPZIONE 2: Matrice di co-authorship (CSV) ===
unique_countries = sorted(set(itertools.chain(*[
    extract_countries(item.get("authorships")) for item in results
])))

# Crea matrice di adiacenza
matrix = {c: {c2: 0 for c2 in unique_countries} for c in unique_countries}

for item in results:
    countries = extract_countries(item.get("authorships"))
    for country1, country2 in itertools.combinations(sorted(set(countries)), 2):
        matrix[country1][country2] += 1
        matrix[country2][country1] += 1

# Salva la matrice
with open("country_coauthorship_matrix.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow([""] + unique_countries)
    for country in unique_countries:
        writer.writerow([country] + [matrix[country][c] for c in unique_countries])

print(f"✓ Matrice di co-authorship creata: country_coauthorship_matrix.csv")

# === OPZIONE 3: CSV per VOSviewer (dettagli paesi) ===
with open("vosviewer_countries.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=["Country", "Documents", "Citations"])
    writer.writeheader()
    
    for country in unique_countries:
        # Conta i documenti per paese
        doc_count = country_papers.get(country, 0)
        # Calcola le collaborazioni totali
        collabs = sum(country_network.get(f"{country}|{c2}", 0) for c2 in unique_countries if c2 != country) + \
                  sum(country_network.get(f"{c1}|{country}", 0) for c1 in unique_countries if c1 != country)
        
        writer.writerow({
            "Country": country,
            "Documents": doc_count,
            "Citations": collabs
        })

print(f"✓ File VOSviewer creato: vosviewer_countries.csv ({len(unique_countries)} paesi)")

# === STATISTICHE ===
print("\n" + "="*50)
print("STATISTICHE CO-AUTHORSHIP PAESI")
print("="*50)
print(f"Numero di paesi: {len(unique_countries)}")
print(f"Numero di collaborazioni: {len(country_network)}")
print(f"\nTop 10 paesi per numero di paper:")
for country, count in sorted(country_papers.items(), key=lambda x: -x[1])[:10]:
    print(f"  {country}: {count} paper")

print(f"\nTop 10 collaborazioni tra paesi:")
for (countries, weight) in sorted(country_network.items(), key=lambda x: -x[1])[:10]:
    print(f"  {countries}: {weight} collaborazioni")
