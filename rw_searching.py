import json
import time
import src_IR_prediction.Config as cf

graph_data = json.load("data/graph_stored.json")

def PersonalRank(G, alpha, root, max_depth):
    rank = dict()
    rank = {x: 0 for x in G.keys()}
    rank[root] = 1
    begin = time.time()
    for k in range(max_depth):
        tmp = {x: 0 for x in G.keys()}
        for i, ri in G.items():
            for j, wij in ri.items():
                tmp[j] += alpha * rank[i] / (1.0 * len(ri))
        tmp[root] += (1 - alpha)
        rank = tmp
    end = time.time()
    print('use_time', end - begin)
    lst = sorted(rank.items(), key=lambda x: x[1], reverse=True)
    for ele in lst:
        print("%s:%.3f, \t" % (ele[0], ele[1]))
    return rank

PersonalRank(graph_data, cf.alpha, cf.root, cf.max_depth)