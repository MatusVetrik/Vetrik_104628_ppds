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
