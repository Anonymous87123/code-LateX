import re
import sys

with open('word.tex', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = re.compile(r'\\begin\{word\}.*?\\end\{word\}', re.DOTALL)
entries = pattern.findall(content)

name_pat = re.compile(r'\\begin\{word\}\[([^\]]*)\]\{([^}]+)\}')
sense_pat = re.compile(r'\\wordsense\{([^}]+)\}')

# Find entries with multiple meanings crammed in one wordsense line
crammed = []
for e in entries:
    senses = sense_pat.findall(e)
    m = name_pat.search(e)
    if not m:
        continue
    stars = m.group(1)
    name = m.group(2)
    sense_count = len(senses)
    for s in senses:
        if '；' in s or ('; ' in s and len(s) > 30):
            crammed.append((name, stars, s[:80], sense_count))
            break

print(f'Entries with multiple meanings crammed in one wordsense: {len(crammed)}')
print('First 40:')
for name, stars, sense, cnt in crammed[:40]:
    print(f'  [{stars}] {name} (senses={cnt}): {sense}')

# Also find single-sense entries from first chapter
print('\n--- Single-sense entries from beginning (first 50) ---')
single = []
for e in entries:
    m = name_pat.search(e)
    if not m:
        continue
    senses = e.count('\\wordsense')
    if senses == 1:
        single.append((m.group(2), m.group(1)))
        if len(single) >= 50:
            break

for name, stars in single:
    print(f'  [{stars}] {name}')
