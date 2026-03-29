import numpy as np

def bfs(theta): 
    '''
    theta : the design structure matrix
    labels =[1 1 1 2 2 3 3 ...]  lenght(labels)=L, label for each vertex
    labels(i) is order number of connected component, i is vertex number
    rts : roots, numbers of started vertex in each component
    '''
    
    L = theta.shape[0]  # number of vertices

    # Breadth-first search:
    labels = np.zeros(L, dtype=int)  # all vertices unexplored at the beginning
    rts = []
    ccc = 0  # connected components counter

    while True:
        ind = np.where(labels == 0)[0]
        if ind.size > 0:
            fue = ind[0]  # first unexplored vertex
            rts.append(fue)
            list_ = [fue]
            ccc += 1
            labels[fue] = ccc
            while True:
                list_new = []
                for p in list_:
                    cp = np.where(theta[p, :])[0]  # points connected to p
                    cp1 = cp[labels[cp] == 0]  # get only unexplored vertices
                    labels[cp1] = ccc
                    list_new.extend(cp1)
                list_ = list_new
                if len(list_) == 0:
                    break
        else:
            break

    group_num = np.max(labels)
    allgroups = [[] for _ in range(group_num)]
    for i in range(1, group_num + 1):
        allgroups[i - 1] = np.where(labels == i)[0].tolist()
    
    components = allgroups

    h = lambda x : len(x) == 1
    sizeone = list(map(h, components))
    seps = np.concatenate([components[i] for i, flag in enumerate(sizeone) if flag])
    nonseps = [components[i] for i, flag in enumerate(sizeone) if not flag]
    
    subspaces = {'seps': seps, 'nonseps': nonseps} # seps：list of indices; nonseps: list of lists of indices
    return subspaces