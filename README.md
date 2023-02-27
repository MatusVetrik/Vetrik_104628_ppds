## Bakery Algorithm

### Problem

In this branch we are dealing with problem of synchronization between processes.
We are implementing Bakery algorithm which is one of the simplest known solution 
for critical section solution for N processes.

### How to run code

We are implementing algorithm with using these two modules.
```commandline
from fei.ppds import Thread
from time import sleep
```
Time is default python module which you probably alreaddy have. For instalation 
of fei.ppds module you should run this command in terminal.
```commandline
pip install --user fei.ppds
```
There is a critical section area where you can enter your custom complicate computation.

### Solution

Implementation of Bakery algorithm pseudocode in python.
```commandline
Initialization
_______________________________________________________
num ← [0, . . . , 0]            --▷ array of length N
in ← [0, . . . , 0]             --▷ array of length N


Process
_______________________________________________________
i ← thread id
in[i] ← 1
num[i] ← 1 + max(num[0], . . . , num[N − 1])
in[i] ← 0
for j ∈ Z : 0 ≤ j < N do
    while in[j] = 1 do
        wait
    while num[j] ̸= 0 ∧
      (num[j] < num[i] ∨ (num[j] = num[i] ∧ j < i)) do
        wait
. . .                           --▷ critical section
num[i] ← 0
```

### Testing

For demonstration that our code is running properly we will test with 10 threads,
with 10 loops and with critical section containing sleep for 1 second. After running
code we have in console messages "Process XYZ runs a complicated computation!" where 
XYZ is representing thread id. If code ran correctly all thread ids should be in 
ascending order. 

### Why Bakery algorithm ?

There are 4 rules of correct solution of mutual exclusion. 

1. In the critical area, no more than one process may be performed at the time.

* Each process is assigned order number, which describe order of processes entering
critical section. Process waits until his order number is smallest. In corner case, 
when 2 processes have same number we have this condition which will choose process 
with the smallest process id. This is secured by next condition. 

```commandline
while threads_order[j] != 0\
        and (threads_order[j] < threads_order[i] or (threads_order[j] == threads_order[i] and j < i)):
    continue

```

2. The process that is computing outside the critical area must not hinder others
enter it.

* Each process after getting order number is waiting in line for time to enter 
critical section and its not denying other processes to enter critical section.

3. The decision on entering must come within the deadline.

*  The decision on entering the critical section is made in limited time because
at least one process have bigger value in thread_orders array. Because of this, 
when looping through processes, process is always chosen. 

4. Processes cannot assume anything when entering the critical area about
mutual timing (planning).

*  Every process must wait until its turn on entering critical section. Each 
process only knows if is allowed to enter or not without information about
other processes plans.
