#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Kenz-i Mahfî Külliyatı - Gelişmiş Web Veritabanı ve Arama İndeksi Derleyicisi
Tüm markdown belgelerini zengin meta verileriyle (TOC, okuma süresi, kategoriler) 'data/corpus.json' ve 'data/glossary.json' dosyalarına derler.
"""

import os
import glob
import json
import re
import math

def extract_headings(content):
    headings = []
    for line in content.splitlines():
        if line.startswith('## '):
            headings.append({"level": 2, "text": line[3:].strip()})
        elif line.startswith('### '):
            headings.append({"level": 3, "text": line[4:].strip()})
    return headings

def extract_glossary(content):
    glossary = []
    lines = content.splitlines()
    for line in lines:
        line = line.strip()
        if line.startswith('* **'):
            p1 = line.find('**', 4)
            if p1 != -1:
                term_full = line[4:p1].strip()
                rest = line[p1+2:].strip()
                if rest.startswith(':'):
                    rest = rest[1:].strip()
                
                term_name = term_full
                term_alt = ""
                if "(" in term_full and ")" in term_full:
                    parts = term_full.split("(", 1)
                    term_name = parts[0].strip()
                    term_alt = parts[1].replace(")", "").strip()
                    
                glossary.append({
                    "term": term_name,
                    "alt": term_alt,
                    "definition": rest
                })
    return glossary

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
    category = "00. Genel"
    
    if "01_teorik-metafizik" in rel_path:
        category = "01. Teorik Metafizik"
    elif "02_birincil-metinler" in rel_path:
        category = "02. Birincil Metinler"
    elif "03_karsilastirmali-felsefe" in rel_path:
        category = "03. Karşılaştırmalı Felsefe"
    elif "04_edebi-ve-kulturel-yansimalar" in rel_path:
        category = "04. Edebi Yansımalar"
    elif "05_tasavvufi-terimler-sozlugu" in rel_path:
        category = "05. Istılâhât & Lügat"
    elif "kaynakca" in rel_path:
        category = "06. Kaynakça"
    elif "README.md" in rel_path:
        category = "00. Külliyat Takdimi"
        
    words = re.findall(r'\w+', content)
    word_count = len(words)
    reading_time_min = max(1, math.ceil(word_count / 180))
    
    # Extract tags
    tags = []
    lower_c = content.lower()
    if "hadis" in lower_c or "rivayet" in lower_c:
        tags.append("Hadis")
    if "ontoloji" in lower_c or "vücûd" in lower_c or "vucud" in lower_c:
        tags.append("Ontoloji")
    if "muhabbet" in lower_c or "aşk" in lower_c or "ask" in lower_c:
        tags.append("Aşk & Muhabbet")
    if "felsefe" in lower_c or "spinoza" in lower_c or "hegel" in lower_c:
        tags.append("Mukayese")
    if "şiir" in lower_c or "divan" in lower_c or "gazel" in lower_c:
        tags.append("Edebiyat")
        
    headings = extract_headings(content)
    
    return {
        "id": rel_path,
        "title": title,
        "category": category,
        "path": rel_path,
        "content": content,
        "wordCount": word_count,
        "readingTime": f"{reading_time_min} dk okuma",
        "tags": list(set(tags)),
        "headings": headings
    }

def build():
    md_files = glob.glob("docs/**/*.md", recursive=True)
    md_files.extend(glob.glob("kaynakca/*.md"))
    md_files.append("README.md")
    
    corpus = []
    glossary_items = []
    
    for f in sorted(md_files):
        if os.path.exists(f):
            doc = parse_md_file(f)
            corpus.append(doc)
            
            if "05_tasavvufi-terimler-sozlugu" in f or "istilahat" in f.lower():
                glossary_items.extend(extract_glossary(doc["content"]))
                
    os.makedirs("data", exist_ok=True)
    
    out_file = "data/corpus.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(corpus, f, ensure_ascii=False, indent=2)
        
    out_glossary = "data/glossary.json"
    with open(out_glossary, "w", encoding="utf-8") as f:
        json.dump(glossary_items, f, ensure_ascii=False, indent=2)
        
    print(f"[*] Derleme tamamlandı: {len(corpus)} doküman '{out_file}' içerisine kaydedildi.")
    print(f"[*] Sözlük derlendi: {len(glossary_items)} kavram '{out_glossary}' içerisine kaydedildi.")

if __name__ == "__main__":
    build()
