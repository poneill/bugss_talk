import random
from matplotlib import pyplot as plt
from collections import defaultdict

def load_fna():
    """Read the .fna file and return the genomic sequence as a
    string"""
    with open("NC_000913.fna") as f:
        lines = f.readlines()
    sequence_lines = lines[1:] #throw away the header line
    stripped_lines = [line.strip() for line in sequence_lines]
    return "".join(stripped_lines)

genome = load_fna()        
        
# What is the length of the genome?
# What is the frequency of each base?

def reverse_complement(sequence):
    complement = {"A":"T",
                  "T":"A",
                  "G":"C",
                  "C":"G"}
    return "".join(complement[base] for base in reversed(sequence))
    
# How many nmers do we have for length n?

def count_nmers(genome,n):
    """Count the occurrences of each nmer (on the forward strand)"""
    counts = defaultdict(int)#{nmer:0 for nmer in nmers(n)}
    G = len(genome)
    for i in xrange(G-n+1):
        counts[genome[i:i+n]] += 1
    return counts

def gc_content(sequence):
    return (sequence.count("G") + sequence.count("C"))/float(len(sequence))

def random_sequence(n):
    """Return a random nucleotide sequence (with uniform
    probabilities) of length n"""
    return "".join(random.choice("ACGT") for i in xrange(n))

# What is the distribution of monomers?  Dimers?  Trimers?  Decamers?
# What distribution is expected?

stop_codons = ["TGA","TAA","TAG"]
    
def all_orfs(sequence):
    """Given a sequence, return a list whose ith element contains the
    distance from the next in-frame stop codon for the ith position in
    the sequence"""
    n = len(sequence)
    distances = [-1] * n
    for i in xrange(n):
        for j in xrange(i,n,3):
            if sequence [j:j+3] in stop_codons:
                distances[i] = j
                break
    return distances

def plot_orfs(sequence):
    n = len(sequence)
    control_sequence = random_sequence(n)
    print "finding forward ORFs"
    orfs = all_orfs(sequence)
    print "finding forward control ORFs"
    control_orfs = all_orfs(control_sequence)
    print "finding reverse ORFs"
    reverse_orfs = all_orfs(reverse_complement(sequence))
    print "finding reverse control ORFs"
    control_reverse_orfs = all_orfs(reverse_complement(control_sequence))
    plt.plot(orfs,label="Forward ORFs")
    plt.plot(control_orfs,label="Reverse ORFs")
    plt.plot([n - x for x in reversed(reverse_orfs)],
             label="Forward control ORFs")
    plt.plot([n - x for x in reversed(control_reverse_orfs)],
             label="Reverse control ORFs")
    plt.xlabel("Position")
    plt.ylabel("Stop Codon Position")
    plt.legend()
    plt.show()

def dorf(n): #naming convention inherited from R
    """What is the probability of an open reading frame of n
    codons in a random sequence?"""
    stop_codon_probability = 3/float(64)
    return (1-stop_codon_probability )**(n-1)*stop_codon_probability

# what is the expected length of an ORF in a random sequence?
# expectation = sum([n * dorf(n) for n in range(1000)])
# expectation_another_way = 64/float(3)

# what is the distribution of ORFs in a random sequence?

def rorf(): #naming convention inherited from R
    """Sample the length of a random ORF"""
    i = 0
    stop_codon_probability = 3/float(64)
    while random.random() > stop_codon_probability:
        i += 1
    return i
            
def predict_genes(genome,min_gene_nt_length=300):
    gene_positions = []
    n = len(genome)
    for i in range(len(genome)):
        if genome[i:i+3] == "ATG": #if we're currently at a start codon
            start_codon_position = i
            # now look for the last start or stop codon...
            found_stop_codon_yet = False
            exceeded_bound = False
            j = i
            while not found_stop_codon_yet:
                j += 3
                current_codon = genome[j:j+3]
                if current_codon in stop_codons:
                    stop_codon_position = j + 3
                    found_stop_codon_yet = True
                if j > n:
                    exceeded_bound = True
                    break
            if exceeded_bound:
                print "exceeded bound"
                continue
            orf_length = stop_codon_position - start_codon_position
            if (orf_length > min_gene_nt_length #nucleotides
                and not any([other_start < start_codon_position < other_stop
                             for (other_start,other_stop) in gene_positions])):
                print start_codon_position,stop_codon_position
                gene_positions.append((start_codon_position,stop_codon_position))
    return gene_positions
            
def load_ffn():
    """Read the .ffn and return a list of coding sequences"""
    with open("NC_000913.ffn") as f:
        lines = f.readlines()
    # Parse chunks and throw away the first line
    coding_sequence_chunks = [chunk.split("\n")
                              for chunk in "".join(lines).split(">")][1:]
    coding_sequences = ["".join(chunk[1:]) # throw away header
                        for chunk in coding_sequence_chunks]
    return coding_sequences

def find_genes(genome,coding_sequences):
    """Given a genome and list of coding sequences, return a list
    whose ith element is the position (of the beginning) of the ith
    coding sequence on the forward strand (NB!) of the genome"""
    return [genome.find(cds) for cds in coding_sequences]

def get_gene_locations(genome,coding_sequences):
    """Return a list of tuples of form [(start_pos,stop_pos)] for the
    forward and backward strands"""
    forward_gene_locations = find_genes(genome,coding_sequences)
    backward_gene_locations = find_genes(reverse_complement(genome),
                                         coding_sequences)
    return forward_gene_locations,backward_gene_locations

def plot_gene_predictions(gene_predictions,gene_locations):
    """Visualize comparison between gene predictions and gene
    locations as a scatter plot"""
    predicted_starts = [start for (start,stop) in gene_predictions]
    predicted_stops = [stop for (start,stop) in gene_predictions]
    actual_starts = [start for (start,stop) in gene_locations]
    actual_stops = [stop for (start,stop) in gene_locations]
    plt.plot(predicted_starts,predicted_stops,linestyle="",marker=".")
    plt.plot(actual_starts,actual_stops,linestyle="",marker=".")
    
