import re

with open('word.tex', 'r', encoding='utf-8') as f:
    lines = f.readlines()

entries = []
i = 0
while i < len(lines):
    line = lines[i]
    m = re.match(r'\begin\{word\}\[([^\]]*)\]\{([^}]+)\}\{([^}]*)\}', line)
    if m:
        word = m.group(2)
        start_line = i + 1
        body_lines = []
        i += 1
        while i < len(lines) and '\end{word}' not in lines[i]:
            body_lines.append(lines[i])
            i += 1
        body = ''.join(body_lines)
        senses = body.count('\wordsense')
        examples = body.count('\wordexample')
        phrases = body.count('\wordphrase')
        has_breakdown = '\wordbreakdown' in body
        has_family = '\wordfamily' in body
        entries.append({
            'word': word, 'line': start_line,
            'senses': senses, 'examples': examples,
            'phrases': phrases,
            'has_breakdown': has_breakdown, 'has_family': has_family,
        })
    i += 1

print(f"Total entries: {len(entries)}")
single = [e for e in entries if e['senses'] == 1]
no_breakdown = [e for e in entries if not e['has_breakdown']]
no_family = [e for e in entries if not e['has_family']]
fewer_ex = [e for e in entries if e['examples'] < e['senses']]
no_phrase = [e for e in entries if e['phrases'] == 0]

print(f"\nEntries with only 1 sense: {len(single)}")
for e in single[:50]:
    print(f"  L{e['line']}: {e['word']} (phrases={e['phrases']})")

print(f"\nMissing wordbreakdown: {len(no_breakdown)}")
for e in no_breakdown[:10]:
    print(f"  L{e['line']}: {e['word']}")

print(f"\nMissing wordfamily: {len(no_family)}")
for e in no_family[:10]:
    print(f"  L{e['line']}: {e['word']}")

print(f"\nExamples < senses: {len(fewer_ex)}")
for e in fewer_ex[:20]:
    print(f"  L{e['line']}: {e['word']} (senses={e['senses']}, ex={e['examples']})")

print(f"\n0 phrases: {len(no_phrase)}")
for e in no_phrase[:10]:
    print(f"  L{e['line']}: {e['word']}")
