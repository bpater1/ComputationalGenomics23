def optimize_mrna_sequence(amino_acid_sequence):
    codon_table = {
        "A": ["GCU", "GCC", "GCA", "GCG"],
        "C": ["UGU", "UGC"],
        "D": ["GAU", "GAC"],
        "E": ["GAA", "GAG"],
        "F": ["UUU", "UUC"],
        "G": ["GGU", "GGC", "GGA", "GGG"],
        "H": ["CAU", "CAC"],
        "I": ["AUU", "AUC", "AUA"],
        "K": ["AAA", "AAG"],
        "L": ["UUA", "UUG", "CUU", "CUC", "CUA", "CUG"],
        "M": ["AUG"],
        "N": ["AAU", "AAC"],
        "P": ["CCU", "CCC", "CCA", "CCG"],
        "Q": ["CAA", "CAG"],
        "R": ["CGU", "CGC", "CGA", "CGG", "AGA", "AGG"],
        "S": ["UCU", "UCC", "UCA", "UCG", "AGU", "AGC"],
        "T": ["ACU", "ACC", "ACA", "ACG"],
        "V": ["GUU", "GUC", "GUA", "GUG"],
        "W": ["UGG"],
        "Y": ["UAU", "UAC"],
    }

    optimized_mrna = ""
    for amino_acid in amino_acid_sequence:
        codons = codon_table.get(amino_acid, [""])  # Get possible codons for the amino acid
        # Choose the codon that maximizes Cs and Gs and is lexicographically first
        optimal_codon = min(codons, key=lambda codon: (-codon.count("C") - codon.count("G"), codon))
        optimized_mrna += optimal_codon

    return optimized_mrna

if __name__ == "__main__":
    amino_acid_sequence = input()
    mRNA_sequence = optimize_mrna_sequence(amino_acid_sequence)
    print(mRNA_sequence)