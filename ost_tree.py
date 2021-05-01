'''
Алгоритм Краскала для построения остовного дерева
На вход подавать кол-во вершин в графе (n) и список
возможных ребёр (List): (длина, вершина1, вершина2)
На выходе получится граф в виде списка смежностей: [[(длина, вершина)]]

Уточнение: это авторская модификация алгоритма Краскала, т.к. если
брать оригинальный алгоритм, то все пути будут минимальными,
а это скучно (поэтому используется не сортировка по длине, а
перемешивание в случайном порядке).

Естественно, дерево при таком раскладе получается не остовным.
'''

from random import shuffle

import dns_realization


LEN = 0
VEA = 1
VEB = 2

def build_ost_tree(nummer, list_):
    '''
        Функция строит минимальное остовное дерево (см. описание к модулю).
    '''
    graph = []
    for i in range(nummer):
        graph.append([])
    dns = dns_realization.DNS(nummer)
    shuffle(list_)
    new_list = []
    for i in list_:
        if dns.get_parent(i[VEA]) != dns.get_parent(i[VEB]):
            new_list.append(i)
            dns.unite(i[VEA], i[VEB])
    for i in new_list:
        graph[i[VEA]].append((i[LEN], i[VEB]))
        graph[i[VEB]].append((i[LEN], i[VEA]))
    return graph
