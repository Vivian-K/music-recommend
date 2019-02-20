# -*- coding: utf-8 -*-


import math
import operator

def UserSimilarity(train):
    # build inverse table for item_users
    item_users = dict()
    for u,items in train.items():
        for i in items.keys():
            if i not in item_users:
                item_users[i] = set()
            item_users[i].add(u) 
     #'''item_user格式：{艺术家：{user, user, user}, {}, {}}'''
        
    #calculate co-rated items between users
    C = dict()
    N = dict()#
    for i,users in item_users.items():
        for u in users:
            N.setdefault(u,0)
            N[u] += 1
            C.setdefault(u,{})
            for v in users:
                if u == v:
                    continue
                C[u].setdefault(v,0)
                C[u][v] += 1 / math.log(1+len(users))
                #实际上，用户间对冷门物品采取过同样的行为更能说明他们兴趣的相似度，
                #因此，我们可以通过惩罚用户间共同兴趣列表中热门物品的影响（通过下式可见是用分子惩罚的）
                #对上述用户相似度计算式进行改进

    #calculate finial similarity matrix W
    W = C.copy()
    for u, related_users in C.items():
        for v, cuv in related_users.items():
            W[u][v] = cuv / math.sqrt(N[u] * N[v])
    return W
    
def Recommend(user,train,W,K = 3):
    rank = dict()
    if user not in train.keys():
        return rank
    interacted_items = train[user]              ##operator模块提供的itemgetter函数用于获取对象的哪些维的数据
    for v, wuv in sorted(W[user].items(), key = operator.itemgetter(1), \
                         reverse = True)[0:K]:
        for i, rvi in train[v].items():
            #we should filter items user interacted before 
            if i in interacted_items:
                continue
            rank.setdefault(i,0)
            rank[i] += wuv * rvi
    return rank
    
def Recommendation(users, train, W, K = 10):
    result = dict()
    for user in users:
        rank = Recommend(user,train,W,K)
        R = sorted(rank.items(), key = operator.itemgetter(1), \
                   reverse = True)
        result[user] = R
    return result