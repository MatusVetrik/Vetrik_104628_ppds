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

### Solution 

Solution for synchronization problem is by mutual rendezvous. When customer walks in barber shop barber is
sleeping, he is waiting for customer to come `shared.customer.wait()`. Customer makes signal `shared.customer.signal()` 
that he is ready and wait for barber reaction `shared.barber.wait()`. Barber response `shared.barber.signal()` 
and start cutting customer's hair. In this time, customer `i` is getting haircut `get_haircut(i)` and at
the same time barber is cutting customer's hair `cut_hair()`. When job is done, barber waits `hared.customer_done.wait()`
for customer to make signal `shared.customer_done.signal()` if he is satisfied with his hairs. Customer
than pays for haircut and waits for barber `shared.barber_done.wait()` to receive payment and let him leave
`shared.barber_done.signal()`.

```commandline
--CUSTOMER--

shared.customer.signal()
shared.barber.wait()

get_haircut(i)

shared.customer_done.signal()
shared.barber_done.wait()
```

```commandline
--BARBER--

shared.customer.wait()
shared.barber.signal()

cut_hair()

shared.customer_done.wait()
shared.barber_done.signal()
```
Another problem we are dealing with is size of waiting room where are waiting other customers. Waiting room
have limited seats so not everyone can wait for haircut at the same time. When customer walks in waiting room
and seat is empty, he sits, and we increment counter of customers in waiting room. This computation is our
critical section because only one thread can access it at the same time. To secure integrity of this counter
we use mutex. In case, that waiting room is full of customers, customer leaves and come back in some time.

```commandline
shared.mutex.lock()
if shared.waiting_room >= sizeOfWaitingRoom:
    balk(i)
shared.waiting_room += 1
shared.mutex.unlock()
```

When customer is done after getting haircut, he leaves waiting room, and we decrement counter once and again
with mutex because we have to preserve integrity of counter. When customer is out of waiting room, his hairs
are growing and waits for another time to come back for haircut.

```commandline
shared.mutex.lock()
shared.waiting_room -= 1
shared.mutex.unlock()

growing_hair(i)
```

Some wait times are randomized so every time different operation takes different time, for example growing
hair takes between 4 and 6 sec `sleep(randint(4, 6))`.
