import csv
from collections import defaultdict
import itertools

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
        
        for keyword in keywords:
            keyword_papers[keyword] += 1
        
        for k1, k2 in itertools.combinations(sorted(set(keywords)), 2):
            keyword_network[f"{k1}\t{k2}"] += 1

# Salva keyword network
with open("keyword_network_1170_amp.txt", "w", encoding="utf-8") as f:
    for (keywords, weight) in sorted(keyword_network.items(), key=lambda x: -x[1]):
        f.write(f"{keywords}\t{weight}\n")

print(f"✓ Keywords trovate: {len(keyword_papers)}")
print(f"✓ Co-occorrenze: {len(keyword_network)}")

print(f"\nTop 20 keywords:")
for keyword, count in sorted(keyword_papers.items(), key=lambda x: -x[1])[:20]:
    print(f"  {keyword}: {count} paper")

print(f"\nTop 20 co-occorrenze:")
for (keywords, weight) in sorted(keyword_network.items(), key=lambda x: -x[1])[:20]:
    print(f"  {keywords.replace(chr(9), ' <-> ')}: {weight}")

print(f"\n✓ File creato: keyword_network_1170_amp.txt")
