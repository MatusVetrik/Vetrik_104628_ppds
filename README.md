# Barber shop

### Problem

In this branch we are dealing with problem of sleeping barber. It is famous demonstration of 
solving synchronization problem. Idea of this problem is that barber can only serve one customer
at time, so another customers are waiting in waiting room. Here comes synchronization problem where
customer and barber have to synchronize where barber is cutting hair and customer is getting 
haircut at the same time.

### How to run code

We are implementing solution with using these 3 modules.
```commandline
from fei.ppds import Mutex, Thread, print, Semaphore
from time import sleep
from random import randint
```
`time` and `random` are default python modules which you probably already have. For installation 
of fei.ppds module you should run this command in terminal.
```commandline
pip install --user fei.ppds
```
