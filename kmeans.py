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
    mat = np.zeros((len(tweets), len(tweets)))
    for i in range(len(tweets)):
        for j in range(len(tweets)):
            mat[i][j] = jaccard(tweets[i], tweets[j])
    return mat

file = open('Health-Tweets/samplefoxnewshealth.txt')
lines = file.readlines()

tweets = [process_tweet(line) for line in lines]
print(tweets)

iterations = 0
max_iterations = 50
k = 2
clusters = [[] for i in range(k)]

seeds = random.sample(tweets, k)
# TODO: get the ids of the seeds somehow to use later for initialization
for i in range(len(tweets)):
    min_dist = 99999
    for j in range(len(seeds)):
        if jaccard(tweets[i], seeds[j]) < min_dist:
            pass


jaccard_matrix = get_jaccard_matrix(tweets)

while iterations < max_iterations:
    iterations += 1
