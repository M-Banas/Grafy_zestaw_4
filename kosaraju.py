"""Algorytm Kosaraju – silnie spójne składowe digrafu (implementacja ze stosem)."""


def _dfs_visit(v, g, d, f, t, stack):
    t += 1
    d[v] = t
    for u in g.adj_list[v]:  # przejście po krawędzi (v, u)
        if d[u] == -1:
            t = _dfs_visit(u, g, d, f, t, stack)
    t += 1
    f[v] = t
    stack.append(v)
    return t


def _components_r(nr, v, gt, comp):
    for u in gt.adj_list[v]:
        if comp[u] == -1:
            comp[u] = nr
            _components_r(nr, u, gt, comp)


def kosaraju(g):
    """Zwraca (comp, d, f): numery składowych oraz czasy odwiedzenia i przetworzenia.

    comp, d, f są słownikami indeksowanymi wierzchołkami 1..n; składowe numerowane od 1.
    """
    d = {v: -1 for v in g.adj_list}
    f = {v: -1 for v in g.adj_list}
    t = 0
    stack = []
    for v in g.adj_list:
        if d[v] == -1:
            t = _dfs_visit(v, g, d, f, t, stack)

    gt = g.transpose()
    comp = {v: -1 for v in gt.adj_list}
    nr = 0
    while stack: 
        v = stack.pop()
        if comp[v] == -1:
            nr += 1
            comp[v] = nr
            _components_r(nr, v, gt, comp)
    return comp, d, f


def components(comp):
    """Lista składowych (posortowanych list wierzchołków), w kolejności numerów"""
    nr = max(comp.values(), default=0)
    groups = [[] for _ in range(nr)]
    for v in sorted(comp):
        groups[comp[v] - 1].append(v)
    return groups


def is_strongly_connected(g):
    comp, _, _ = kosaraju(g)
    return len(components(comp)) <= 1
