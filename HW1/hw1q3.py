def transcription(dna):
    count = 1
    transcribed_dna = ""
    for base in dna:
      if count % 3 == 0 and count != len(dna):
         base+='-'
      if base == 'T':
        base = 'U'
      transcribed_dna+= base
      count += 1
    return ''.join(transcribed_dna)

if __name__ == "__main__":
    dna_input = input().strip()
    dna_cleaned = ''.join(base for base in dna_input if base in 'ACTG')
    transcribed = transcription(dna_cleaned)
    print(transcribed)