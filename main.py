"""This module implements dinning philosophers problem.

 Left-handed and right-handed philosophers solution is implemented.
 """

__authors__ = "Tomáš Vavro, Matúš Vetrík"
__emails__ = "xvavro@stuba.sk, xvetrik@stuba.sk"
__license__ = "MIT"

from fei.ppds import Thread, Mutex, Semaphore, print
from time import sleep

NUM_PHILOSOPHERS: int = 4
NUM_RUNS: int = 10  # number of repetitions of think-eat cycle of philosophers


class Shared:
    """Represent shared data for all threads."""

    def __init__(self):
        """Initialize an instance of Shared."""
        self.forks = [Mutex() for _ in range(NUM_PHILOSOPHERS)]


def think(i: int):
    """Simulate thinking.

    Args:
        i -- philosopher's id
    """
    print(f"Philosopher {i} is thinking!")
    sleep(0.5)


def eat(i: int):
    """Simulate eating.

    Args:
        i -- philosopher's id
    """
    print(f"Philosopher {i} is eating!")
    sleep(0.5)


def pick_up_left_fork_first(shared: Shared, i: int):
    """Pick up left fork first.

    Args:
        i -- philosopher's id
        shared -- shared data
    """
    shared.forks[(i + 1) % NUM_PHILOSOPHERS].lock()
    sleep(0.5)
    shared.forks[i].lock()


def pick_up_right_fork_first(shared: Shared, i: int):
    """Pick up right fork first.

    Args:
        i -- philosopher's id
        shared -- shared data
    """
    shared.forks[i].lock()
    sleep(0.5)
    shared.forks[(i + 1) % NUM_PHILOSOPHERS].lock()


def put_down_left_fork_first(shared: Shared, i: int):
    """Put down right fork first.

    Args:
        i -- philosopher's id
        shared -- shared data
    """
    shared.forks[(i + 1) % NUM_PHILOSOPHERS].unlock()
    shared.forks[i].unlock()


def put_down_right_fork_first(shared: Shared, i: int):
    """Put down right fork first.

    Args:
        i -- philosopher's id
        shared -- shared data
    """
    shared.forks[i].unlock()
    shared.forks[(i + 1) % NUM_PHILOSOPHERS].unlock()


def philosopher(i: int, shared: Shared):
    """Run philosopher's code.

    Args:
        i -- philosopher's id
        shared -- shared data
    """
    for _ in range(NUM_RUNS):
        think(i)
        if i % 2 == 0:
            pick_up_left_fork_first(shared, i)
        else:
            pick_up_right_fork_first(shared, i)
        eat(i)
        if i % 2 == 0:
            put_down_left_fork_first(shared, i)
        else:
            put_down_right_fork_first(shared, i)


def main():
    """Run main."""
    shared: Shared = Shared()
    philosophers: list[Thread] = [
        Thread(philosopher, i, shared) for i in range(NUM_PHILOSOPHERS)
    ]
    for p in philosophers:
        p.join()


if __name__ == "__main__":
    main()
