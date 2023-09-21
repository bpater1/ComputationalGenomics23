# If more than 1 read has the highest or lowest quality, give the one that occurs first in the file.

# (a) The read that has the lowest total quality score (1=first read, 2=second read, etc)
# (b) The read that has the highest total quality score
# (c) The total number of base quality values (denoted Q in lecture) less than 10.
# (d) The total number of base quality values ≥ 30
# (e) Total number of characters observed in the read sequences of the file other than A, C, G, or T

from io import StringIO
import sys

# got parse_fastq function code from https://nbviewer.org/github/BenLangmead/comp-genomics-class/blob/master/notebooks/FASTQ.ipynb, linked in HW
def parse_fastq(fh):
        # """ Parse reads from a FASTQ filehandle.  For each read, we
        # return a name, nucleotide-string, quality-string triple. """
    reads = []
    while True:
        first_line = fh.readline()
        if len(first_line) == 0:
            break  # end of file
        name = first_line[1:].rstrip()
        seq = fh.readline().rstrip()
        fh.readline()  # ignore line starting with +
        qual = fh.readline().rstrip()
        reads.append((name, seq, qual))
    return reads

def calculate_statistics(reads):
    # initialize the variables
    lowest_quality_read_index = None
    highest_quality_read_index = None
    total_quality_less_than_10 = 0
    total_quality_greater_than_equal_to_30 = 0
    total_non_ACGT_characters = 0

    for i, (_, _, qual) in enumerate(reads):
        # Calculate total quality
        total_quality = sum(ord(q) - 33 for q in qual)
        
        if lowest_quality_read_index is None or total_quality < lowest_quality_read_index[0]:
            lowest_quality_read_index = (total_quality, i + 1)
        if highest_quality_read_index is None or total_quality > highest_quality_read_index[0]:
            highest_quality_read_index = (total_quality, i + 1)

        # Calculate total quality values less than 10 and greater than or equal to 30
        total_quality_less_than_10 += sum(1 for q in qual if ord(q) - 33 < 10)
        total_quality_greater_than_equal_to_30 += sum(1 for q in qual if ord(q) - 33 >= 30)
        
        # Calculate total non-ACGT characters
        total_non_ACGT_characters += sum(1 for base in reads[i][1] if base not in "ACGT")

    return lowest_quality_read_index[1], highest_quality_read_index[1], total_quality_less_than_10, total_quality_greater_than_equal_to_30, total_non_ACGT_characters

if __name__ == "__main__":
    # make sure you have the correct number of arguments
    if len(sys.argv) != 3:
        print("Usage: {} <input_fastq_file> <output_summary_file>".format(sys.argv[0]))
        sys.exit(1)

    input_fastq_file = sys.argv[1]
    output_summary_file = sys.argv[2]

    try:
        with open(input_fastq_file, 'r') as fastq_file:
            reads = parse_fastq(fastq_file)
        
        # Calculate summary statistics
        lowest_quality, highest_quality, total_quality_lt_10, total_quality_ge_30, total_non_ACGT = calculate_statistics(reads)

        # Write the summary statistics to the output file
        with open(output_summary_file, 'w') as summary_file:
            summary_file.write("{} {} {} {} {}".format(
                lowest_quality, highest_quality, total_quality_lt_10, total_quality_ge_30, total_non_ACGT
            ))

    except FileNotFoundError:
        print("Error: Input FASTQ file not found.")
        sys.exit(1)
