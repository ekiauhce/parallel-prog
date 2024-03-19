

import math
import time
import matplotlib.pyplot as plt
import numpy as np
from numba import njit, prange, set_num_threads
import statistics




def make_random_matrix(n, m):
    return np.random.randint(-100, 100, size=(n,m))


def make_empty_matrix(n, m):
    return [[math.nan for _ in range(m)] for _ in range(n)]


@njit(parallel=True)
def mat_mult(A, B):
    assert A.shape[1] == B.shape[0]
    res = np.zeros((A.shape[0], B.shape[1]), )
    for i in prange(A.shape[0]):
        for k in range(A.shape[1]):
            for j in range(B.shape[1]):
                res[i,j] += A[i,k] * B[k,j]
    return res


def func(a, b):
    durations = []
    for _ in range(0, 5):
        start = time.perf_counter_ns()
        mat_mult(a, b)
        duration = (time.perf_counter_ns() - start) / 1_000_000.
        durations.append(duration)

    return statistics.median(durations)


if __name__ == "__main__":
    ns = [int(100 * 2**i) for i in range(-1, 5)]
    labels = [f"{i}x{i}" for i in ns]
    thread_counts = [2, 4]

    matrices = []
    for n in ns:
        a = make_random_matrix(n, n)
        b = make_random_matrix(n, n)
        matrices.append((a, b))

    for threads_count in thread_counts:
        set_num_threads(threads_count)
        durations = []
        for a, b in matrices:
            duration = func(a, b)
            durations.append(duration)
        plt.scatter(ns, durations)
        plt.plot(ns, durations, label=f"threads count = {threads_count}")

    plt.legend()
    plt.xticks(ns, labels)
    plt.ylabel("A * B duration, ms")
    plt.show()