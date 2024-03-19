

from functools import reduce
import logging
import random
import sys
from threading import Lock, Thread
import time


logging.basicConfig(
    format="%(asctime)s\t%(levelname)s\t%(thread)d\t%(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
    stream=sys.stderr,
    level=logging.INFO,
)

def task_1():
    p = 0.9
    x = 5.5
    y = 6.7
    results = {}
    def compute_t1():
        logging.info("Start computing t1")
        time.sleep(1)
        results["t1"] = x + y
        logging.info("Done computing t1")

    def compute_t2():
        logging.info("Start computing t2")
        time.sleep(1)
        results["t2"] = x - y
        logging.info("Done computing t2")

    def log_result():
        result = results["t1"] if p < 0 else results["t2"]
        logging.info(f"Result is {result}")


    logging.info("SEQ: Start calculating result")
    compute_t1()
    compute_t2()
    log_result()
    logging.info("SEQ: Done calculating result")

    results = {}

    logging.info("PAR: Start calculating result")
    jobs = [
        Thread(target=compute_t1),
        Thread(target=compute_t2)
    ]
    [j.start() for j in jobs]
    [j.join() for j in jobs]
    log_result()
    logging.info("PAR: Done calculating result")


def task_2_3(reducer):
    n = 12
    numbers = list(random.sample(range(1, 101), n))
    logging.info(f"NUMBERS: {numbers}")

    logging.info("SEQ: Start calculating result")
    min_number = reduce(reducer, numbers)
    logging.info(f"Result is {min_number}")
    logging.info("SEQ: Done calculating result")

    logging.info("PAR: Start calculating result")
    results = []
    jobs = [
        Thread(target=lambda: results.append(reduce(reducer, numbers[:len(numbers) // 2:]))),
        Thread(target=lambda: results.append(reduce(reducer, numbers[len(numbers) // 2:]))),
    ]
    [j.start() for j in jobs]
    [j.join() for j in jobs]
    logging.info(f"Result is {reducer(results[0], results[1])}")
    logging.info("PAR: Done calculating result")


def task_2():
    def reducer(x, y):
        time.sleep(0.5)
        if x < y:
            return x
        return y
    task_2_3(reducer)


def task_3():
    def reducer(x, y):
        time.sleep(0.5)
        if x > y:
            return x
        return y
    task_2_3(reducer)


def task_4():
    N = [1, 2, 3, 3, 4, 5, 6, 7, -8, -9, -6]

    def reducer(acc, x):
        time.sleep(0.5)
        acc["mutex"].acquire()
        if x > 0:
            acc["positive"] += 1
        elif x < 0:
            acc["negative"] += 1
        else:
            ... # NOTE: do nothing on zero
        acc["mutex"].release()
        return acc

    result = {"positive": 0, "negative": 0, "mutex": Lock()}
    logging.info("SEQ: Start calculating result")

    result = reduce(reducer, N, result)
    result.pop("mutex")

    logging.info(f"Result is {result}")
    logging.info("SEQ: Done calculating result")

    result = {"positive": 0, "negative": 0, "mutex": Lock()}
    logging.info("PAR: Start calculating result")

    jobs = [
        Thread(target=lambda: reduce(reducer, N[:len(N) // 2:], result)),
        Thread(target=lambda: reduce(reducer, N[len(N) // 2:], result)),
    ]
    [j.start() for j in jobs]
    [j.join() for j in jobs]
    result.pop("mutex")
    logging.info(f"Result is {result}")
    logging.info("PAR: Done calculating result")


if __name__ == "__main__":
    func_name = sys.argv[1]
    logging.info(f"{func_name.upper()}: Start")
    globals()[func_name]()
    logging.info(f"{func_name.upper()}: Done")
