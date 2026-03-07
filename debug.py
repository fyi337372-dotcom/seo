import re
with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Find all article-grid and tips-section positions
for m in re.finditer(r'<div class="article-grid"|<section class="tips-section">', c):
    print(f'{m.start()}: {m.group()}')
