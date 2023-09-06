def reverse_complement(dna):
    complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    return ''.join(complement[base] for base in dna[::-1])


def generate_palindromes(sequence, n, length):
    if length > n:
        return
    
    reverse_comp = reverse_complement(sequence)
    
    if sequence == reverse_comp:
        print(sequence)
    
    for base in "ACGT":
        if base not in sequence:
            generate_palindromes(sequence + base, n, length + 1)


def find_palindromes(n):
    for base in "ACGT":
        generate_palindromes(base, n, 1)


if __name__ == "__main__":
    n = int(input())
    find_palindromes(n)
