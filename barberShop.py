"""
Program represents implementation of sleeping barber problem in python.

University: STU Slovak Technical University in Bratislava
Faculty: FEI Faculty of Electrical Engineering and Information Technology
Year: 2023
"""

__authors__ = "Marián Šebeňa, Matúš Vetrík"
__emails__ = "mariansebena@stuba.sk, xvavro@stuba.sk, xvetrik@stuba.sk"
__license__ = "MIT"

from fei.ppds import Mutex, Thread, print, Semaphore
from time import sleep
from random import randint

numOfCustomers = 5
sizeOfWaitingRoom = 3


class Shared(object):
    """Initialize patterns we need and variables
    """

    def __init__(self):
        self.mutex = Mutex()
        self.waiting_room = 0
        self.customer = Semaphore(0)
        self.barber = Semaphore(0)
        self.customer_done = Semaphore(0)
        self.barber_done = Semaphore(0)


def get_haircut(i):
    """Simulate time and print info when customer gets haircut
        Arguments:
            i      -- customer id
    """

    print(f'Customer {i} is getting haircut.')
    sleep(2)


def cut_hair():
    """Simulate time and print info when barber cuts customer's hair
    """

    print(f'Barber is cutting hair.')
    sleep(2)


def balk(i):
    """Represents situation when waiting room is full and print info
        Arguments:
            i      -- customer id
    """

    print(f'Waiting room is full. Customer {i} is waiting for seat.')
    sleep(randint(3, 5))


def growing_hair(i):
    """Represents situation when customer wait after getting haircut. So hair is growing and customer is sleeping for
    some time
        Arguments:
            i      -- customer id
    """

    print(f'Customer {i} is growing hair.')
    sleep(randint(4, 6))


def customer(i, shared):
    """Function represents customers behaviour.
        Arguments:
            i      -- customer id
            shared -- object of class Shared
    """

    while True:
        shared.mutex.lock()
        if shared.waiting_room >= sizeOfWaitingRoom:
            balk(i)
        shared.waiting_room += 1
        print(f"Customer {i} entered room.")
        shared.mutex.unlock()

        shared.customer.signal()
        shared.barber.wait()

        get_haircut(i)

        shared.customer_done.signal()
        shared.barber_done.wait()

        shared.mutex.lock()
        shared.waiting_room -= 1
        shared.mutex.unlock()

        growing_hair(i)


def barber(shared):
    """Function barber represents barber.
        Arguments:
            shared -- object of class Shared
    """

    while True:
        shared.customer.wait()
        shared.barber.signal()

        cut_hair()

        shared.customer_done.wait()
        shared.barber_done.signal()


def main():
    """Main function
    """

    shared = Shared()
    customers = []

    for i in range(numOfCustomers):
        customers.append(Thread(customer, i, shared))
    hair_stylist = Thread(barber, shared)

    for t in customers + [hair_stylist]:
        t.join()


if __name__ == "__main__":
    main()
