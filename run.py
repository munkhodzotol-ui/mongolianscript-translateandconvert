import json
import os

input_file = "lyrics-bichig2cryllic.txt"
output_file = "dictionary_clean.json"

if not os.path.exists(input_file):
    print(f"[!] File '{input_file}' not found in this folder.")
else:
    print(f"[*] Reading and parsing '{input_file}'...")
    dictionary = {}
    with open(input_file, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if "|" in line:
                parts = line.split("|")
                cyr_words = parts[0].strip().split()
                bic_words = parts[1].strip().split()
                if len(cyr_words) == len(bic_words):
                    for c, b in zip(cyr_words, bic_words):
                        dictionary[c.strip().lower()] = b.strip()

    with open(output_file, "w", encoding="utf-8") as out:
        json.dump(dictionary, out, ensure_ascii=False, indent=2)

    print(f"[✓] SUCCESS! Extracted {len(dictionary):,} unique word pairs into '{output_file}'!")