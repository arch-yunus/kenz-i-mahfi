#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Kenz-i Mahfî Külliyatı - Gelişmiş Bütünlük Doğrulama, Link Kontrolü ve İstatistik Aracı
"""

import os
import glob
import re
import sys

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
    broken_links = []
    broken_images = []
    
    # Key concept frequency tracker
    concept_freq = {
        "Kenz-i Mahfî / Gizli Hazine": 0,
        "Vücûd / Varlık": 0,
        "Tecellî": 0,
        "Muhabbet / Aşk": 0,
        "İnsân-ı Kâmil": 0,
        "A'yân-ı Sâbite": 0,
        "Nefes-i Rahmânî": 0,
        "Ahadiyyet / Vâhidiyyet": 0
    }
    
    print("=" * 75)
    print("✨ KENZ-İ MAHFÎ KÜLLİYATI DETAYLI BÜTÜNLÜK VE İSTATİSTİK RAPORU")
    print("=" * 75)
    
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
            print(f"- {filepath:55s} | {line_count:4d} satır | {word_count:5d} kelime")
            
            # Check concept frequencies (case-insensitive & accent-relaxed)
            lower_c = content.lower()
            if "kenz" in lower_c or "mahfi" in lower_c or "hazine" in lower_c:
                concept_freq["Kenz-i Mahfî / Gizli Hazine"] += len(re.findall(r'kenz|hazine', lower_c))
            if "vücud" in lower_c or "vucud" in lower_c or "varlık" in lower_c:
                concept_freq["Vücûd / Varlık"] += len(re.findall(r'vüc[uû]d|varl[ıi]k', lower_c))
            if "tecelli" in lower_c:
                concept_freq["Tecellî"] += len(re.findall(r'tecell[iî]', lower_c))
            if "muhabbet" in lower_c or "aşk" in lower_c or "ask" in lower_c:
                concept_freq["Muhabbet / Aşk"] += len(re.findall(r'muhabbet|a[sş]k', lower_c))
            if "kâmil" in lower_c or "kamil" in lower_c:
                concept_freq["İnsân-ı Kâmil"] += len(re.findall(r'ins[aâ]n-?[ıi]\s*k[aâ]mil', lower_c))
            if "a'yân" in lower_c or "ayan" in lower_c:
                concept_freq["A'yân-ı Sâbite"] += len(re.findall(r'a.?y[aâ]n', lower_c))
            if "nefes" in lower_c:
                concept_freq["Nefes-i Rahmânî"] += len(re.findall(r'nefes-?i\s*rahm[aâ]n', lower_c))
            if "ahadiyyet" in lower_c or "vahidiyyet" in lower_c:
                concept_freq["Ahadiyyet / Vâhidiyyet"] += len(re.findall(r'ahadiyyet|v[aâ]hidiyyet', lower_c))
                
            # Check relative markdown links
            dir_path = os.path.dirname(filepath)
            links = re.findall(r'\[.*?\]\((?!http|#|mailto:)(.*?)\)', content)
            for link in links:
                target_link = link.split('#')[0]
                if not target_link:
                    continue
                target_path = os.path.normpath(os.path.join(dir_path, target_link))
                if not os.path.exists(target_path):
                    broken_links.append((filepath, link, target_path))
                    
            # Check image links
            images = re.findall(r'!\[.*?\]\((?!http)(.*?)\)', content)
            for img in images:
                target_path = os.path.normpath(os.path.join(dir_path, img))
                if not os.path.exists(target_path):
                    broken_images.append((filepath, img))
                    
    print("-" * 75)
    print(f"📊 Toplam Doküman Sayısı : {len(file_stats)} dosya")
    print(f"📊 Toplam Satır Sayısı   : {total_lines:,} satır")
    print(f"📊 Toplam Kelime Sayısı  : {total_words:,} kelime")
    print("-" * 75)
    print("🔑 TEMEL İRFÂNÎ KAVRAM FREKANSLARI:")
    for concept, count in concept_freq.items():
        print(f"  • {concept:32s}: {count:4d} kez geçiyor")
    print("-" * 75)
    
    if broken_links:
        print(f"⚠️  UYARI: {len(broken_links)} Kırık Link Tespit Edildi:")
        for source, link, target in broken_links:
            print(f"   Kaynak: {source} -> Link: {link}")
    else:
        print("✅ [OK] Bütün göreceli markdown bağlantıları geçerli.")
        
    if broken_images:
        print(f"⚠️  UYARI: {len(broken_images)} Eksik Görsel Tespit Edildi:")
        for source, img in broken_images:
            print(f"   Kaynak: {source} -> Görsel: {img}")
    else:
        print("✅ [OK] Bütün görsel dosyaları eksiksiz ve mevcut.")
        
    print("=" * 75)
    print("✨ Bütünlük ve istatistik doğrulaması başarıyla tamamlandı.")

if __name__ == "__main__":
    analyze_corpus()
