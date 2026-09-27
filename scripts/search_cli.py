#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Kenz-i Mahfî Külliyatı - Gelişmiş Kavram ve Metin Arama Motoru CLI
Akıllı normalizasyon, renkli terminal vurgulama, kategori filtreleme ve istatistik destekli.
"""

import os
import sys
import glob
import re
import unicodedata
import argparse

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# ANSI Escape Colors
GOLD = "\033[38;2;212;175;55m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"

def normalize_text(text):
    norm = unicodedata.normalize('NFD', text)
    norm = "".join(c for c in norm if unicodedata.category(c) != 'Mn')
    replacements = {
        'ı': 'i', 'İ': 'I', 'ş': 's', 'Ş': 'S', 
        'ğ': 'g', 'Ğ': 'G', 'ç': 'c', 'Ç': 'C', 
        'ö': 'o', 'Ö': 'O', 'ü': 'u', 'Ü': 'U'
    }
    for k, v in replacements.items():
        norm = norm.replace(k, v)
    return norm.lower()

def search_corpus(query, category_filter=None, base_dir="."):
    files = glob.glob(os.path.join(base_dir, "docs", "**", "*.md"), recursive=True)
    files.append(os.path.join(base_dir, "README.md"))
    files.extend(glob.glob(os.path.join(base_dir, "kaynakca", "*.md")))
    
    norm_query = normalize_text(query)
    results = []
    
    for filepath in sorted(files):
        if not os.path.exists(filepath):
            continue
            
        rel_path = os.path.relpath(filepath, base_dir).replace('\\', '/')
        if category_filter and category_filter.lower() not in rel_path.lower():
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
                results.append((rel_path, matched_lines))
        except Exception:
            pass
            
    return results

def highlight_term(line, query):
    norm_query = normalize_text(query)
    norm_line = normalize_text(line)
    
    idx = norm_line.find(norm_query)
    if idx != -1:
        start_orig = idx
        end_orig = idx + len(query)
        # Attempt safe replacement
        return line[:start_orig] + f"{BOLD}{GOLD}" + line[start_orig:end_orig] + f"{RESET}" + line[end_orig:]
    return line

def display_results(query, results):
    print("\n" + "=" * 75)
    print(f"{BOLD}{GOLD}✨ ARAMA SONUÇLARI:{RESET} '{query}' ({len(results)} dokümanda eşleşti)")
    print("=" * 75)
    
    if not results:
        print(f"{YELLOW}[-] Eşleşen sonuç bulunamadı.{RESET}\n")
        return
        
    total_matches = sum(len(m) for _, m in results)
    print(f"{DIM}Toplam {total_matches} eşleşme bulundu.{RESET}\n")
    
    for rel_path, matches in results:
        print(f"{BOLD}{CYAN}📄 {rel_path}{RESET} {GREEN}({len(matches)} eşleşme){RESET}")
        print(f"{DIM}" + "─" * 60 + f"{RESET}")
        for line_num, text in matches[:5]:
            highlighted = highlight_term(text, query)
            print(f"  {DIM}[Satır {line_num:4d}]:{RESET} {highlighted}")
        if len(matches) > 5:
            print(f"  {DIM}... ve {len(matches) - 5} satır daha.{RESET}")
        print()
    print("=" * 75 + "\n")

def interactive_mode():
    print(f"{BOLD}{GOLD}=========================================================={RESET}")
    print(f"{BOLD}✨ KENZ-İ MAHFÎ KÜLLİYATI AKILLI ARAMA MOTORU ✨{RESET}")
    print("Çıkmak için 'q' veya 'exit' yazınız.")
    print("=" * 58)
    while True:
        try:
            query = input(f"{BOLD}{CYAN}Aramak istediğiniz kavram / kelime:{RESET} ").strip()
            if not query:
                continue
            if query.lower() in ["q", "exit", "quit", "cikis", "çıkış"]:
                print(f"{GOLD}Kenz-i Mahfî külliyatında iyi okumalar dileriz.{RESET}")
                break
            results = search_corpus(query)
            display_results(query, results)
        except (KeyboardInterrupt, EOFError):
            print("\nProgram sonlandırıldı.")
            break

def main():
    parser = argparse.ArgumentParser(description="Kenz-i Mahfî Külliyatı Metin Arama Motoru")
    parser.add_argument("query", nargs="*", help="Aramak istediğiniz kavram")
    parser.add_argument("-c", "--category", help="Kategori filtresi (örn: 'teorik', 'birincil', 'felsefe')")
    parser.add_argument("-i", "--interactive", action="store_true", help="Etkileşimli arama modunu başlat")
    
    args = parser.parse_args()
    
    if args.interactive or not args.query:
        interactive_mode()
    else:
        query_str = " ".join(args.query)
        results = search_corpus(query_str, category_filter=args.category)
        display_results(query_str, results)

if __name__ == "__main__":
    main()
