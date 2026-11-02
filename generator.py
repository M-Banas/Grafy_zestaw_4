import random

from digraph import random_digraph
from kosaraju import is_strongly_connected


def random_strongly_connected(n, p, max_attempts=100000):
    """Losuje G(n, p) aż do uzyskania digrafu silnie spójnego (test Kosaraju)."""
    for attempt in range(1, max_attempts + 1):
        g = random_digraph(n, p)
        if is_strongly_connected(g):
            return g, attempt
    raise RuntimeError(
        f"Nie udało się wylosować silnie spójnego digrafu w {max_attempts} próbach "
        f"– zwiększ p (orientacyjnie p >= ln(n)/n)"
    )


def random_weights(g, lo=-5, hi=10):
    """Losowe wagi całkowite z [lo, hi] dla każdego łuku: {(u, v): w}."""
    return {(u, v): random.randint(lo, hi) for u, v in g.edges()}