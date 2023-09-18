def hamming_distance(str1, str2):
    if len(str1) != len(str2):
        raise ValueError("Input strings must have the same length")
    
    distance = 0
    for i in range(len(str1)):
        if str1[i] != str2[i]:
            distance += 1
    return distance

import sys

# Read input DNA strings
a = sys.stdin.readline().strip()
b = sys.stdin.readline().strip()

# Calculate Hamming distance and write the result to standard output
sys.stdout.write(f'{hamming_distance(a, b)}\n')