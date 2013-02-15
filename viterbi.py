from math import log

# framework basically ripped off from wikipedia:
# http://en.wikipedia.org/wiki/Viterbi_algorithm
# and adapted for our purposes

states = ('non_coding',
          'start_codon1','start_codon2','start_codon3',
          'coding1','coding2','coding3',
          'stop_codon1',
          'stop_codon2_TAG','stop_codon2_TGA','stop_codon2_TAA',
          'stop_codon3_TAG','stop_codon3_TGA','stop_codon3_TAA')
 
observations = ('A','C','G','T')
 
start_probability = {'non_coding':1, # assume we definitely start in non_coding
                     'start_codon1':0,'start_codon2':0,'start_codon3':0,
                     'coding1':0,'coding2':0,'coding3':0,
                     'stop_codon1':0,
                     'stop_codon2_TAG':0,'stop_codon2_TGA':0,'stop_codon2_TAA':0,
                     'stop_codon3_TAG':0,'stop_codon3_TGA':0,'stop_codon3_TAA':0}

 
transition_probability = {
    'non_coding' : {'non_coding':.99, # assume we definitely start in non_coding
                     'start_codon1':0.01,'start_codon2':0,'start_codon3':0,
                     'coding1':0,'coding2':0,'coding3':0,
                     'stop_codon1':0,
                     'stop_codon2_TAG':0,'stop_codon2_TGA':0,'stop_codon2_TAA':0,
                     'stop_codon3_TAG':0,'stop_codon3_TGA':0,'stop_codon3_TAA':0},
    'start_codon1' : {'non_coding':0, #transition to start_codon2
                     'start_codon1':0,'start_codon2':1,'start_codon3':0,
                     'coding1':0,'coding2':0,'coding3':0, 
                     'stop_codon1':0,
                      'stop_codon2_TAG':0,'stop_codon2_TGA':0,'stop_codon2_TAA':0,
                     'stop_codon3_TAG':0,'stop_codon3_TGA':0,'stop_codon3_TAA':0},
    'start_codon2' : {'non_coding':0, # transition to start_codon3
                     'start_codon1':0,'start_codon2':0,'start_codon3':1,
                     'coding1':0,'coding2':0,'coding3':0,
                     'stop_codon1':0,
                      'stop_codon2_TAG':0,'stop_codon2_TGA':0,'stop_codon2_TAA':0,
                     'stop_codon3_TAG':0,'stop_codon3_TGA':0,'stop_codon3_TAA':0},
    'start_codon3' : {'non_coding':0, # transition to coding 1
                     'start_codon1':0,'start_codon2':0,'start_codon3':0,
                     'coding1':1,'coding2':0,'coding3':0,
                     'stop_codon1':0,
                      'stop_codon2_TAG':0,'stop_codon2_TGA':0,'stop_codon2_TAA':0,
                     'stop_codon3_TAG':0,'stop_codon3_TGA':0,'stop_codon3_TAA':0},
    'coding1' : {'non_coding':0, # transition to coding 2
                  'start_codon1':0,'start_codon2':0,'start_codon3':0,
                  'coding1':0,'coding2':1,'coding3':0,
                  'stop_codon1':0,
                 'stop_codon2_TAG':0,'stop_codon2_TGA':0,'stop_codon2_TAA':0,
                 'stop_codon3_TAG':0,'stop_codon3_TGA':0,'stop_codon3_TAA':0},
    'coding2' : {'non_coding':0, # transition to coding 3
                 'start_codon1':0,'start_codon2':0,'start_codon3':0,
                 'coding1':0,'coding2':0,'coding3':1,
                 'stop_codon1':0,
                 'stop_codon2_TAG':0,'stop_codon2_TGA':0,'stop_codon2_TAA':0,
                 'stop_codon3_TAG':0,'stop_codon3_TGA':0,'stop_codon3_TAA':0},
    'coding3' : {'non_coding':0, # transition to coding1 or stop_codon1
                 'start_codon1':0,'start_codon2':0,'start_codon3':0,
                 'coding1':0.997,'coding2':0,'coding3': 0,
                 'stop_codon1':.003,
                 'stop_codon2_TAG':0,'stop_codon2_TGA':0,'stop_codon2_TAA':0,
                 'stop_codon3_TAG':0,'stop_codon3_TGA':0,'stop_codon3_TAA':0},
    'stop_codon1' : {'non_coding':0, # transition to (some) stop_codon2
                     'start_codon1':0,'start_codon2':0,'start_codon3':0,
                     'coding1':0,'coding2':0,'coding3':0,
                     'stop_codon1':0,
                     'stop_codon2_TAG':.34,'stop_codon2_TGA':.33,'stop_codon2_TAA':.33,
                     'stop_codon3_TAG':0,'stop_codon3_TGA':0,'stop_codon3_TAA':0},
    'stop_codon2_TAG' : {'non_coding':0, # transition to stop_codon3_TAG
                         'start_codon1':0,'start_codon2':0,'start_codon3':0,
                         'coding1':0,'coding2':0,'coding3':0,
                         'stop_codon1':0,
                         'stop_codon2_TAG':0,'stop_codon2_TGA':0,'stop_codon2_TAA':0,
                         'stop_codon3_TAG':1,'stop_codon3_TGA':0,'stop_codon3_TAA':0},
    'stop_codon2_TGA' : {'non_coding':0, # transition to stop_codon3_TGA
                         'start_codon1':0,'start_codon2':0,'start_codon3':0,
                         'coding1':0,'coding2':0,'coding3':0,
                         'stop_codon1':0,
                         'stop_codon2_TAG':0,'stop_codon2_TGA':0,'stop_codon2_TAA':0,
                         'stop_codon3_TAG':0,'stop_codon3_TGA':1,'stop_codon3_TAA':0},
    'stop_codon2_TAA' : {'non_coding':0, # transition to stop_codon3_TAA
                         'start_codon1':0,'start_codon2':0,'start_codon3':0,
                         'coding1':0,'coding2':0,'coding3':0,
                         'stop_codon1':0,
                         'stop_codon2_TAG':0,'stop_codon2_TGA':0,'stop_codon2_TAA':0,
                         'stop_codon3_TAG':0,'stop_codon3_TGA':0,'stop_codon3_TAA':1},
    'stop_codon3_TAG' : {'non_coding':1, # transition to non_coding
                         'start_codon1':0,'start_codon2':0,'start_codon3':0,
                         'coding1':0,'coding2':0,'coding3':0,
                         'stop_codon1':0,
                         'stop_codon2_TAG':0,'stop_codon2_TGA':0,'stop_codon2_TAA':0,
                         'stop_codon3_TAG':0,'stop_codon3_TGA':0,'stop_codon3_TAA':0},
    'stop_codon3_TGA' : {'non_coding':1, # transition to non_coding
                         'start_codon1':0,'start_codon2':0,'start_codon3':0,
                         'coding1':0,'coding2':0,'coding3':0,
                         'stop_codon1':0,
                         'stop_codon2_TAG':0,'stop_codon2_TGA':0,'stop_codon2_TAA':0,
                         'stop_codon3_TAG':0,'stop_codon3_TGA':0,'stop_codon3_TAA':0},
    'stop_codon3_TAA' : {'non_coding':1, # transition to non_coding
                         'start_codon1':0,'start_codon2':0,'start_codon3':0,
                         'coding1':0,'coding2':0,'coding3':0,
                         'stop_codon1':0,
                         'stop_codon2_TAG':0,'stop_codon2_TGA':0,'stop_codon2_TAA':0,
                         'stop_codon3_TAG':0,'stop_codon3_TGA':0,'stop_codon3_TAA':0}
   }

stop_codons = ["TGA","TAG","TAA"]
coding_codons = [nmer for nmer in nmers(3) if not nmer in stop_codons]
first_codon_counts,second_codon_counts,third_codon_counts = zip(*coding_codons)
emission_probability = {
   'non_coding' : {'A': 0.25, 'C': 0.25, 'G': 0.25, 'T':0.25},
   'start_codon1' : {'A': 1, 'C': 0.0, 'G': 0.0, 'T':0.0},
   'start_codon2' : {'A': 0.0, 'C': 0.0, 'G': 0.0, 'T':1.0},
   'start_codon3' : {'A': 0.0, 'C': 0.0, 'G': 1.0, 'T':0.0},
   'coding1' : {'A': first_codon_counts.count("A")/61.0,
                'C': first_codon_counts.count("C")/61.0,
                'G': first_codon_counts.count("G")/61.0,
                'T': first_codon_counts.count("T")/61.0},
   'coding2' : {'A': second_codon_counts.count("A")/61.0,
                'C': second_codon_counts.count("C")/61.0,
                'G': second_codon_counts.count("G")/61.0,
                'T': second_codon_counts.count("T")/61.0},
   'coding3' : {'A': third_codon_counts.count("A")/61.0,
                'C': third_codon_counts.count("C")/61.0,
                'G': third_codon_counts.count("G")/61.0,
                'T': third_codon_counts.count("T")/61.0},
   'stop_codon1' : {'A': 0, 'C': 0.0, 'G': 0.0, 'T':1.0},
   'stop_codon2_TAG' : {'A': 1, 'C': 0.0, 'G': 0.0, 'T':0.0},
   'stop_codon2_TGA' : {'A': 0.0, 'C': 0.0, 'G': 1, 'T':0.0},
   'stop_codon2_TAA' : {'A': 1, 'C': 0.0, 'G': 0.0, 'T':0.0},
   'stop_codon3_TAG' : {'A': 0, 'C': 0.0, 'G': 1.0, 'T':0.0},
   'stop_codon3_TGA' : {'A': 1.0, 'C': 0.0, 'G': 0, 'T':0.0},
   'stop_codon3_TAA' : {'A': 1, 'C': 0.0, 'G': 0.0, 'T':0.0},
   }

def print_dptable(V):
    print "    ",
    for i in range(len(V)): print "%7d" % i,
    print
 
    for y in V[0].keys():
        print "%.5s: " % y,
        for t in range(len(V)):
            print "%.7s" % ("%f" % V[t][y]),
        print
 
def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}]
    path = {}
    def safe_log(x):
        return log(x + 10**-100)
    # Initialize base cases (t == 0)
    for y in states:
        V[0][y] = safe_log(start_p[y]) + safe_log(emit_p[y][obs[0]])
        path[y] = [y]
 
    # Run Viterbi for t > 0
    for t in range(1,len(obs)):
        V.append({})
        newpath = {}
 
        for y in states:
            #(prob, state) = max([(V[t-1][y0] * trans_p[y0][y] * emit_p[y][obs[t]], y0) for y0 in states])
            (prob, state) = max([(V[t-1][y0] + safe_log(trans_p[y0][y]) + safe_log(emit_p[y][obs[t]]), y0) for y0 in states])
            V[t][y] = prob
            newpath[y] = path[state] + [y]
 
        # Don't need to remember the old paths
        path = newpath
 
    #print_dptable(V)
    (prob, state) = max([(V[len(obs) - 1][y], y) for y in states])
    return (prob, path[state])

def path_to_gene_predictions(path):
    """Accept a path as predicted by Viterbi and return a list of gene predictions
    in the form [(start_pos,stop_pos)]"""
    gene_locations = []
    n = len(path)
    for i in xrange(n):
        current_state = path[i]
        if current_state == "start_codon1":
            start_pos = i
        elif "stop_codon3" in current_state:
            stop_pos = i
            gene_locations.append((start_pos,stop_pos))
    return gene_locations
