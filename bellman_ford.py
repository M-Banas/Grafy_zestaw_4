"""Algorytm Bellmana-Forda – najkrótsze ścieżki z jednego źródła (wagi mogą być ujemne)."""

INF = float("inf")


def bellman_ford(g, weights, s):
    """Zwraca (dist, pred, cycle).

    Gdy nie ma ujemnego cyklu osiągalnego z s: cycle = None, a dist i pred są poprawne.
    Gdy jest: dist = pred = None, a cycle to lista wierzchołków ujemnego cyklu [x, ..., x].
    """
    dist = {v: INF for v in g.adj_list}
    pred = {v: None for v in g.adj_list}
    dist[s] = 0
    edges = g.edges()

    for _ in range(g.n - 1):
        changed = False
        for u, v in edges:
            if dist[u] != INF and dist[u] + weights[(u, v)] < dist[v]:
                dist[v] = dist[u] + weights[(u, v)]
                pred[v] = u
                changed = True
        if not changed:  # wcześniejsze zakończenie
            break

    # n-ta runda: jeśli coś się jeszcze poprawia, to jest ujemny cykl
    for u, v in edges:
        if dist[u] != INF and dist[u] + weights[(u, v)] < dist[v]:
            pred[v] = u
            x = v
            for _ in range(g.n):  # n cofnięć gwarantuje wejście na cykl
                x = pred[x]
            cycle = [x]
            y = pred[x]
            while y != x:
                cycle.append(y)
                y = pred[y]
            cycle.append(x)
            cycle.reverse()
            return None, None, cycle

    return dist, pred, None


def path_to(pred, s, v):
    """Odtwarza najkrótszą ścieżkę s -> v z tablicy poprzedników."""
    path = [v]
    while path[-1] != s:
        path.append(pred[path[-1]])
    return path[::-1]