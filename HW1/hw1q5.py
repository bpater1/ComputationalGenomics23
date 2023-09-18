def translate_rna_codon(codon, codon_table):
    for amino_acid, codons in codon_table.items():
        if codon in codons:
            return amino_acid
    return None

def count_amino_acids(rna_sequence, codon_table):
    amino_acid_counts = {amino_acid: 0 for amino_acid in codon_table.keys()}
    codon_length = 3

    for i in range(0, len(rna_sequence), codon_length):
        codon = rna_sequence[i:i + codon_length]
        amino_acid = translate_rna_codon(codon, codon_table)
        if amino_acid is not None:
            amino_acid_counts[amino_acid] += 1

    return amino_acid_counts

if __name__ == "__main__":
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

    rna_sequence = input().upper()
    amino_acid_counts = count_amino_acids(rna_sequence, codon_table)

    counts = [amino_acid_counts[acid] for acid in codon_table.keys()]
    result = ",".join(map(str, counts))

    print(result)