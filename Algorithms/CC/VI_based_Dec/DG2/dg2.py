import numpy as np
from tqdm import tqdm

class Delta():
    delta1 = 0
    delta2 = 0

class Evaluations():
    base = 0
    F = 0
    fhat = 0

class DG2():
    def __init__(self, fun, info):
        self.fun = fun
        self.info = info

    def DG2(self):
        delta, evaluations, lambda_ = self.ism()
        seps, nonseps, theta, epsilon = self.dsm(evaluations, lambda_)
        return seps, nonseps

    # ISM: Interaction Structure Matrix
    def ism (self):
        delta = Delta()
        evaluations = Evaluations()
        center = 0.5*(self.info['lower']+self.info['upper'])*np.ones(self.info['dimension']) # m
        f_archive = np.full((self.info['dimension'], self.info['dimension']), np.nan) # record the [a_hat,b_hat,c,...] in the paper
        fhat_archive = np.full((self.info['dimension'], 1), np.nan) # record the [a,b_hat,c,...] in the paper
        delta1 = np.full((self.info['dimension'], self.info['dimension']), np.nan)
        delta2 = np.full((self.info['dimension'], self.info['dimension']), np.nan)
        lambda_ = np.full((self.info['dimension'], self.info['dimension']), np.nan) # raw interaction structure matrix

        p1 = np.ones(self.info['dimension'])*self.info['lower']
        fp1 = self.fun(p1) # f_base
        counter = 0 # Gamma

        for i in tqdm(range(self.info['dimension']-1)):
            if not np.isnan(fhat_archive[i]):
                fp2 = fhat_archive[i]
            else:
                p2 = np.copy(p1)
                p2[i] = center[i]
                fp2 = self.fun(p2)
                fhat_archive[i] = fp2
                counter += 1

            for j in range(i+1,self.info['dimension']):
                if not np.any(np.isnan(f_archive[j])):
                    fp3 = fhat_archive[j]
                else:
                    p3 = np.copy(p1)
                    p3[j] = center[j]
                    fp3 = self.fun(p3)
                    counter += 1
                    fhat_archive[j] = fp3

                p4 = np.copy(p1)
                p4[i] = center[i]
                p4[j] = center[j]
                fp4 = self.fun(p4)
                counter += 1
                f_archive[i,j] = fp4
                f_archive[j,i] = fp4
                d1 = fp2 - fp1
                d2 = fp4 - fp3
                delta1[i,j] = d1
                delta2[i,j] = d1
                lambda_[i,j] = abs(d1-d2)
        
        delta.delta1 = delta1
        delta.delta2 = delta2
        evaluations.base = fp1
        evaluations.F = f_archive
        evaluations.fhat = fhat_archive

        return delta, evaluations, lambda_

    # DSM: Decomposition Structure Matrix
    def dsm(self, evaluation, lambda_ ):
        fhat_archive = evaluation.fhat
        f_archive = evaluation.F
        fp1 = evaluation.base

        F1 = np.ones((self.info['dimension'], self.info['dimension']))*fp1
        F2 = np.tile(fhat_archive.T, (self.info['dimension'], 1))
        F3 = np.tile(fhat_archive, (1, self.info['dimension']))
        F4 = f_archive
        FS = np.stack((F1, F2, F3, F4), axis=2)
        Fmax = np.amax(FS, axis=2)
        FS = np.stack((F1+F4, F2+F3), axis=2)
        Fmax_inf = np.amax(FS, axis=2)

        theta = np.full((self.info['dimension'],self.info['dimension']), np.nan) # design structure matrix
        muM = np.finfo(float).eps / 2
        gamma = lambda n: (n * muM) / (1 - n * muM) 
        errlb = gamma(2)*Fmax_inf
        errub = gamma((self.info['dimension'])**0.5)*Fmax
        
        I1 = lambda_ <= errlb
        theta[I1] = 0
        I2 = lambda_ >= errub
        theta[I2] = 1
        I0 = (lambda_ == 0)
        c0 = np.sum(I0)
        count_seps = np.sum(~I0 & I1) # o<lambda_<=errlb
        count_nonseps = np.sum(I2)
        reliable_calcs = count_seps + count_nonseps
        w1 = ((count_seps+c0)/(c0 + reliable_calcs)) 
        w2 = ((count_nonseps)/(c0 + reliable_calcs))
        epsilon = w1*errlb + w2*errub

        AdjTemp = lambda_ > epsilon # adjustment threshold
        idx = np.isnan(theta)
        theta[idx] = AdjTemp[idx] # Complete the values ​​in the range[errlb, errub]
        theta[np.diag_indices(self.info['dimension'])] = True

        return theta.astype(int)