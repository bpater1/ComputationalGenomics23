import sys

def suffix_prefix_match(str1, str2, min_overlap):
    if len(str2) < min_overlap:
        return 0
    str2_prefix = str2[:min_overlap]
    str1_pos = -1
    while True:
        str1_pos = str1.find(str2_prefix, str1_pos + 1)
        if str1_pos == -1:
            return 0
        str1_suffix = str1[str1_pos:]
        if str2.startswith(str1_suffix):
            return len(str1_suffix)

def make_kmer_table(seqs, k):
    table = {}
    for name, seq in seqs.items():
        for i in range(0, len(seq) - k + 1):
            kmer = seq[i:i+k]
            if kmer not in table:
                table[kmer] = set()
            table[kmer].add(name)
    return table

if len(sys.argv) != 4:
    print("Usage: python3 hw4q2.py input_fastq K output_file")
    sys.exit(1)

input_fastq = sys.argv[1]
K = int(sys.argv[2])
output_file = sys.argv[3]

reads = {}
current_read = None

with open(input_fastq, 'r') as file:
    for line in file:
        if line.startswith('@'):
            current_read = line.strip()
        else:
            reads[current_read] = line.strip()

kmer_table = make_kmer_table(reads, K)

with open(output_file, 'w') as output:
    for read_name, read_seq in reads.items():
        kmer = read_seq[:K]
        potential_matches = set()
        if kmer in kmer_table:
            potential_matches = kmer_table[kmer]
        
        best_match = None
        max_overlap = 0

        for match_name in potential_matches:
            if match_name != read_name:
                overlap = suffix_prefix_match(read_seq, reads[match_name], K)
                if overlap > max_overlap:
                    max_overlap = overlap
                    best_match = match_name
        
        if best_match:
            output.write(f"{read_name[1:]} {max_overlap} {best_match[1:]}\n")

print("Done.")
