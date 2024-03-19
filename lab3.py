
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait
from threading import Thread
import time
import numpy as np
import matplotlib.pyplot as plt
import statistics


def partition(array, low, high):
    pivot = array[high]
    i = low - 1
    for j in range(low, high):
        if array[j] <= pivot:
            i = i + 1
            array[i], array[j] = array[j], array[i]
    array[i + 1], array[high] = array[high], array[i + 1]
    return i + 1


def quick_sort(array, low, high, depth, k, executor):
    if low < high:
        pi = partition(array, low, high)
        if depth <= k:
            jobs = [
                executor.submit(quick_sort, (array, low, pi - 1, depth + 1, k)),
                executor.submit(quick_sort, (array, pi + 1, high, depth + 1, k))
            ]
            wait(jobs)


def make_random_array(n):
    return np.random.randint(-100, 100, size=(n,))


if __name__ == "__main__":
    ks = list(range(6))
    pows = list(range(10, 21))
    array_sizes = [2**i for i in pows]
    labels = [f"2^{p}" for p in pows]

    executor = ThreadPoolExecutor(max_workers=40)
    for k in ks:
        durations = []
        for array_size in array_sizes:
            ds = []
            for _ in range(10):
                data = make_random_array(array_size)
                start = time.perf_counter_ns()
                quick_sort(data, 0, len(data) - 1, depth=1, k=k, executor=executor)
                duration = (time.perf_counter_ns() - start) / 1_000_000.
                ds.append(duration)
            durations.append(statistics.median(ds))

        plt.scatter(array_sizes, durations)
        plt.plot(array_sizes, durations, label=f"k = {k}")

    executor.shutdown()

    plt.legend()
    plt.xticks(array_sizes, labels)
    plt.ylabel("sort duration, ms")
    plt.show()
