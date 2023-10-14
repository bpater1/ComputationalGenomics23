import sys

# Function to generate the suffix array using radix sort
def build_suffix_array(s):
    n = len(s)
    suffixes = [(s[i:], i) for i in range(n)]
    suffixes.sort()
    return [suffix[1] for suffix in suffixes]

# Function to calculate BWT from the input string and suffix array
def calculate_bwt(input_string, suffix_array):
    bwt = [input_string[i - 1] for i in suffix_array]
    print(bwt)
    return "".join(bwt)

# Function to calculate BWT run-length and length of longest run
def calculate_run_length(bwt):
    run_length = 1
    max_run_length = 1
    num_runs = 1

    for i in range(1, len(bwt)):
        if bwt[i] == bwt[i - 1]:
            run_length += 1
        else:
            num_runs += 1
            max_run_length = max(max_run_length, run_length)
            run_length = 1

    return num_runs, max_run_length

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 hw3q2.py input.txt output.txt")
        sys.exit(1)

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    with open(input_filename, "r") as input_file, open(output_filename, "w") as output_file:
        input_string = input_file.readline().strip()

        suffix_array = build_suffix_array(input_string)
        bwt = calculate_bwt(input_string, suffix_array)

        # Calculate BWT number of runs and length of longest run
        num_runs, max_run_length = calculate_run_length(bwt)

        # Write results to the output file
        output_file.write(bwt + "\n")
        output_file.write(str(num_runs) + "\n")
        output_file.write(str(max_run_length) + "\n")