import sys
from collections import defaultdict

def calculate_total_weight(quals):
    return sum(ord(qual) - 33 for qual in quals)

def categorize_locus(reference_base, base_counts):
    sorted_base_counts = sorted(base_counts.items())
    return sorted_base_counts

def main():
    if len(sys.argv) != 4:
        print("Usage: python hw2q5.py <reference.fasta> <reads.fastq> <output.txt>")
        sys.exit(1)

    reference_file = sys.argv[1]
    reads_file = sys.argv[2]
    output_file = sys.argv[3]

    reference = ""
    with open(reference_file, 'r') as ref_f:
        for line in ref_f:
            if not line.startswith('>'):
                reference += line.strip()

    k = 30  # Length of the reads
    kmer_index = defaultdict(list)

    # Create a k-mer index of the reference genome
    for i in range(len(reference) - k + 1):
        kmer = reference[i:i + k]
        kmer_index[kmer].append(i)

    locus_data = {}

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
                            if locus_position not in locus_data:
                                locus_data[locus_position] = {'reference_base': reference[locus_position], 'base_counts': defaultdict(int)}
                            for j in range(k):
                                if reference[locus_position + j] != read_seq[i + j]:
                                    locus_data[locus_position]['base_counts'][read_seq[i + j]] += calculate_total_weight(read_quals)

    n_count = 0
    m_count = 0
    v_count = 0
    all_bases = set()

    with open(output_file, 'w') as output_f:
        for locus_position, locus_info in sorted(locus_data.items()):
            locus_reference_base = locus_info['reference_base']
            locus_bases_and_weights = categorize_locus(locus_reference_base, locus_info['base_counts'])

            if locus_position == 0:
                locus_label = 'N'
                n_count += 1
            elif all(base == locus_reference_base for base, _ in locus_bases_and_weights):
                locus_label = 'M'
                m_count += 1
            else:
                locus_label = 'V'
                v_count += 1

            output_f.write(f"{locus_position},{locus_reference_base},")

            # Collect all bases for sorting
            for base, weight in locus_bases_and_weights:
                all_bases.add(base)

            # Sort bases alphabetically
            sorted_bases_and_weights = sorted(locus_bases_and_weights, key=lambda x: x[0])

            output_f.write(','.join([f"{base}:{weight}" for base, weight in sorted_bases_and_weights]))
            output_f.write('\n')

    with open(output_file, 'a') as output_f:
        output_f.write(f"{n_count},{m_count},{v_count}\n")

if __name__ == "__main__":
    main()
