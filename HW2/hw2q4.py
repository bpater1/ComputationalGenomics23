import sys
from collections import defaultdict

def build_kmer_index(sequence, k):
    kmer_index = defaultdict(list)
    for i in range(len(sequence) - k + 1):
        kmer = sequence[i:i + k]
        kmer_index[kmer].append(i)
    return kmer_index

def parse_fastq(fh):
    reads = []
    while True:
        first_line = fh.readline()
        if len(first_line) == 0:
            break
        name = first_line[1:].rstrip()
        seq = fh.readline().rstrip()
        fh.readline()  # ignore line starting with '+'
        qual = fh.readline().rstrip()
        reads.append((name, seq, qual))
    return reads

def hamming_distance(str1, str2):
    return sum(ch1 != ch2 for ch1, ch2 in zip(str1, str2))

def approximate_matching(kmer_index, read, max_mismatches, k):
    read_length = len(read)
    partitions = [read[i:i + k] for i in range(0, read_length, k)]
    
    partition_counts = [0] * (max_mismatches + 1)
    partition_offsets = [[] for _ in range(max_mismatches + 1)]
    
    for partition in partitions:
        hits = kmer_index.get(partition, [])
        for hit in hits:
            mismatches = hamming_distance(partition, read[hit:hit + len(partition)])
            if mismatches <= max_mismatches:
                partition_counts[mismatches] += 1
                if mismatches == 0:
                    partition_offsets[mismatches].append(hit)
    
    result = []
    for i in range(max_mismatches + 1):
        result.append(partition_counts[i])
        if i == 0:
            if partition_offsets[i]:
                result.append(':'.join(map(str, sorted(set(partition_offsets[i])))))
            else:
                result.append('')
        else:
            if partition_offsets[i]:
                result.append(f"{i}:{','.join(map(str, sorted(set(partition_offsets[i]))))}")
            else:
                result.append('')

    return ' '.join(map(str, result))

def main():
    if len(sys.argv) != 4:
        print("Usage: {} <fasta_file> <fastq_file> <output_file>".format(sys.argv[0]))
        sys.exit(1)

    fasta_file_name = sys.argv[1]
    fastq_file_name = sys.argv[2]
    output_file_name = sys.argv[3]

    try:
        with open(fasta_file_name, 'r') as fasta_file:
            genome_sequence = "".join(line.strip() for line in fasta_file if not line.startswith('>'))

        k = 6  # k-mer length, adjust as needed
        max_mismatches = 4
        kmer_index = build_kmer_index(genome_sequence, k)

        with open(fastq_file_name, 'r') as fastq_file:
            reads = parse_fastq(fastq_file)

        with open(output_file_name, 'w') as output_file:
            for _, read, _ in reads:
                result = approximate_matching(kmer_index, read, max_mismatches, k)
                output_file.write(result + '\n')

    except FileNotFoundError as e:
        print("Error:", e)
        sys.exit(1)

if __name__ == "__main__":
    main()