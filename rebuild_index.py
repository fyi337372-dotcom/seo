# -*- coding: utf-8 -*-
import os
import re

# Get all article files
articles = []
seen_titles = set()

for f in os.listdir('article'):
    if f.endswith('.html'):
        path = f'article/{f}'
        with open(path, 'r', encoding='utf-8', errors='ignore') as fp:
            content = fp.read()
            match = re.search(r'<title>(.*?)</title>', content)
            title = match.group(1) if match else f.replace('.html', '')
            
            # Skip duplicates by title
            if title in seen_titles:
                continue
            seen_titles.add(title)
            
            date_match = re.search(r'(\d{4})-(\d{2})-(\d{2})', content)
            date = date_match.group(0) if date_match else '2026-03-04'
            cat_match = re.search(r'<span class="category">(.*?)</span>', content)
            category = cat_match.group(1) if cat_match else '游戏攻略'
            
            articles.append({
                'file': f,
                'title': title,
                'date': date,
                'category': category
            })

# Sort by date descending
articles.sort(key=lambda x: x['date'], reverse=True)

# Take latest 30
latest = articles[:30]

# Read index.html
with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Fix garbled text
c = c.replace('传奇技?</a>', '传奇技巧</a>')
c = c.replace('游戏技?</a>', '游戏技巧</a>')

# Find article grid section
gs = c.find('<div class="article-grid">')
ts = c.find('<section class="tips-section">')

if gs > 0 and ts > 0:
    before = c[:gs + 25]
    after = c[ts:]
    
    # Build new article cards
    new_cards = ''
    for a in latest:
        new_cards += f'''
                <div class="article-card">
                    <span class="category">{a['category']}</span>
                    <h3>{a['title']}</h3>
                    <p>{a['title']}</p>
                    <div class="meta">更新时间：{a['date']}</div>
                    <a href="article/{a['file']}" class="btn">阅读全文 →</a>
                </div>
'''
    
    c = before + new_cards + after

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print(f'Done! Kept {len(latest)} latest articles, removed duplicates.')
