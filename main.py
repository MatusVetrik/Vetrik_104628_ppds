"""This module contains an implementation of bakery algorithm.
Bakery algorithm assures mutual exclusion of N threads.
"""

__authors__ = "Tomáš Vavro, Matúš Vetrík"
__emails__ = "xvavro@stuba.sk, xvetrik@stuba.sk"
__license__ = "MIT"

from fei.ppds import Thread
from time import sleep

NUM_THREADS = 10
threads_order = [0] * NUM_THREADS
current_in = [0] * NUM_THREADS


def process(tid: int, num_runs: int):
    """Simulates a process.
    Arguments:
        tid      -- thread id
        num_runs -- number of executions of the critical section
    """

    global threads_order, current_in, NUM_THREADS

    for _ in range(num_runs):
        i = tid
        current_in[i] = 1
        threads_order[i] = 1 + max(threads_order)
        current_in[i] = 0

        for j in range(NUM_THREADS):
            while current_in[j] == 1:
                continue
            while threads_order[j] != 0\
                    and (threads_order[j] < threads_order[i] or (threads_order[j] == threads_order[i] and j < i)):
                continue

        # execute critical section
        print(f"Process {tid} runs a complicated computation!")
        sleep(1)

        # leaving critical section
        threads_order[i] = 0


if __name__ == '__main__':
    DEFAULT_NUM_RUNS = 10
    threads = [Thread(process, i, DEFAULT_NUM_RUNS) for i in range(NUM_THREADS)]
    [t.join() for t in threads]
