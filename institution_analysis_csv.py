import csv
from collections import defaultdict
import itertools

institution_network = defaultdict(int)
institution_papers = defaultdict(int)

# Leggi il CSV
with open("OPENALEX_1159_amp.csv", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)  # salta header
    
    for row in reader:
        if len(row) < 7:
            continue
        
        institutions_str = row[6]  # colonna istituzioni
        institutions = [inst.strip() for inst in institutions_str.split("|") if inst.strip()]
        
        for inst in institutions:
            institution_papers[inst] += 1
        
        for inst1, inst2 in itertools.combinations(sorted(set(institutions)), 2):
            institution_network[f"{inst1}\t{inst2}"] += 1

print(f"✓ Trovate {len(institution_papers)} istituzioni")
print(f"✓ Trovate {len(institution_network)} collaborazioni")

# Salva rete
with open("institution_network_csv_eskape.txt", "w", encoding="utf-8") as f:
    for (institutions, weight) in sorted(institution_network.items(), key=lambda x: -x[1]):
        f.write(f"{institutions}\t{weight}\n")

print(f"✓ Network file creato")

# Top istituzioni
print(f"\nTop 15 istituzioni:")
for institution, count in sorted(institution_papers.items(), key=lambda x: -x[1])[:15]:
    print(f"  {institution}: {count} paper")

# Top collaborazioni
print(f"\nTop 15 collaborazioni:")
for (institutions, weight) in sorted(institution_network.items(), key=lambda x: -x[1])[:15]:
    print(f"  {institutions.replace(chr(9), ' <-> ')}: {weight}")
