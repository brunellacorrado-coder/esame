import csv
from collections import defaultdict
import itertools

# Mapping acronimi a nomi paesi
country_codes = {
    'NL': 'Netherlands',
    'CA': 'Canada',
    'AT': 'Austria',
    'US': 'United States',
    'GB': 'United Kingdom',
    'DE': 'Germany',
    'FR': 'France',
    'IT': 'Italy',
    'ES': 'Spain',
    'SE': 'Sweden',
    'CH': 'Switzerland',
    'BE': 'Belgium',
    'DK': 'Denmark',
    'NO': 'Norway',
    'FI': 'Finland',
    'PL': 'Poland',
    'CZ': 'Czech Republic',
    'AU': 'Australia',
    'JP': 'Japan',
    'CN': 'China',
    'IN': 'India',
    'BR': 'Brazil',
    'MX': 'Mexico',
    'KR': 'South Korea',
    'SG': 'Singapore',
    'NZ': 'New Zealand',
    'ZA': 'South Africa',
    'RU': 'Russia',
    'TR': 'Turkey',
    'GR': 'Greece',
    'PT': 'Portugal',
    'IE': 'Ireland',
    'NZ': 'New Zealand',
    'IL': 'Israel',
    'SA': 'Saudi Arabia',
    'AE': 'United Arab Emirates',
    'TW': 'Taiwan',
    'TH': 'Thailand',
    'MY': 'Malaysia',
    'PH': 'Philippines',
    'VN': 'Vietnam',
    'ID': 'Indonesia',
    'PK': 'Pakistan',
    'BD': 'Bangladesh',
    'NG': 'Nigeria',
    'EG': 'Egypt',
    'KE': 'Kenya',
    'AR': 'Argentina',
    'CL': 'Chile',
    'CO': 'Colombia',
    'PE': 'Peru',
}

# ===== COUNTRY CO-AUTHORSHIP =====
country_network = defaultdict(int)
country_papers = defaultdict(int)

# ===== INSTITUTION CO-AUTHORSHIP =====
institution_network = defaultdict(int)
institution_papers = defaultdict(int)

with open("1170 Amp open alex.csv", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)  # salta header
    
    for row in reader:
        if len(row) < 8:
            continue
        
        # Estrai paesi e converti acronimi
        countries_str = row[4]
        country_codes_list = [c.strip() for c in countries_str.split("|") if c.strip()]
        countries = [country_codes.get(code, code) for code in country_codes_list]
        
        for country in countries:
            country_papers[country] += 1
        
        for c1, c2 in itertools.combinations(sorted(set(countries)), 2):
            country_network[f"{c1}\t{c2}"] += 1
        
        # Estrai istituzioni
        institutions_str = row[6]
        institutions = [inst.strip() for inst in institutions_str.split("|") if inst.strip()]
        
        for inst in institutions:
            institution_papers[inst] += 1
        
        for i1, i2 in itertools.combinations(sorted(set(institutions)), 2):
            institution_network[f"{i1}\t{i2}"] += 1

# Salva country network
with open("country_network_1170_amp.txt", "w", encoding="utf-8") as f:
    for (countries, weight) in sorted(country_network.items(), key=lambda x: -x[1]):
        f.write(f"{countries}\t{weight}\n")

# Salva institution network
with open("institution_network_1170_amp.txt", "w", encoding="utf-8") as f:
    for (institutions, weight) in sorted(institution_network.items(), key=lambda x: -x[1]):
        f.write(f"{institutions}\t{weight}\n")

print(f"✓ Paesi trovati: {len(country_papers)}")
print(f"✓ Collaborazioni tra paesi: {len(country_network)}")
print(f"\nTop 15 paesi:")
for country, count in sorted(country_papers.items(), key=lambda x: -x[1])[:15]:
    print(f"  {country}: {count} paper")

print(f"\nTop 15 collaborazioni tra paesi:")
for (countries, weight) in sorted(country_network.items(), key=lambda x: -x[1])[:15]:
    print(f"  {countries.replace(chr(9), ' <-> ')}: {weight}")

print(f"\n" + "="*60)
print(f"✓ Istituzioni trovate: {len(institution_papers)}")
print(f"✓ Collaborazioni tra istituzioni: {len(institution_network)}")
print(f"\nTop 15 istituzioni:")
for inst, count in sorted(institution_papers.items(), key=lambda x: -x[1])[:15]:
    print(f"  {inst}: {count} paper")

print(f"\nTop 15 collaborazioni tra istituzioni:")
for (institutions, weight) in sorted(institution_network.items(), key=lambda x: -x[1])[:15]:
    print(f"  {institutions.replace(chr(9), ' <-> ')}: {weight}")

print(f"\n✓ File creati:")
print(f"  - country_network_1170_amp.txt")
print(f"  - institution_network_1170_amp.txt")
