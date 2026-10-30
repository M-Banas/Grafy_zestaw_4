import random


class Digraph:
    def __init__(self, n):
        self.n = n
        self.adj_list = {v: [] for v in range(1, n + 1)}

    def add_edge(self, u, v):
        self.adj_list[u].append(v)

    def edges(self):
        return [(u, v) for u in range(1, self.n + 1) for v in sorted(self.adj_list[u])]

    def transpose(self):
        gt = Digraph(self.n)
        for u, v in self.edges():
            gt.add_edge(v, u)
        return gt


    def adjacency_list(self):
        return [(v, sorted(self.adj_list[v])) for v in range(1, self.n + 1)]

    def adjacency_matrix(self):
        m = [[0] * self.n for _ in range(self.n)]
        for u, v in self.edges():
            m[u - 1][v - 1] = 1
        return m

    def incidence_matrix(self):
        edges = self.edges()
        m = [[0] * len(edges) for _ in range(self.n)]
        for k, (u, v) in enumerate(edges):
            m[u - 1][k] = -1
            m[v - 1][k] = 1
        return m


    def format_adjacency_list(self):
        return "\n".join(
            f"{v}.  " + " ".join(map(str, nbrs)) if nbrs else f"{v}."
            for v, nbrs in self.adjacency_list()
        )

    def format_adjacency_matrix(self):
        return format_matrix(self.adjacency_matrix())

    def format_incidence_matrix(self):
        return format_matrix(self.incidence_matrix())

    @classmethod
    def from_adjacency_list(cls, text):
        """ Tutaj wczytujemy graf format:
          `v. u1 u2 ...`"""
        rows = {}
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            head, _, rest = line.partition(".")
            rows[int(head)] = [int(x) for x in rest.split()]
        n = max(rows) if rows else 0
        g = cls(n)
        for u, nbrs in rows.items():
            for v in nbrs:
                if not 1 <= v <= n:
                    raise ValueError(f"wierzchołek {v} spoza zakresu 1..{n} nie powinno tak byc")
                g.add_edge(u, v)
        return g


def format_matrix(m):
    if not m or not m[0]:
        return ""
    width = max(len(str(x)) for row in m for x in row)
    return "\n".join(" ".join(str(x).rjust(width) for x in row) for row in m)

#digraf prosty
def random_digraph(n, p):
    if n < 1 or not(0 <= p <= 1):
        raise ValueError("n musi być dodatnie, p ~ [0,1]")
    g = Digraph(n)
    for u in range(1, n + 1):
        for v in range(1, n + 1):
            if u != v and random.random() < p:
                g.add_edge(u, v)
    return g
