import sys

# Function to generate the suffix array using radix sort
def build_suffix_array(s):
    n = len(s)
    suffixes = [(s[i:], i) for i in range(n)]
    suffixes.sort()
    return [suffix[1] for suffix in suffixes]

def calculate_bwt_with_indices(input_string, suffix_array):
    n = len(input_string)
    bwt = []
    indices = []

    for i in suffix_array:
        char = input_string[i - 1]
        if ((i - 1) == -1):
            i = n 
        indices.append(i - 1)
        bwt.append(char)
    return "".join(bwt), indices



if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 hw3q3.py input.txt output.txt")
        sys.exit(1)

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    with open(input_filename, "r") as input_file, open(output_filename, "w") as output_file:
        input_string = input_file.readline().strip()

        # Ensure the input string ends with a '$' character
        if input_string[-1] != '$':
            input_string += '$'

        # Build the suffix array
        suffix_array = build_suffix_array(input_string)

        # Calculate BWT
        bwt, original_indices = calculate_bwt_with_indices(input_string, suffix_array)
        output_file.write(" ".join(map(str, original_indices)) + "\n")