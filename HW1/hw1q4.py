def reverse_complement(dna):
    complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    return ''.join(complement[base] for base in dna[::-1])

def generate_palindromes(n):
    palindromes = set()
    bases = 'ACGT'

    def generate(palindrome):
        if len(palindrome) <= n:
            rc = reverse_complement(palindrome)
            if palindrome == rc:
                palindromes.add(palindrome)
            for base in bases:
                generate(palindrome + base)

    generate('')
    return sorted(palindromes)

if __name__ == "__main__":
    n = int(input())
    palindromes = generate_palindromes(n)
    for palindrome in palindromes:
        print(palindrome)