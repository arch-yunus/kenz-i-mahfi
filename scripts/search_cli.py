#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Kenz-i Mahfî Külliyatı - Metin ve Kavram Arama CLI Aracı (Akıllı Normalizasyon Destekli)
"""

import os
import sys
import glob
import re
import unicodedata

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

def normalize_text(text):
    # Normalize accents (â -> a, î -> i, û -> u, etc.)
    norm = unicodedata.normalize('NFD', text)
    norm = "".join(c for c in norm if unicodedata.category(c) != 'Mn')
    # Custom replacements
    replacements = {'ı': 'i', 'İ': 'I', 'ş': 's', 'Ş': 'S', 'ğ': 'g', 'Ğ': 'G', 'ç': 'c', 'Ç': 'C', 'ö': 'o', 'Ö': 'O', 'ü': 'u', 'Ü': 'U'}
    for k, v in replacements.items():
        norm = norm.replace(k, v)
    return norm.lower()

def search_corpus(query, base_dir="."):
    docs_pattern = os.path.join(base_dir, "docs", "**", "*.md")
    files = glob.glob(docs_pattern, recursive=True)
    
    files.append(os.path.join(base_dir, "README.md"))
    files.extend(glob.glob(os.path.join(base_dir, "kaynakca", "*.md")))
    
    norm_query = normalize_text(query)
    results = []
    
    for filepath in files:
        if not os.path.exists(filepath):
            continue
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.read().splitlines()
                
            matched_lines = []
            for idx, line in enumerate(lines, 1):
                norm_line = normalize_text(line)
                if norm_query in norm_line:
                    matched_lines.append((idx, line.strip()))
                    
            if matched_lines:
                results.append((filepath, matched_lines))
        except Exception:
            pass
            
    return results

def display_results(query, results):
    print("\n" + "="*70)
    print(f"[*] ARAMA SONUCLARI: '{query}' ({len(results)} dosyada bulundu)")
    print("="*70)
    
    if not results:
        print("[-] Eslesen sonuc bulunamadi.\n")
        return
        
    for filepath, matches in results:
        rel_path = os.path.relpath(filepath)
        print(f"\n[+] Dosya: {rel_path} ({len(matches)} eslesme)")
        print("-" * 50)
        for line_num, text in matches[:5]:
            print(f"  [Satir {line_num:3d}]: {text}")
        if len(matches) > 5:
            print(f"  ... ve {len(matches) - 5} satir daha.")
    print("\n" + "="*70 + "\n")

def interactive_mode():
    print("==========================================================")
    print("KENZ-I MAHFI KULLIYATI ARAMA MOTORU")
    print("Cikmak icin 'q' veya 'exit' yazin.")
    print("==========================================================")
    while True:
        try:
            query = input("Aramak istediginiz kavram / kelime: ").strip()
            if not query:
                continue
            if query.lower() in ["q", "exit", "quit", "cikis"]:
                print("Iyi calismalar dileriz.")
                break
            results = search_corpus(query)
            display_results(query, results)
        except (KeyboardInterrupt, EOFError):
            print("\nProgram sonlandirildi.")
            break

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] in ["-i", "--interactive"]:
            interactive_mode()
        else:
            query = " ".join(sys.argv[1:])
            results = search_corpus(query)
            display_results(query, results)
    else:
        interactive_mode()

if __name__ == "__main__":
    main()
