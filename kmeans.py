import random
import numpy as np

debug = False
def kmeans(initial_clusters, max_iterations, jaccard_matrix):
    iterations = 0
    k = len(initial_clusters)
    n = len(jaccard_matrix)
    clusters = initial_clusters
    old_clusters = []
    # keep going until it reaches max_iterations or converges
    while iterations < max_iterations and old_clusters != clusters:
        iterations += 1
        # the clusters from last iteration are now old
        old_clusters = clusters
        # reset the clusters to fill again
        clusters = [[] for i in range(k)]
        for i in range(n):
            dist_to_clusters = []
            # calculate average distance to each cluster for tweet i
            for cluster in old_clusters:
                if len(cluster) == 0:
                    continue
                total_dist_to_cluster = sum([jaccard_matrix[i][j] for j in cluster])
                if i in cluster and len(cluster) > 1:
                    dist_to_clusters += [total_dist_to_cluster / (len(cluster) - 1)]
                else:
                    dist_to_clusters += [total_dist_to_cluster / (len(cluster))]
            # find the minimum distance to see which cluster the tweet actually belongs to
            clusters[dist_to_clusters.index(min(dist_to_clusters))] += [i]
        if debug:
            print('after iteration', iterations, ':\t', clusters)
        else:
            print(max_iterations - iterations, 'iterations remaining')
    return clusters

def sse(clusters, jaccard_matrix):
    sse = 0
    for cluster in clusters:
        for i in cluster:
            total_dist_to_cluster = sum([(jaccard_matrix[i][j]) for j in cluster])
            if i in cluster and len(cluster) > 1:
                sse += (total_dist_to_cluster / (len(cluster) - 1))**2
            else:
                sse += (total_dist_to_cluster / (len(cluster)))**2
        if debug:
            print(sse)
    return sse


# create the required variables:
max_iterations = 50
k = 42
initial_clusters = [[] for i in range(k)]

jaccard_matrix = np.load('jaccard_matrix.npy')
n = len(jaccard_matrix)

# initialize the clusters with random seeds:
seed_ids = random.sample(range(n), k)
for i in range(n):
    min_dist = 2
    min_dist_index = 0
    for j in range(k):
        distance_to_seed_j = jaccard_matrix[i][j]
        if distance_to_seed_j < min_dist:
            min_dist = distance_to_seed_j
            min_dist_index = j
    initial_clusters[min_dist_index] += [i]
if debug:
    print('initial clusters:\t', initial_clusters)
    print()


clusters = kmeans(initial_clusters, max_iterations, jaccard_matrix)
print('k =\t', k)
print('SSE:\t', sse(clusters, jaccard_matrix))
print('\nCLUSTERS:')
for i in range(len(clusters)):
    print(i, ':', len(clusters[i]))
