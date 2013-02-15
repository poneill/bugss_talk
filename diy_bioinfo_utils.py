# Just some utility functions

def auto_cor(xs):
    """Return autocorrelation of xs"""
    n = len(xs)
    mu = mean(xs)
    sigma_sq = variance(xs)
    return [mean([(xs[i]-mu)*(xs[i+k]-mu) for i in xrange(n-k)])/sigma_sq
            for k in verbose_gen(range(n))]

def verbose_gen(xs,modulus=1):
    """A poor man's progress bar'"""
    for i,x in enumerate(xs):
        if not i % modulus:
            print i
        yield x

def mean(xs):
    """Compute mean"""
    return sum(xs)/float(len(xs))

def variance(xs,correct=True):
    """Compute variance, with or without sample correction"""
    n = len(xs)
    correction = n/float(n-1) if correct else 1
    return correction * mean([x**2 for x in xs]) - mean(xs) ** 2

def group_by(xs,n):
    """Split xs into lists of length n"""
    return [xs[i:i+n] for i in range(0,len(xs),n)]

def codonize(seq):
    """Split a sequence into codons"""
    return group_by(seq,3)

def safe_index(xs,x):
    """Implement index function of lists, but return -1 if x not
    found"""
    if x in xs:
        return xs.index(x)
    else:
        return -1

def nmers(n):
    """Return an exhaustive list of oligomers of length n"""
    bases = ["A","C","G","T"]
    if n == 1:
        return bases
    else:
        return sum([map(lambda(b):b+c,nmers(n-1))
                    for c in bases],[])

def translate(codon):
    """Translate a codon or sequence"""
    if len(codon) == 3:
        for aa in translation_table:
            if codon in translation_table[aa]:
                return aa
    else:
        return "".join(map(translate,codonize(codon)))

translation_table = {"A":["GCA","GCC","GCG","GCT"],
                     "R": ["AGA","AGG","CGA","CGC","CGG","CGT"],
                     "N": ["AAT", "AAC"],
                     "D": ["GAT", "GAC"],
                     "C": ["TGT", "TGC"],
                     "E": ["GAA", "GAG"],
                     "Q": ["CAA", "CAG"],
                     "G": ["GGA","GGC","GGG","GGT"],
                     "H": ["CAT", "CAC"],
                     "I": ["ATT", "ATC", "ATA"],
                     "L": ["TTA", "TTG", "CTA","CTC","CTG","CTT"],
                     "K": ["AAA", "AAG"],
                     "M": ["ATG"],
                     "F": ["TTT", "TTC"],
                     "P": ["CCA","CCC","CCG","CCT"],
                     "S": ["AGT", "AGC", "TCA","TCC","TCG","TCT"],
                     "T": ["ACA","ACC","ACG","ACT"],
                     "W": ["TGG"],
                     "Y": ["TAT", "TAC"],
                     "V": ["GTA","GTC","GTG","GTT"],
                     "X": ["TAA", "TAG","TGA"]}
