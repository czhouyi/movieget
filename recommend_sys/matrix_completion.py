#!/usr/bin/env python
import numpy as np
from scipy import linalg
import time

class SVDThreshold:
    def __init__(self):
        self.cut_num = 5
        self.delta = 1.2
        self.tolerance = 8

    def train(self, matrix):
        print "training the matrix..."
        start_time = time.time()
        norm = 100
        xk = matrix.complete_matrix
        projector = matrix.truth_tags
        true_M = xk*projector
        m,n = xk.shape
        counter = 0
        n_keep = self.cut_num
        while norm > self.tolerance:
            xk[projector] = true_M[projector]
            u,s,v = linalg.svd(xk)            
            sig = linalg.diagsvd(s, m, n)
            cutoff = sig[n_keep-1]
            sig_cut = sig*(sig > cutoff)
            xk = u.dot(sig_cut.dot(v))
            true_xk = xk*projector
            diff_matrix = true_M - true_xk          
            norm = linalg.norm(diff_matrix)            
            counter += 1
            if counter%50 == 0:
                n_keep += 1
            if counter%500 == 0:
                print 'be patient, working on it...'
                print 'time spend: %s'%(time.time()-start_time)
                #break
                #print "loop: ",counter
        print "total cost: %s seconds"%(time.time()-start_time)
        print "total loops: ",str(counter)
        return xk
            
