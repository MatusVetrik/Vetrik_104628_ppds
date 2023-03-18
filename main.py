"""
Program represents implementation of modified hungry savages problem in python.
University: STU Slovak Technical University in Bratislava
Faculty: FEI Faculty of Electrical Engineering and Information Technology
Year: 2023
Resource: https://www.youtube.com/watch?v=54zi8qdBjdk&ab_channel=Mari%C3%A1n%C5%A0ebe%C5%88a
"""

__authors__ = "Marián Šebeňa, Matúš Vetrík"
__emails__ = "mariansebena@stuba.sk, xvetrik@stuba.sk"
__license__ = "MIT"

from fei.ppds import Thread, Mutex, Semaphore, print
from time import sleep

NUM_OF_SAVAGES = 5
NUM_OF_PORTIONS = 3

print(f"\nPočet divochov: {NUM_OF_SAVAGES}")
print(f"Počet porcií: {NUM_OF_PORTIONS}\n")


class Shared:
    """Initialize patterns we need and variables"""

    def __init__(self):
        self.mutex = Mutex()
        self.servings = NUM_OF_PORTIONS
        self.countOfSavages = 0
        self.fullPot = Semaphore(0)
        self.emptyPot = Semaphore(0)
        self.barrier1 = Semaphore(0)
        self.barrier2 = Semaphore(0)


def come_to_dinner(shared, savage_id):
    """Represents situation when savage comes to dinner.
        Arguments:
            shared    -- object of class Shared
            savage_id -- savage id
    """

    shared.countOfSavages += 1
    print(f"Divoch {savage_id} prišiel na večeru. Počet divochov čakajúcich na večeru je {shared.countOfSavages}.")
    sleep(0.2)


def get_serving_from_pot(shared, savage_id):
    """Represents situation when savage is taking portion of food from pot.
        Arguments:
            shared    -- object of class Shared
            savage_id -- savage id
    """

    print(f"Divoch {savage_id} si berie porciu.")
    shared.servings = shared.servings - 1
    print(f"Divoch {savage_id} hoduje. Počet zostávajúcich porcií v hrnci je {shared.servings}.")
    sleep(1)


def savage(shared, savage_id):
    """Function savage represents savage.
        Arguments:
            shared    -- object of class Shared
            savage_id -- savage id
    """

    while True:
        shared.mutex.lock()
        come_to_dinner(shared, savage_id)
        if shared.countOfSavages == NUM_OF_SAVAGES:
            print(f'Všetci divosi sa zišli, ide sa hodovať.')
            shared.barrier1.signal(NUM_OF_SAVAGES)
        shared.mutex.unlock()
        shared.barrier1.wait()

        shared.mutex.lock()
        get_serving_from_pot(shared, savage_id)
        if shared.servings == 0:
            print(f"Hrniec je prázdny. Divoch {savage_id} budí kuchára.")
            shared.emptyPot.signal()
            shared.fullPot.wait()
            put_servings_in_pot(shared)
        shared.mutex.unlock()

        shared.mutex.lock()
        shared.countOfSavages -= 1
        if shared.countOfSavages == 0:
            shared.barrier2.signal(NUM_OF_SAVAGES)
        shared.mutex.unlock()
        shared.barrier2.wait()


def put_servings_in_pot(shared):
    """Represents situation when cook fill up pot with food.
        Arguments:
            shared    -- object of class Shared
    """

    print("Kuchár pridal guláš do hrnca.")
    shared.servings = NUM_OF_PORTIONS
    sleep(1.5)


def cook(shared):
    """Function cook represents cook.
        Arguments:
            shared    -- object of class Shared
    """

    while True:
        shared.emptyPot.wait()
        print("Kuchár varí.")
        sleep(3)
        shared.fullPot.signal()


def main():
    """Run main."""

    shared: Shared = Shared()
    savages: list[Thread] = [
        Thread(savage, shared, i) for i in range(NUM_OF_SAVAGES)
    ]
    cook_thread = Thread(cook, shared)
    for s in savages + [cook_thread]:
        s.join()


if __name__ == "__main__":
    main()
