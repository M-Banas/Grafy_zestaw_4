"""Zestaw 4, zad. 1 i 2: losowy digraf G(n, p) i silnie spójne składowe (Kosaraju)."""

import argparse
import sys

from digraph import Digraph, random_digraph
from kosaraju import components, kosaraju


def parse_args():
    ap = argparse.ArgumentParser(
        description="Generuje losowy digraf oraz  wyznacza jego silnie spójne składowe"
    )
    ap.add_argument("-n", type=int, help="liczba wierzchołków")
    ap.add_argument("-p", type=float, help="prawdopodobieństwo istnienia łuku, 0..1")
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


if __name__ == "__main__":
    main()
