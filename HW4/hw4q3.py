import sys

def find_unitigs(input_file, output_file):
    # Read the "best unambiguous match to the right" information from the input file
    bmr_matches = {}
    bml_matches = {}

    with open(input_file, 'r') as file:
        for line in file:
            parts = line.strip().split()
            read_id, overlap, match_id = parts[0], int(parts[1]), parts[2]

            # Update BMR (best match to the right)
            if read_id not in bmr_matches:
                bmr_matches[read_id] = []
            bmr_matches[read_id].append((match_id, overlap))

            # Update BML (best match to the left)
            if match_id not in bml_matches:
                bml_matches[match_id] = []
            bml_matches[match_id].append((read_id, overlap))

    unitigs = []

    def find_unitig(start_read):
        unitig = [start_read]
        while start_read in bmr_matches:
            if not bmr_matches[start_read]:
                break  # No BMR, exit the loop
            bmr_matches[start_read].sort(key=lambda x: -x[1])  # Sort by descending overlap
            next_read, overlap = bmr_matches[start_read][0]
            bmr_matches[start_read] = bmr_matches[start_read][1:]  # Remove the used match
            if next_read in bml_matches and (start_read, overlap) in bml_matches[next_read]:
                unitig.append(next_read)
                start_read = next_read
            else:
                break
        return unitig

    # Find and build unitigs
    for start_read in list(bmr_matches.keys()):  # Create a copy of keys
        if start_read not in bmr_matches:
            continue
        unitig = find_unitig(start_read)
        unitigs.append(unitig)

    # Sort unitigs in alphabetical order by the leftmost read
    unitigs.sort(key=lambda x: x[0])

    # Write the unitigs to the output file
    with open(output_file, 'w') as out_file:
        for unitig in unitigs:
            if len(unitig) > 1:
                out_file.write(unitig[0] + '\n')
                prev_read = unitig[0]
                for read in unitig[1:]:
                    overlap = next(x[1] for x in bml_matches[read] if x[0] == prev_read)
                    out_file.write(f"{overlap} {read}\n")
                    prev_read = read

if len(sys.argv) != 3:
    print("Usage: python3 hw4q3.py input_file output_file")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

find_unitigs(input_file, output_file)
