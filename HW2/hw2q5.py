import sys
from collections import defaultdict

def calculate_total_weight(quals):
    return sum(ord(qual) - 33 for qual in quals)

def main():
    if len(sys.argv) != 4:
        print("Usage: python hw2q5.py <reference.fasta> <reads.fastq> <output.txt>")
        sys.exit(1)

    reference_file = sys.argv[1]
    reads_file = sys.argv[2]
    output_file = sys.argv[3]

    with open(reference_file, 'r') as ref_f:
        reference = "".join(line.strip() for line in ref_f if not line.startswith('>'))

    k = 30  # Length of the reads
    kmer_index = defaultdict(list)

    # Create a k-mer index of the reference genome
    for i in range(len(reference) - k + 1):
        kmer = reference[i:i + k]
        kmer_index[kmer].append(i)

    locus_data = defaultdict(lambda: {'base_counts': defaultdict(int)})

    with open(reads_file, 'r') as reads_f:
        for line in reads_f:
            if line.startswith('@'):
                read_name = line.strip()
                read_seq = next(reads_f).strip()
                _ = next(reads_f)  # skip '+'
                read_quals = next(reads_f).strip()

                for i in range(len(read_seq) - k + 1):
                    kmer = read_seq[i:i + k]
                    if kmer in kmer_index:
                        for locus_position in kmer_index[kmer]:
                            for j in range(k):
                                locus_data[locus_position + j]['base_counts'][read_seq[i + j]] += calculate_total_weight(read_quals)

    v_loci = []

    v_loci_data = []

    with open(output_file, 'w') as output_f:
        for locus_position, locus_info in sorted(locus_data.items()):
            locus_reference_base = reference[locus_position]
            base_counts = locus_info['base_counts']

            # Skip loci with no alternative bases
            if len(base_counts) <= 1:
                continue

            base_weight_pairs = [f"{base}:{calculate_total_weight(quals)}" for base, quals in base_counts.items()]
            locus_line = f"{locus_position},{locus_reference_base},"
            locus_line += f"{','.join(base_weight_pairs)}\n"
            v_loci_data.append(locus_line)
            v_loci.append(locus_position)

    n_count = len(reference) - len(v_loci)  # Number of N loci
    m_count = 0  # Number of M loci
    v_count = len(v_loci)  # Number of V loci

    with open(output_file, 'w') as output_f:
        output_f.writelines(v_loci_data)
        output_f.write(f"{n_count},{m_count},{v_count}\n")

if __name__ == "__main__":
    main()
