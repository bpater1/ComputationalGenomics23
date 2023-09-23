import sys

def build_kmer_index(sequence, k):
    kmer_index = {}
    for i in range(len(sequence) - k + 1):
        kmer = sequence[i:i + k]
        if kmer not in kmer_index:
            kmer_index[kmer] = []
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

def exact_matching(kmer_index, read):
    matches = []
    k = len(list(kmer_index.keys())[0])  # Get k-mer size from the index
    for i in range(len(read) - k + 1):
        kmer = read[i:i + k]
        if kmer in kmer_index:
            matches.extend([pos - i for pos in kmer_index[kmer]])  # Adjust the offsets
    return sorted(matches)

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

        k = 6
        kmer_index = build_kmer_index(genome_sequence, k)
        search_sequence = "ACACAC"  # Specify the search sequence

        with open(fastq_file_name, 'r') as fastq_file:
            reads = parse_fastq(fastq_file)

        total_most_common_offsets = 0  # Initialize a counter for the total most common offsets

        with open(output_file_name, 'w') as output_file:
            for name, read, _ in reads:
                matches = exact_matching(kmer_index, read)
                most_common_offsets = get_most_common_offsets(matches)

                if most_common_offsets:
                    output_file.write("this:{}\n".format(search_sequence))
                    # Write the read sequence
                    output_file.write("{}\n".format(read))
                    # Write the most common offsets
                    output_file.write(",".join(map(str, most_common_offsets)) + "\n")
                    total_most_common_offsets += len(most_common_offsets)  # Update total offsets counter

            # Write the total number of most common offsets at the end of the file
            output_file.seek(0)
            output_file.write("{}\n".format(search_sequence))
            output_file.write("{}\n".format(total_most_common_offsets))

    except FileNotFoundError as e:
        print("Error:", e)
        sys.exit(1)

def get_most_common_offsets(matches):
    offset_counts = {}
    for offset in matches:
        if offset in offset_counts:
            offset_counts[offset] += 1
        else:
            offset_counts[offset] = 1

    if not offset_counts:
        return []  # Return an empty list if there are no matches

    max_count = max(offset_counts.values())
    most_common_offsets = [offset for offset, count in offset_counts.items() if count == max_count]
    return most_common_offsets

if __name__ == "__main__":
    main()
