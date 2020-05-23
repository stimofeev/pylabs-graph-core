import matplotlib.pyplot as plt
import networkx as nx
from numpy import genfromtxt
import numpy as np

# множество узлов
G = set()

# множество дуг
E = set()

# супермножество - множество всех комбинаций всех элементов
S = set()


def get_superset(graph_set: set):
    nodes_count = len(graph_set)
    super_set = set()
    # переберем все комбинации всех элементов
    for i1 in range(nodes_count+1):
        for i2 in range(nodes_count+1):
            for i3 in range(nodes_count+1):
                for i4 in range(nodes_count+1):
                    for i5 in range(nodes_count+1):
                        new_set = set()
                        if (i1 != 0):
                            new_set.add(i1-1)
                        if (i2 != 0):
                            new_set.add(i2-1)
                        if (i3 != 0):
                            new_set.add(i3-1)
                        if (i4 != 0):
                            new_set.add(i4-1)
                        if (i5 != 0):
                            new_set.add(i5-1)
                        if (len(new_set) > 0):
                            # запакуем множество в строку
                            new_elem = str(new_set)
                            # добавим новое множество в супермножество
                            super_set.add( new_elem )
    return super_set



def get_neibs_for_set(nodes_set: set):
    neibs_set = set()
    for node in nodes_set:
        # соседи для узла
        node_neibs = get_neibs_for_node(node)
        # добавим в общий список соседей для множества
        neibs_set.update(node_neibs)
    return neibs_set


# def get_neibs_exclude_for_set(nodes_set: set):
#     neibs_set = get_neibs_for_set(nodes_set)
#     for node in nodes_set:
#         neibs_set.discard(node)
#     return neibs_set


def unpack_set_from_str(set_str: str):
    # распакуем строку во множество
    s = set()
    for curr_char in set_str:
        if not (curr_char in (',','{','}',' ')):
            s.add( int(curr_char) )
    return s


def is_inner_stable(nodes_set: set):
    # общее множество соседей для проверяемого множества узлов
    neibs = get_neibs_for_set(nodes_set)
    # пересечение проверяемого множества узлов и общего множества соседей  
    intersection = nodes_set.intersection(neibs)
    # если множество перемечений - пустое (в общем множестве соседей нет узлов из проверяемого множества)
    #  то множество - внутренне устойчиво
    return ( len(intersection) == 0 )


def get_neibs_for_node(node):    
    node_neibs = set()
    for edge in E:
        if (edge[0] == node):
            # первый элемент дуги - искомый узел
            # добавим во множество соседей - второй узел из дуги
            node_neibs.add(edge[1])
        elif (edge[1] == node):
            # второй элемент дуги - искомый узел
            # добавим во множество соседей - первый узел из дуги
            node_neibs.add(edge[0])
    return node_neibs


def is_outer_stable(nodes_set: set):
    if len(nodes_set) == 0:
        return False
    # для каждого элемента множества должна быть связь с внешним миром
    # то есть пересечение с множеством соседей - непустое
    for node in nodes_set:
        node_neibs = get_neibs_for_node(node)
        # есть ли внешние соседи для узла
        diff_set = node_neibs.difference(nodes_set)
        if len(diff_set) == 0:
            # нет внешних соседей
            return False
    return True


def main():

    # считываем файл с мартрицей смежности
    a_matrix = genfromtxt('a_matrix.csv', delimiter=';')
    # формируем матрицу смежности
    adjacency = a_matrix[1:, 1:]
    # печатаем матрицу смежности  
    print('\nМатрица смежности\n',adjacency)
    
    # заполняем граф по матрице смежности
    a_rows, a_cols = np.where(adjacency == 1)
    a_edges = zip(a_rows.tolist(), a_cols.tolist())
    graph = nx.Graph()
    graph.add_edges_from(a_edges)

    # множество узлов
    for node in graph.nodes:
        G.add(node)
    print('\nУзлы графа:',G)

    # множество дуг
    for edge in graph.edges:
        E.add(edge)
    print('\nДуги графа:',E)

    # супермножество - множество всех комбинаций узлов
    S = get_superset(G)

    print('\nЯдра')
    for curr_set_str in S:
        # текущее множество узлов из супермножества
        curr_set = unpack_set_from_str(curr_set_str)
        # проверим - является ли множество внутренне устойчивым
        if is_inner_stable(curr_set):
            # проверим - является ли множество внешне устойчивым
            if is_outer_stable(curr_set):
                # нашли ядро
                print('Ядро:', curr_set)

    # показать основной граф
    nx.draw(graph, node_color='green', with_labels=True)
    plt.show()

main()



