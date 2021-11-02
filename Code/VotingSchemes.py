import numpy as np

# Can be used for plurality, vote for n, anti-plurality
def create_vote_for_n_vector(n, num_candidates):
    vec = np.zeros(num_candidates)
    vec[0:n] = 1
    return vec

# Can be used for borda count
def create_borda_count(num_candidates):
    vec = np.zeros(num_candidates)
    for x in range(num_candidates):
        vec[x] = (num_candidates-1-x)
    return vec
