# Dinning philosophers problem

### Problem

Dinning philosophers problem is problem known in parallel programing about multiple threads 
reaching limited resources. Philosophers are sitting at round table and each one have fork 
by left and right hand. At first, philosophers are thinking but by the time they will starve,
so they have to eat. In front of them is big plate with food but every philosopher needs two 
forks(right and left) to be able to eat. When every philosopher take fork by right-hand, last
philosopher will not have fork to eat. We are implementing solution where some philosophers 
are left-handed.

![dining-philosophers-problem.png](assets%2Fimages%2Fdining-philosophers-problem.png)

You can visualize this problem on picture above.



### How to run code

We are implementing solution with using these 3 modules.
```commandline
from fei.ppds import Thread, Mutex, Semaphore, print
from time import sleep
```
`time` is default python module which you probably already have. For installation 
of fei.ppds module you should run this command in terminal.
```commandline
pip install --user fei.ppds
```

### Solution 

Out solution is that one of the philosophers is left-handed. In critical section
where philosophers are picking up forks, we are checking if philosopher `id` is 0. When
`id` is 0, philosopher is left-handed, and he is picking up left fork first.

```commandline
        think(i)
        if i == 0:
            pick_up_left_fork_first(shared, i)
        else:
            pick_up_right_fork_first(shared, i)
        eat(i)
        if i == 0:
            put_down_left_fork_first(shared, i)
        else:
            put_down_right_fork_first(shared, i)
```

With this solution, every philosopher will be fed and starvation does not occur.

### Comparing problem solution with "waiter" solution

There is more than one solution for our problem. We solved problem with solution of left-handed
philosopher. It is hard to tell which solution is better than other, but we can focus on possibility
of starvation in different solution. In solution with left-handed philosopher is granted that everyone
will feast in some time. When at least one philosopher pick fork with left hand, at least one 
philosopher will eat and others will wait for him. When first finish, next in queue will feast. 
But with solution with waiter, there is possibility for starvation. When waiter is choosing which
one will have forks, there is a chance that others will overtake in order. Question of starvation
is resolved by waiter, if he will be manipulated, others may starve to death.


