#Алгоритм Краскала для построения остовного дерева
#На вход подавать кол-во вершин в графе (n) и список возможных ребёр (List): (длина, вершина1, вершина2)
#На выходе получится граф в виде списка смежностей: [[(длина, вершина)]]

#Уточнение: это авторская модификация алгоритма Краскала, т.к. если брать оригинальный алгоритм, то все пути будут минимальными,
#а это скучно (поэтому используется не сортировка по длине, а перемешивание в случайном порядке).

#Естественно, дерево при таком раскладе получается не остовным.

import DNS
from random import shuffle

LEN = 0; VEA = 1; VEB = 2

def buildOstTree(n, List):
    graph = []
    for i in range(n):
        graph.append([])
    dns = DNS.DNS(n)
    shuffle(List)
    newList = []
    for i in List:
        if dns.get_parent(i[VEA]) != dns.get_parent(i[VEB]):
            newList.append(i)
            dns.unite(i[VEA], i[VEB])
    for i in newList:
        graph[i[VEA]].append((i[LEN], i[VEB]))
        graph[i[VEB]].append((i[LEN], i[VEA]))
    return graph

