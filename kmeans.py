import random
import numpy as np

# returns false if word starts with @ or is a link
def valid_word(w):
    if w.startswith('@') or w.startswith('http'):
        return False
    return True

# preprocesses tweets to delete unecessary stuff
def process_tweet(tweet):
    tweet = tweet.split('|')[2].replace('#', '').lower()
    result = ' '.join([word for word in tweet.split(' ') if valid_word(word)])
    return result

# performs jaccard distance calculation given two sentences
def jaccard(t1, t2):
    union = len(set(t1.split() + t2.split()))
    inter = len([word for word in t1.split() if word in t2.split()])
    return 1 - inter / union

# returns a matrix storing jaccard distances so we don't have to do the jaccard calculation again and again
def get_jaccard_matrix(tweets):
    n = len(tweets)
    mat = np.zeros((n, n))
    for i in range(n):
        for j in range(i, n):
            mat[i][j] = jaccard(tweets[i], tweets[j])
            mat[j][i] = mat[i][j]
    return mat


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
                total_dist_to_cluster = sum([jaccard_matrix[i][j] for j in cluster])
                if i in cluster and len(cluster) > 1:
                    dist_to_clusters += [total_dist_to_cluster / (len(cluster) - 1)]
                else:
                    dist_to_clusters += [total_dist_to_cluster / (len(cluster))]
            # find the minimum distance to see which cluster the tweet actually belongs to
            clusters[dist_to_clusters.index(min(dist_to_clusters))] += [i]
            print(clusters)



file = open('Health-Tweets/samplefoxnewshealth.txt')
lines = file.readlines()

tweets = [process_tweet(line) for line in lines]
print(tweets)

# create the required variables:
max_iterations = 50
k = 3
initial_clusters = [[] for i in range(k)]

# initialize the clusters with random seeds:
seed_ids = random.sample(range(len(tweets)), k)
seeds = [tweets[i] for i in seed_ids]
for tweet in tweets:
    min_dist = 2
    min_dist_index = 0
    for j in range(len(seeds)):
        distance_to_seed_j = jaccard(tweet, seeds[j])
        if distance_to_seed_j < min_dist:
            min_dist = distance_to_seed_j
            min_dist_index = j
    initial_clusters[min_dist_index] += [tweets.index(tweet)]
file = open('jaccard_matrix.npy')
jaccard_matrix = np.load('jaccard_matrix.npy')
# initial_clusters = [[0, 1, 2, 4, 5, 6], [3]]
print(initial_clusters)
kmeans(initial_clusters, 50, jaccard_matrix)
