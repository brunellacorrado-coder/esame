import json
import csv
from collections import defaultdict
import itertools

def extract_institutions(authorships):
    """Estrae le istituzioni dagli autori"""
    institutions = []
    for a in authorships or []:
        insts = a.get("institutions", [])
        for inst in insts:
            name = inst.get("display_name", "")
            if name:
                institutions.append(name)
    return list(set(institutions))

with open("works_eskape.json") as f:
    results = json.load(f).get("results", [])

print(f"Elaborando {len(results)} paper...")

institution_network = defaultdict(int)
institution_papers = defaultdict(int)

for idx, item in enumerate(results):
    if idx % 10 == 0:
        print(f"  {idx}/{len(results)}...")
    
    institutions = extract_institutions(item.get("authorships"))
    for inst in institutions:
        institution_papers[inst] += 1
    for inst1, inst2 in itertools.combinations(sorted(set(institutions)), 2):
        key = f"{inst1}|{inst2}"
        institution_network[key] += 1

print(f"\n✓ Trovate {len(institution_papers)} istituzioni")
print(f"✓ Trovate {len(institution_network)} collaborazioni")

# Salva il file di rete per VOSviewer
with open("institution_network_eskape.txt", "w", encoding="utf-8") as f:
    f.write("Institution1\tInstitution2\tWeight\n")
    for (institutions, weight) in sorted(institution_network.items(), key=lambda x: -x[1]):
        inst1, inst2 = institutions.split("|")
        f.write(f"{inst1}\t{inst2}\t{weight}\n")

print(f"✓ Network file creato: institution_network_eskape.txt")

# Top 10
print(f"\nTop 10 istituzioni:")
for institution, count in sorted(institution_papers.items(), key=lambda x: -x[1])[:10]:
    print(f"  {institution}: {count} paper")

print(f"\nTop 10 collaborazioni:")
for (institutions, weight) in sorted(institution_network.items(), key=lambda x: -x[1])[:10]:
    print(f"  {institutions}: {weight}")
