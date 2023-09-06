def reverse_complement(dna):
    complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    return ''.join(complement[base] for base in dna[::-1])

if __name__ == "__main__":
    dna_input = input().strip()
    dna_cleaned = ''.join(base for base in dna_input if base in 'ACTG')
    reverse_comp = reverse_complement(dna_cleaned)
    print(reverse_comp)