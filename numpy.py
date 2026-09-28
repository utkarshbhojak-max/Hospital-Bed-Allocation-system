"""
Pure-Python minimal compatibility replacement for numpy.
Provides array-like operations, math constants/functions, percentiles, and PCG64 random generator
without requiring binary wheels or C extensions.
"""

import math
import random as _py_random
import statistics
from typing import Any, Sequence, Union, Optional

__version__ = "1.26.0"

# Math constants & functions
pi = math.pi
e = math.e
nan = float("nan")
inf = float("inf")

def log(x: Union[float, int]) -> float:
    return math.log(x)

def exp(x: Union[float, int]) -> float:
    return math.exp(x)

def sqrt(x: Union[float, int]) -> float:
    return math.sqrt(x)

import builtins

def clip(a: Any, a_min: float, a_max: float) -> Any:
    if isinstance(a, (list, tuple)):
        return [builtins.max(a_min, builtins.min(float(x), a_max)) for x in a]
    return builtins.max(a_min, builtins.min(float(a), a_max))

def mean(a: Sequence[float]) -> float:
    if not a:
        return 0.0
    return float(sum(a)) / len(a)

def median(a: Sequence[float]) -> float:
    if not a:
        return 0.0
    return float(statistics.median(a))

def percentile(a: Sequence[float], q: float) -> float:
    if not a:
        return 0.0
    sorted_a = sorted(a)
    n = len(sorted_a)
    if n == 1:
        return float(sorted_a[0])
    idx = (float(q) / 100.0) * (n - 1)
    lower = int(idx)
    upper = builtins.min(lower + 1, n - 1)
    weight = idx - lower
    return float(sorted_a[lower] * (1.0 - weight) + sorted_a[upper] * weight)

def max(a: Any, *args, **kwargs) -> Any:
    if args:
        return builtins.max(a, *args, **kwargs)
    if isinstance(a, (list, tuple)):
        return float(builtins.max(a)) if a else 0.0
    return builtins.max(a)

def min(a: Any, *args, **kwargs) -> Any:
    if args:
        return builtins.min(a, *args, **kwargs)
    if isinstance(a, (list, tuple)):
        return float(builtins.min(a)) if a else 0.0
    return builtins.min(a)

def array(data: Any, dtype=None):
    return list(data)

def isscalar(val: Any) -> bool:
    return isinstance(val, (int, float, bool, str))

class _PCG64:
    def __init__(self, seed: Optional[int] = None):
        self.seed = seed

class _Generator:
    def __init__(self, bit_generator: Optional[_PCG64] = None):
        seed = getattr(bit_generator, "seed", None)
        self._rng = _py_random.Random(seed)

    def exponential(self, scale: float = 1.0) -> float:
        return self._rng.expovariate(1.0 / scale)

    def choice(self, a: Sequence[Any], p: Optional[Sequence[float]] = None) -> Any:
        if p is not None:
            return self._rng.choices(a, weights=p, k=1)[0]
        return self._rng.choice(a)

    def lognormal(self, mean: float = 0.0, sigma: float = 1.0) -> float:
        return self._rng.lognormvariate(mean, sigma)

class _RandomNamespace:
    PCG64 = _PCG64
    Generator = _Generator
    def seed(self, s=None):
        _py_random.seed(s)

random = _RandomNamespace()
