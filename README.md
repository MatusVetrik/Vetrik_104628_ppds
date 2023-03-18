# Modified hungry savages problem

### Problem

We are dealing with modified hungry savages problem. The problem is about interaction between multiple savages and 
cook. At first all savages meets before feast. When they are all together they come to pot and start taking portions
of food and eating. When pot is empty, they wakes up cook. Cook starts cooking another portions. When cook is done
with cooking, he takes portions of food and fills up pot with food. Once again, savages meets and so on. 

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

In our solution we are tracking multiple situations in proces. We are assuming that pot is already filled up.
At first, we are tracking when savage arrives to dinner. We are incrementing counter of savages waiting for
dinner to start. All waiting savages are hold back by barrier. We are simulating arrive time with 0.2 seconds.

```commandline
def come_to_dinner(shared, savage_id):
    """Represents situation when savage comes to dinner.
        Arguments:
            shared    -- object of class Shared
            savage_id -- savage id
    """

    shared.countOfSavages += 1
    print(f"Divoch {savage_id} prišiel na večeru. Počet divochov čakajúcich na večeru je {shared.countOfSavages}.")
    sleep(0.2)
```
Integrity of counter is secured by mutex. When last savage comes, we give a signal, and it is time for feast. 

```commandline    
shared.mutex.lock()
come_to_dinner(shared, savage_id)
if shared.countOfSavages == NUM_OF_SAVAGES:
    print(f'Všetci divosi sa zišli, ide sa hodovať.')
    shared.barrier1.signal(NUM_OF_SAVAGES)
shared.mutex.unlock()
shared.barrier1.wait()
```
Then savages one by one taking portions from pot. Simulation of taking portion is 1 second. By every portion taken
we are decrementing counter of portions in pot. 

```commandline
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
```

When savage take last portion, next savage gives signal that pot is empty and wakes up cook.

```commandline
shared.mutex.lock()
if shared.servings == 0:
    print(f"Hrniec je prázdny. Divoch {savage_id} budí kuchára.")
    shared.emptyPot.signal()
    shared.fullPot.wait()
    put_servings_in_pot(shared)
get_serving_from_pot(shared, savage_id)
shared.mutex.unlock()
```

When empty pot signal is given, cook starts cooking. Cooking simulation time is 3 seconds. When cooking is done,
cook gives signal that pot is finally full.

```commandline
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
```


Of course, when savage leave we must decrement counter of savages. When last savage is fed and leave, he gives signal
that all savages can meet up once again.

```commandline
shared.mutex.lock()
shared.countOfSavages -= 1
if shared.countOfSavages == 0:
    print("Všetci divosi sa najedli.")
    sleep(0.5)
    shared.barrier2.signal(NUM_OF_SAVAGES)
shared.mutex.unlock()
shared.barrier2.wait()
```

### Result

![logs.png](assets%2Fimages%2Flogs.png)

We are testing functionality with 5 savages and pot with capacity of 3 servings. It is accurate count for obvious
demonstration that our implementation is correct. In result, we can see that savages are coming one by one. When are 
all together they can start feast. Savage takes portion, and we are giving information about number of portions left in
the pot. When pot is empty savage wakes up cook. Cook is cooking and after that he fills up pot. Then remaining savages
feast. When all savages are fed and there is remaining portions in pot, they meet up and start taking portions again. 
And same cycle again and again and again and they live happily ever after... 

