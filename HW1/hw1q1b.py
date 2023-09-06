import sys
inputFile = sys.argv[1]
outputFile = "hw1q1b.out"

with open(inputFile) as myFile:
  lines = myFile.readlines()

output = []
for ln in lines:
  for c in ln:
    if c in 'ACGT':
      output.append(c)

with open(outputFile, 'w') as out_fh:
  out_fh.write(''.join(output))