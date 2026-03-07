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

articles.sort(key=lambda x: x['date'], reverse=True)
latest = articles[:30]

print(f"Found {len(articles)} articles, keeping {len(latest)}")

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Find FIRST article-grid and FIRST tips-section
grid_match = re.search(r'<div class="article-grid"', c)
section_match = re.search(r'<section class="tips-section">', c)

if grid_match and section_match:
    grid_pos = grid_match.start()
    section_pos = section_match.start()
    
    # Get content before the first article-grid
    before = c[:grid_pos]
    
    # Get the first article-grid tag itself
    grid_tag = c[grid_pos:grid_match.end()]
    
    # Get content between first grid and first tips-section (the old cards - to be replaced)
    old_cards_section = c[grid_match.end():section_pos]
    
    # Get content from tips-section to end
    after = c[section_pos:]
    
    # Build new cards
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
    
    # Reconstruct
    new_content = before + grid_tag + new_cards + after
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    card_count = new_content.count('<div class="article-card">')
    print(f"Done! Index has {card_count} cards")
else:
    print("ERROR: Could not find patterns")
