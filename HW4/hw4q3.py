import sys

def find_unitigs(input_file, output_file):
    # Read the "best unambiguous match to the right" information from the input file
    matches = {}
    with open(input_file, 'r') as file:
        for line in file:
            parts = line.strip().split()
            read_id, overlap, match_id = parts[0], int(parts[1]), parts[2]
            if match_id not in matches:
                matches[match_id] = {'BMR': [], 'BML': []}
            matches[match_id]['BMR'].append((read_id, overlap))
            if read_id not in matches:
                matches[read_id] = {'BMR': [], 'BML': []}
            matches[read_id]['BML'].append((match_id, overlap))

    unitigs = []

    def find_unitig(start_read):
        unitig = [start_read]
        while start_read in matches:
            matches[start_read]['BMR'].sort(key=lambda x: -x[1])
            next_read, overlap = matches[start_read]['BMR'][0]
            del matches[start_read]
            if next_read in matches and (start_read, overlap) in matches[next_read]['BML']:
                unitig.append(next_read)
                start_read = next_read
            else:
                break
        return unitig


    # Find and build unitigs
    for start_read in list(matches.keys()):  # Create a copy of keys
        if start_read not in matches:
            continue
        unitig = find_unitig(start_read)
        unitigs.append(unitig)

    # Sort unitigs alphabetically by the leftmost read
    unitigs.sort(key=lambda x: x[0])

    # Write the unitigs to the output file
    with open(output_file, 'w') as out_file:
        for unitig in unitigs:
            out_file.write(unitig[0] + '\n')
            prev_read = unitig[0]
            for read in unitig[1:]:
                overlap = next(x[1] for x in matches[prev_read] if x[0] == read)
                out_file.write(f"{overlap} {read}\n")
                prev_read = read

if len(sys.argv) != 3:
    print("Usage: python3 hw4q3.py input_file output_file")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

find_unitigs(input_file, output_file)
