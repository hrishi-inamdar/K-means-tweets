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

file = open('Health-Tweets/samplefoxnewshealth.txt')
lines = file.readlines()
tweets = [process_tweet(line) for line in lines]

jaccard_matrix = get_jaccard_matrix(tweets)
np.save('jaccard_matrix.npy', jaccard_matrix)