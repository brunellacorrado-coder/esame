import csv
from collections import defaultdict
import itertools

# Leggi thesaurus
thesaurus = {}
with open("thesaurus_1170.txt", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        variants = [v.strip().lower() for v in line.split("|")]
        canonical = variants[0]  # Prima variante è il termine canonico
        for variant in variants:
            thesaurus[variant] = canonical

print(f"✓ Thesaurus caricato: {len(thesaurus)} mappature")

keyword_network = defaultdict(int)
keyword_papers = defaultdict(int)

with open("1170 Amp open alex.csv", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)  # salta header
    
    for row in reader:
        if len(row) < 8:
            continue
        
        keywords_str = row[7]
        keywords = [kw.strip().replace('"', '') for kw in keywords_str.split("|") if kw.strip()]
        
        # Applica thesaurus (converti a minuscolo e cerca nel thesaurus)
        normalized_keywords = []
        for kw in keywords:
            kw_lower = kw.lower()
            if kw_lower in thesaurus:
                normalized_keywords.append(thesaurus[kw_lower])
            else:
                normalized_keywords.append(kw_lower)
        
        for keyword in normalized_keywords:
            keyword_papers[keyword] += 1
        
        for k1, k2 in itertools.combinations(sorted(set(normalized_keywords)), 2):
            keyword_network[f"{k1}\t{k2}"] += 1

# Filtra keywords con occorrenze < 5
min_occurrences = 5
filtered_keywords = {kw: count for kw, count in keyword_papers.items() if count >= min_occurrences}
print(f"\n✓ Keywords originali: {len(keyword_papers)}")
print(f"✓ Keywords con >= {min_occurrences} occorrenze: {len(filtered_keywords)}")

# Filtra anche la network
filtered_network = {}
for (keywords, weight) in keyword_network.items():
    kw1, kw2 = keywords.split("\t")
    if kw1 in filtered_keywords and kw2 in filtered_keywords:
        filtered_network[keywords] = weight

print(f"✓ Co-occorrenze filtrate: {len(filtered_network)}")

# Salva keyword network normalizzato e filtrato
with open("keyword_network_1170_amp_normalized.txt", "w", encoding="utf-8") as f:
    for (keywords, weight) in sorted(filtered_network.items(), key=lambda x: -x[1]):
        f.write(f"{keywords}\t{weight}\n")

print(f"\nTop 20 keywords (normalizzate, >= {min_occurrences} occorrenze):")
for keyword, count in sorted(filtered_keywords.items(), key=lambda x: -x[1])[:20]:
    print(f"  {keyword}: {count} paper")

print(f"\nTop 20 co-occorrenze:")
for (keywords, weight) in sorted(filtered_network.items(), key=lambda x: -x[1])[:20]:
    print(f"  {keywords.replace(chr(9), ' <-> ')}: {weight}")

print(f"\n✓ File creato: keyword_network_1170_amp_normalized.txt")
