import json
import csv
from collections import defaultdict
import itertools

COUNTRY_NAMES = {
    'AT': 'Austria', 'AU': 'Australia', 'BR': 'Brazil', 'CA': 'Canada',
    'CN': 'China', 'DE': 'Germany', 'ES': 'Spain', 'HU': 'Hungary',
    'IL': 'Israel', 'IN': 'India', 'IT': 'Italy', 'NL': 'Netherlands', 'US': 'United States'
}

def get_country_name(code):
    return COUNTRY_NAMES.get(code, code)

def extract_countries(authorships):
    countries = []
    for a in authorships or []:
        countries.extend(a.get("countries", []))
    return list(set(countries))

with open("project_work.json") as f:
    results = json.load(f).get("results", [])

country_network = defaultdict(int)
country_papers = defaultdict(int)

for item in results:
    countries = extract_countries(item.get("authorships"))
    for country in countries:
        country_papers[country] += 1
    for country1, country2 in itertools.combinations(sorted(set(countries)), 2):
        country_network[f"{country1}|{country2}"] += 1

with open("country_network.txt", "w") as f:
    for (countries, weight) in sorted(country_network.items(), key=lambda x: -x[1]):
        c1, c2 = countries.split("|")
        f.write(f"{get_country_name(c1)}\t{get_country_name(c2)}\t{weight}\n")

unique_countries = sorted(set(itertools.chain(*[extract_countries(item.get("authorships")) for item in results])))

matrix = {c: {c2: 0 for c2 in unique_countries} for c in unique_countries}
for item in results:
    countries = extract_countries(item.get("authorships"))
    for country1, country2 in itertools.combinations(sorted(set(countries)), 2):
        matrix[country1][country2] += 1
        matrix[country2][country1] += 1

with open("country_coauthorship_matrix.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow([""] + [get_country_name(c) for c in unique_countries])
    for country in unique_countries:
        writer.writerow([get_country_name(country)] + [matrix[country][c] for c in unique_countries])

with open("vosviewer_countries.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=["Country", "Documents", "Collaborations"])
    writer.writeheader()
    for country in unique_countries:
        doc_count = country_papers.get(country, 0)
        collabs = sum(country_network.get(f"{country}|{c2}", 0) for c2 in unique_countries if c2 != country) + sum(country_network.get(f"{c1}|{country}", 0) for c1 in unique_countries if c1 != country)
        writer.writerow({"Country": get_country_name(country), "Documents": doc_count, "Collaborations": collabs})

print("="*50)
print("STATISTICHE CO-AUTHORSHIP PAESI")
print("="*50)
print(f"Numero di paesi: {len(unique_countries)}")
print(f"Numero di collaborazioni: {len(country_network)}")
print(f"\nTop 10 paesi:")
for country, count in sorted(country_papers.items(), key=lambda x: -x[1])[:10]:
    print(f"  {get_country_name(country)}: {count} paper")
print(f"\nTop 10 collaborazioni:")
for (countries, weight) in sorted(country_network.items(), key=lambda x: -x[1])[:10]:
    c1, c2 = countries.split("|")
    print(f"  {get_country_name(c1)} - {get_country_name(c2)}: {weight}")
