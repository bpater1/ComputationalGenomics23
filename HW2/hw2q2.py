import sys

def build_kmer_index(sequence, k):
    kmer_index = {}  # Initialize an empty k-mer index as a dictionary
    total_kmers = 0  # Initialize a counter for total k-mers
    
    for i in range(len(sequence) - k + 1):
        kmer = sequence[i:i + k]
        
        if kmer not in kmer_index:
            kmer_index[kmer] = i  # Store the 0-based offset of the k-mer
            total_kmers += 1
    
    return total_kmers, kmer_index

if __name__ == "__main__":
    # make sure we have epected number of command line arguments
    if len(sys.argv) != 4:
        print("Usage: {} <fasta_file> <k_file> <output_file>".format(sys.argv[0]))
        sys.exit(1)

    fasta_file = sys.argv[1]
    k_file = sys.argv[2]
    output_file = sys.argv[3]

    # Read the value of k from the k_file
    try:
        with open(k_file, 'r') as k_file_handle:
            k = int(k_file_handle.read())
    except FileNotFoundError:
        print("Error: k file not found.")
        sys.exit(1)
    except ValueError:
        print("Error: Invalid k value in the k file.")
        sys.exit(1)

    # Read the FASTA file
    try:
        with open(fasta_file, 'r') as fasta_file_handle:
            header = fasta_file_handle.readline().strip()  # Read the header line
            sequence = "".join(line.strip() for line in fasta_file_handle)  # Read the sequence
    except FileNotFoundError:
        print("Error: FASTA file not found.")
        sys.exit(1)

    # Build the k-mer index and get the total number of keys
    total_kmers, kmer_index = build_kmer_index(sequence, k)

    # Write the total number of keys to the output file
    try:
        with open(output_file, 'w') as output_file_handle:
            output_file_handle.write(str(total_kmers))
    except FileNotFoundError:
        print("Error: Output file not found.")
        sys.exit(1)