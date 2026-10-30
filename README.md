## Uruchamianie

```bash
python3 main.py -n N -p P [--format list|matrix|incidence|all] [--times]
python3 main.py --input PLIK [--format ...] [--times]
```

| Opcje | Znaczenie |
|---|---|
| `-n` | liczba wierzchołków s |
| `-p` | prawdopodobieństwo istnienia łuku `u → v`|
| `--input PLIK` | Wczytaje graf z pliku|
| `--format` | reprezentacja grafu na wyjściu: `list` (default u nas), `matrix`, `incidence`, `all` |
| `--times` | wypisuje czasy odwiedzenia `d[v]` i przetworzenia `f[v]` z pierwszego DFS |

### Przykłady

Losowy digraf o 7 wierzchołkach, `p = 0.3`, wszystkie reprezentacje:

```bash
python3 main.py -n 7 -p 0.3 --format all
```

Albo z pliku:

```bash
python3 main.py --input example_graph.txt --format all
```

Wynik:

```
Lista sąsiedztwa:
1.  2 3 5
2.  1 3 4 5 7
...
Silnie spójne składowe (1):
  1: 1 2 3 4 5 6 7

Macierz incydencji:
-1 -1  1  0  0  0  0  1  0  0  0  0  0  0  0  0  0
 0  0 -1 -1  1  0  0  0  0  0  0  0  0  0  0  0  0
 1  0  0  0 -1 -1 -1  0  0  0  0  0  1  0  0  0  0
...

Silnie spójne składowe (3):
  1: 9
  2: 1 2 3 4 5 6 7 8
  3: 10

Graf nie jest silnie spójny
```

## Co wypisuje program

* liczbę wierzchołków i łuków,
* graf w wybranej reprezentacji:
  * **lista sąsiedztwa**
  * **macierz sąsiedztwa**
  * **macierz incydencji**
* (z `--times`) czasy `d[v]/f[v]` z pierwszego DFS,
* silnie spójne składowe (numerowane w kolejności ich znajdowania) i informację, czy graf jest silnie spójny.

## Jak działa Kosaraju w tym programie

1. Pierwsze DFS po `G` liczy czasy `d[v]`, `f[v]`; wierzchołek trafia na stos w momencie zakończenia przetwarzania.
2. Budowany jest graf transponowany `Gt`.
3. Wierzchołki są ściągane ze stosu (malejące `f[v]`); z każdego jeszcze nieodwiedzonego uruchamiane jest DFS po `Gt`, które oznacza jedną składową.

DFS jest zapisany iteracyjnie.


