.. _astronuc:

AstroNuc 2026
=============

.. raw:: html

    <iframe src="../../_static/presentations/astronuc/main.html" width="100%" height="500px"></iframe>

.. button-link:: ../../_static/presentations/astronuc/main.html
    :color: primary
    :shadow:
    :align: center

    View full-screen presentation

.. .. figure:: ../../_static/rabbits.png
..     :align: center
..     :width: 400px
    
..     Rabbits, rabbits everywhere!

.. Overview
.. --------

.. Picture a remote island, filled with luscious green grass and lettuce and perfect weather. A few rabbits arrive on the island and decide to make it their new home. As you know, there's nothing a rabbit loves more than to multiply! Your task is to write a program that simulates the growth of the rabbit population on this island over a number of months.

.. You will add code to the ``problems/populations.py`` file to model the rabbit population growth.

.. You can run this program from the command line, passing in parameters for the initial population size, fertility rate, and number of months to simulate. For example:

.. .. code-block:: bash

..     python problems/populations.py -s 10 -f 4 -m 3

.. I've set up the command line argument parsing for you; your job is to implement the population growth logic. Right now it'll always just return 0 (oh no, where did the rabbits go?!).

.. Part one: Basic Population Growth
.. ---------------------------------

.. Start by simulating the rabbit population growth without any constraints. You'll be modifying the ``growth`` function in ``problems/populations.py``. The function takes three parameters:

.. - ``n_start``: The initial number of rabbits on the island
.. - ``fertility``: The average number of offspring each *pair* of rabbits produce per month
.. - ``months``: The number of months to simulate

.. These are very romantic rabbits that mate for life! That means that only pairs of rabbits can produce offspring. For example, if there are 10 rabbits on the island, there are 5 pairs, and if the fertility rate is 4, then those 5 pairs will produce a total of 20 new rabbits in one month. But if there were 11 rabbits, there would still only be 5 pairs (the extra rabbit is single 😭), and they would still only produce 20 new rabbits in one month.

.. These rabbits are magical and **immortal** (because who wants to think about death in a rabbit population problem?). So once a rabbit is born, it will live forever and continue to reproduce according to the fertility rate.

.. Your task is to implement the population growth logic in the ``growth`` function. The function should return the total rabbit population after the specified number of months.

.. Here are some test cases your function should pass:

.. .. code-block:: python

..     # the syntax for running your function looks like
..     # python problems/populations.py -p 1 -s <starting_population> -f <fertility_rate> -m <months>
..     # the parameter -p 1 indicates that we want to test part one of the problem

..     # expected output: 3
..     python problems/populations.py -p 1 -s 2 -f 1 -m 1

..     # expected output: 1234
..     python problems/populations.py -p 1 -s 10 -f 1 -m 12

..     # expected output: 67108865
..     python problems/populations.py -p 1 -s 5 -f 2 -m 24

..     # expected output: 21767823360
..     python problems/populations.py -p 1 -s 10 -f 10 -m 12


.. Part two: Timing growth
.. -----------------------

.. Now let's instead consider how long it takes a rabbit population to reach a certain size. The ``time_to_target`` function in ``problems/populations.py`` takes three parameters:

.. - ``n_start``: The initial number of rabbits on the island
.. - ``fertility``: The average number of offspring each *pair* of rabbits produce per month
.. - ``target``: The target population size

.. Your task is to implement the logic in the ``time_to_target`` function. The function should return the number of months it takes for the rabbit population to reach, or exceed, the target size.

.. Here are some test cases your function should pass:

.. .. code-block:: python

..     # the syntax for running your function looks like
..     # python problems/populations.py -p 2 -s <starting_population> -f <fertility_rate> -t <target_population>
..     # the parameter -p 2 indicates that we want to test part two of the problem

..     # expected output: 1
..     python problems/populations.py -p 2 -s 2 -f 1 -t 3

..     # expected output: 12
..     python problems/populations.py -p 2 -s 10 -f 1 -t 1234

..     # expected output: 12
..     python problems/populations.py -p 2 -s 50 -f 5 -t 100000000


.. Part three: The rabbits are mutating!
.. -------------------------------------

.. Our magical rabbits have quite an amazing property: after there are at least 10 times the initial population on the island, they all suddenly mutate and change their fertility rate! From that point on, each *pair* of rabbits produces the offspring at a rate that's modified by a given mutation factor.

.. Change the ``time_with_mutation`` function in ``problems/populations.py`` to account for this mutation. The function takes the same parameters as ``time_to_target``, with one extra parameter:

.. - ``n_start``: The initial number of rabbits on the island
.. - ``fertility``: The average number of offspring each *pair* of rabbits produce per month
.. - ``target``: The target population size
.. - ``mutation_factor``: The factor by which the fertility rate changes once the population reaches 10 times the initial size

.. .. margin::

..     Hint: The ``floor()`` function from the ``math`` module can be useful for rounding down to the nearest whole number. I've already imported this for you, so you can use it directly in your code!

..     .. code-block:: python

..         x = 1.5
..         y = floor(x)
..         print(y)       # Output: 1

.. Note that the mutation factor can be a decimal (for example, a mutation factor of 1.5 means the fertility rate increases by 50%). Since we can't create a fraction of a rabbit, round down the new fertility rate to the nearest whole number. It could also be less than 1, meaning the rabbits become less fertile after the mutation.

.. .. admonition:: Watch out for zero fertility!

..     With certain mutation factors, it's possible for the fertility rate to drop to zero after mutation (for example, a fertility rate of 1 with a mutation factor of 0.5). In this case, the rabbit population will stop growing entirely once the mutation occurs. Make sure your code can handle this scenario correctly!

..     The number of months is now infinite if the population cannot reach the target size due to zero fertility. In this case, your function should return -1 to indicate that the target population is unreachable.

.. Your task is to implement the logic in the ``time_with_mutation`` function. The function should return the number of months it takes for the rabbit population to reach, or exceed, the target size, accounting for the mutation.

.. Here are some test cases your function should pass:

.. .. code-block:: python

..     # the syntax for running your function looks like
..     # python problems/populations.py -p 3 -s <starting_population> -f <fertility_rate> -t <target_population> -mf <mutation_factor>
..     # the parameter -p 3 indicates that we want to test part three of the problem

..     # expected output: 1
..     python problems/populations.py -p 3 -s 2 -f 1 -t 3 -mf 2

..     # expected output: -1
..     python problems/populations.py -p 3 -s 10 -f 1 -t 1234 -mf 0.1

..     # expected output: 9
..     python problems/populations.py -p 3 -s 50 -f 5 -t 100000000 -mf 2

..     # expected output: 12
..     python problems/populations.py -p 3 -s 50 -f 1 -t 100000000 -mf 20

..     # expected output: 11
..     python problems/populations.py -p 3 -s 50 -f 1 -t 100000000 -mf 20


.. Part four: An island upstate
.. ----------------------------

.. .. figure:: ../../_static/rabbits_ferry.png
..     :align: center
..     :width: 500px
    
..     They're off to an island upstate!

.. The rabbits quickly realise that there's only some much grass and lettuce on the island, and that the population can't grow indefinitely. The island has a maximum capacity, meaning that once the population reaches this size, the fertility rate drops to only 1 offspring per pair of rabbits per month (they're too busy competing for resources to reproduce effectively!). This means that the number of rabbits can exceed the island's capacity, but the growth rate slows down significantly once that point is reached.

.. Given the scarcity of resources, you might imagine that some of the rabbits may die off if the population exceeds the island's carrying capacity. However, fear not, these magical rabbits are resourceful and have devised a clever plan to take a ferry to an island upstate! Each month, a ferry arrives that can take a certain number of rabbits away from the crowded island, reducing the population.

.. In the final function, ``growth_with_capacity``, you'll implement this more complex population model. The function takes the following parameters:

.. - ``n_start``: The initial number of rabbits on the island
.. - ``fertility``: The average number of offspring each *pair* of rabbits produce per month
.. - ``months``: The number of months to simulate
.. - ``mutation_factor``: The factor by which the fertility rate changes once the population reaches 10 times the initial size
.. - ``island_capacity``: The maximum population capacity that the island can easily sustain
.. - ``n_ferry``: The number of rabbits that can fit on the ferry each month

.. Your task is to implement the logic in the ``growth_with_capacity`` function. The rules are now as follows:

.. - Each month, the rabbit population grows according to the fertility rate, which may be affected by mutation and island capacity.
..     - Once the population reaches 10 times the initial size, the fertility rate mutates as described in part three.
..     - If the population exceeds the island capacity, the fertility rate drops to 1 offspring per pair of rabbits per month.
.. - Once the population reaches the island capacity for the first time, the rabbits build the ferry. Each month after and including that month, the ferry arrives and takes away up to ``n_ferry`` rabbits from the population.
.. - The rabbits complete all of their breeding before the ferry arrives each month.
.. - If the population ever reaches zero during the simulation, your function should immediately return 0, as the rabbits have all left the island.

.. Here are some test cases your function should pass:

.. .. code-block:: python

..     # the syntax for running your function looks like
..     # python problems/populations.py -p 4 -s <starting_population> -f <fertility_rate> -m <months> -mf <mutation_factor> -c <island_capacity> -d <n_ferry>
..     # the parameter -p 4 indicates that we want to test part four of the problem

..     # expected output: 13
..     python problems/populations.py -p 4 -s 2 -f 1 -m 5 -mf 2 -c 10 -d 3

..     # expected output: 0
..     python problems/populations.py -p 4 -s 2 -f 1 -m 12 -mf 2 -c 10 -d 300

..     # expected output: 32452
..     python problems/populations.py -p 4 -s 20 -f 1 -m 14 -mf 20 -c 1000 -d 300

..     # expected output: 0
..     python problems/populations.py -p 4 -s 20 -f 1 -m 14 -mf 20 -c 1000 -d 3000


.. Good luck, and may the rabbits multiply in your favour! 🐇🐇🐇