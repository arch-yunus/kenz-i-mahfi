#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Kenz-i Mahfî Külliyatı - Web Veritabanı ve Arama İndeksi Derleyicisi
Tüm markdown belgelerini JSON formatında 'data/corpus.json' dosyasına derler.
"""

import os
import glob
import json
import re

def parse_md_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    lines = content.splitlines()
    title = ""
    for line in lines:
        if line.startswith('# '):
            title = line[2:].strip()
            break
            
    if not title:
        title = os.path.splitext(os.path.basename(filepath))[0]
        
    rel_path = os.path.relpath(filepath).replace('\\', '/')
    category = "Genel"
    if "01_teorik-metafizik" in rel_path:
        category = "01. Teorik Metafizik"
    elif "02_birincil-metinler" in rel_path:
        category = "02. Birincil Metinler"
    elif "03_karsilastirmali-felsefe" in rel_path:
        category = "03. Karşılaştırmalı Felsefe"
    elif "04_edebi-ve-kulturel-yansimalar" in rel_path:
        category = "04. Edebi Yansımalar"
    elif "kaynakca" in rel_path:
        category = "05. Kaynakça"
        
    return {
        "id": rel_path,
        "title": title,
        "category": category,
        "path": rel_path,
        "content": content,
        "wordCount": len(re.findall(r'\w+', content))
    }

def build():
    md_files = glob.glob("docs/**/*.md", recursive=True)
    md_files.extend(glob.glob("kaynakca/*.md"))
    md_files.append("README.md")
    
    corpus = []
    for f in sorted(md_files):
        if os.path.exists(f):
            corpus.append(parse_md_file(f))
            
    os.makedirs("data", exist_ok=True)
    out_file = "data/corpus.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(corpus, f, ensure_ascii=False, indent=2)
        
    print(f"[*] Derleme tamamlandı: {len(corpus)} doküman '{out_file}' içerisine kaydedildi.")

if __name__ == "__main__":
    build()
