# If more than 1 read has the highest or lowest quality, give the one that occurs first in the file.

# (a) The read that has the lowest total quality score (1=first read, 2=second read, etc)
# (b) The read that has the highest total quality score
# (c) The total number of base quality values (denoted Q in lecture) less than 10.
# (d) The total number of base quality values ≥ 30
# (e) Total number of characters observed in the read sequences of the file other than A, C, G, or T


# got parse_fastq function code from https://nbviewer.org/github/BenLangmead/comp-genomics-class/blob/master/notebooks/FASTQ.ipynb, linked in HW
def parse_fastq(fh):
    """ Parse reads from a FASTQ filehandle.  For each read, we
        return a name, nucleotide-string, quality-string triple. """
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

fastq_string = '''@ERR294379.100739024 HS24_09441:8:2203:17450:94030#42/1
AGGGAGTCCACAGCACAGTCCAGACTCCCACCAGTTCTGACGAAATGATG
+
BDDEEF?FGFFFHGFFHHGHGGHCH@GHHHGFAHEGFEHGEFGHCCGGGF
@ERR294379.136275489 HS24_09441:8:2311:1917:99340#42/1
CTTAAGTATTTTGAAAGTTAACATAAGTTATTCTCAGAGAGACTGCTTTT
+
@@AHFF?EEDEAF?FEEGEFD?GGFEFGECGE?9H?EEABFAG9@CDGGF
@ERR294379.97291341 HS24_09441:8:2201:10397:52549#42/1
GGCTGCCATCAGTGAGCAAGTAAGAATTTGCAGAAATTTATTAGCACACT
+
CDAF<FFDEHEFDDFEEFDGDFCHD=GHG<GEDHDGJFHEFFGEFEE@GH'''

from io import StringIO

parse_fastq(StringIO(fastq_string))