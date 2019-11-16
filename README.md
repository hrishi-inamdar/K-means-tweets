# K-means-tweets

## Running Instructions:
jaccard_matrix.npy is already preloaded with the jaccard distance data from foxnewshealth.txt input file.
If you wish to load another file, please edit line 31 of preprocess.py with the new file location and run it. This will generate a new jaccard_matrix.npy.

Once this is complete, edit the k value and max iterations on lines 52 and 53 of kmeans.py and run kmeans on the jaccard_matrix from earlier. This will produce an output like this:
```
...
1 iterations remaining
0 iterations remaining
k =	 8
SSE:	 1821.6262244819793

CLUSTERS:
0 : 205
1 : 542
2 : 102
3 : 265
4 : 261
5 : 215
6 : 118
7 : 292
```

The results in results.txt had max_iteration of 50 for all. 
