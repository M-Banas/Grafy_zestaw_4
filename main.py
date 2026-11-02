import argparse
import sys

from digraph import Digraph, random_digraph
from kosaraju import components, kosaraju
from generator import random_strongly_connected, random_weights
from bellman_ford import bellman_ford, path_to, INF


def parse_args():
    ap = argparse.ArgumentParser(
        description="Generuje losowy digraf oraz  wyznacza jego silnie spójne składowe"
    )
    ap.add_argument("-n", type=int, help="liczba wierzchołków")
    ap.add_argument("-p", type=float, help="prawdopodobieństwo istnienia łuku, 0..1")
    ap.add_argument("-s", type=int, default=1,
                    help="wierzchołek źródłowy dla Bellmana-Forda (domyślnie 1)")
    ap.add_argument("--input", metavar="PLIK",
                    help="wczytaj graf z pliku w formacie listy sąsiedztwa")
    ap.add_argument("--format", choices=["list", "matrix", "incidence", "all"], default="list",
                    help="reprezentacja grafu na wyjściu (domyślnie: list)")
    ap.add_argument("--times", action="store_true",
                    help="wypisz czasy odwiedzenia d[v] i przetworzenia f[v] z pierwszego DFS")
    args = ap.parse_args()
    if args.input is None and (args.n is None or args.p is None):
        ap.error("podaj -n i -p albo --input")
    return args


def print_graph(g, fmt):
    sections = {
        "list": ("Lista sąsiedztwa", g.format_adjacency_list),
        "matrix": ("Macierz sąsiedztwa", g.format_adjacency_matrix),
        "incidence": ("Macierz incydencji", g.format_incidence_matrix),
    }
    chosen = sections if fmt == "all" else {fmt: sections[fmt]}
    for title, render in chosen.values():
        print(f"{title}:")
        print(render())
        print()


def print_times(d, f):
    w = len(str(max(f.values(), default=0)))
    print("Czasy DFS (v: d[v]/f[v]):")
    for v in sorted(d):
        print(f"  {v}: {d[v]:>{w}}/{f[v]:>{w}}")
    print()


def print_weighted(g, weights):
    print("Lista sąsiedztwa z wagami (v: u(w) ...):")
    for v in range(1, g.n + 1):
        nbrs = " ".join(f"{u}({weights[(v, u)]})" for u in sorted(g.adj_list[v]))
        print(f"  {v}.  {nbrs}")
    print()


def main():
    args = parse_args()

    if args.input is not None:
        text = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
        g = Digraph.from_adjacency_list(text)
    else:
        g = random_digraph(args.n, args.p)

    print(f"Digraf: n = {g.n}, liczba łuków = {len(g.edges())}\n")
    print_graph(g, args.format)

    comp, d, f = kosaraju(g)
    groups = components(comp)

    if args.times:
        print_times(d, f)

    print(f"Silnie spójne składowe ({len(groups)}):")
    for i, group in enumerate(groups, 1):
        print(f"  {i}: " + " ".join(map(str, group)))
    print()
    print("Graf jest silnie spójny" if len(groups) == 1 else "Graf nie jest silnie spójny")

    if args.n is None or args.p is None:
        return  
    if not 1 <= args.s <= args.n:
        print(f"\nPomijam zad. 3: -s musi należeć do 1..{args.n}")
        return

    print("\n" + "=" * 50)
    print("losowy silnie spójny digraf z wagami + Bellman-Ford")
    print("=" * 50 + "\n")

    gs, attempts = random_strongly_connected(args.n, args.p)
    print(f"Digraf silnie spójny: n = {gs.n}, liczba łuków = {len(gs.edges())} "
          f"(wylosowano w {attempts} próbach)\n")

    weights = random_weights(gs)
    print_weighted(gs, weights)

    dist, pred, cycle = bellman_ford(gs, weights, args.s)
    if cycle is not None:
        total = sum(weights[(cycle[i], cycle[i + 1])] for i in range(len(cycle) - 1))
        print("Wykryto ujemny cykl osiągalny ze źródła – najkrótsze ścieżki nie istnieją.")
        print("Cykl: " + " -> ".join(map(str, cycle)) + f"  (waga = {total})")
        return

    print(f"Najkrótsze ścieżki ze źródła s = {args.s}:")
    for v in range(1, gs.n + 1):
        if dist[v] == INF:
            print(f"  {args.s} -> {v}: brak ścieżki")
        else:
            path = " -> ".join(map(str, path_to(pred, args.s, v)))
            print(f"  {args.s} -> {v}: d = {dist[v]:>4},  ścieżka: {path}")


if __name__ == "__main__":
    main()