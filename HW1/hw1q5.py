def translate_rna_codon(codon, genetic_code):
    return genetic_code[codon]

def count_amino_acids(rna_sequence):
    genetic_code = {
        "UUU": "F", "UUC": "F", "UUA": "L", "UUG": "L",
        "UCU": "S", "UCC": "S", "UCA": "S", "UCG": "S",
        "UAU": "Y", "UAC": "Y", "UAA": "", "UAG": "",
        "UGU": "C", "UGC": "C", "UGA": "", "UGG": "W",
        "CUU": "L", "CUC": "L", "CUA": "L", "CUG": "L",
        "CCU": "P", "CCC": "P", "CCA": "P", "CCG": "P",
        "CAU": "H", "CAC": "H", "CAA": "Q", "CAG": "Q",
        "CGU": "R", "CGC": "R", "CGA": "R", "CGG": "R",
        "AUU": "I", "AUC": "I", "AUA": "I", "AUG": "M",
        "ACU": "T", "ACC": "T", "ACA": "T", "ACG": "T",
        "AAU": "N", "AAC": "N", "AAA": "K", "AAG": "K",
        "AGU": "S", "AGC": "S", "AGA": "R", "AGG": "R",
        "GUU": "V", "GUC": "V", "GUA": "V", "GUG": "V",
        "GCU": "A", "GCC": "A", "GCA": "A", "GCG": "A",
        "GAU": "D", "GAC": "D", "GAA": "E", "GAG": "E",
        "GGU": "G", "GGC": "G", "GGA": "G", "GGG": "G"
    }

    amino_acid_counts = {}
    
    for i in range(0, len(rna_sequence), 3):
        codon = rna_sequence[i:i+3]
        amino_acid = translate_rna_codon(codon, genetic_code)
        
        if amino_acid != "" and amino_acid != "M":  # Exclude start and stop codons
            amino_acid_counts[amino_acid] = amino_acid_counts.get(amino_acid, 0) + 1

    sorted_counts = [amino_acid_counts.get(amino_acid, 0) for amino_acid in sorted(genetic_code.values())]
    return sorted_counts

if __name__ == "__main__":
    rna_sequence = input().strip().upper()
    amino_acid_counts = count_amino_acids(rna_sequence)
    
    print(",".join(map(str, amino_acid_counts)))
