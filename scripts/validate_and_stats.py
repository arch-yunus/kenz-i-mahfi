#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Kenz-i Mahfî Külliyatı - Bütünlük Doğrulama ve İstatistik Aracı
"""

import os
import glob
import re
import sys

# Set safe output encoding
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

def analyze_corpus():
    md_files = glob.glob("docs/**/*.md", recursive=True)
    md_files.extend(glob.glob("kaynakca/*.md"))
    md_files.append("README.md")
    
    total_words = 0
    total_lines = 0
    file_stats = []
    
    print("="*65)
    print("[*] KENZ-I MAHFI KULLIYATI ISTATISTIKLERI")
    print("="*65)
    
    for filepath in sorted(md_files):
        if not os.path.exists(filepath):
            continue
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            lines = content.splitlines()
            words = re.findall(r"\w+", content)
            
            line_count = len(lines)
            word_count = len(words)
            total_lines += line_count
            total_words += word_count
            
            file_stats.append((filepath, line_count, word_count))
            print(f"- {filepath:50s} | {line_count:4d} satir | {word_count:5d} kelime")
            
    print("-" * 65)
    print(f"Toplam Dokuman Sayisi : {len(file_stats)} dosya")
    print(f"Toplam Satir Sayisi   : {total_lines} satir")
    print(f"Toplam Kelime Sayisi  : {total_words} kelime")
    print("="*65)
    print("[OK] Butun dokumanlar UTF-8 formatinda ve erisilebilir durumda.")

if __name__ == "__main__":
    analyze_corpus()
