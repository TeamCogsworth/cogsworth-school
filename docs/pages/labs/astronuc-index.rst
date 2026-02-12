.. _astronuc:

AstroNuc 2026
=============

Slides
------

The page below shows the slides that I'll use while teaching this lab. Once you click on the slides you can navigate through them using the arrow keys on your keyboard.
I'd recommend opening the slides in a separate tab or window so that you can refer to them while working through the lab.

.. raw:: html

    <iframe src="../../_static/presentations/astronuc/main.html" width="100%" height="500px"></iframe>

.. button-link:: ../../_static/presentations/astronuc/main.html
    :color: primary
    :shadow:
    :align: center

    View full-screen presentation

.. raw:: html

    <hr style="margin: 4rem 0;">

Overview
--------

Welcome to this lab everyone, I hope you've had an excellent week at AstroNuc 2026! My goal with this lab is to show you how to use ``cogsworth`` to track the timing and location of supernovae in galaxies. As you likely know even better than me, the location and timing of these events is crucial for galactic chemical evolution.

We're going to incrementally develop a suite of simulations that uses ``cogsworth`` to track these events and see how they are sensitive to different aspects of binary evolution and galactic dynamics.

Learning Goals
--------------

By the end of this lab, my aim is that you will:

- **Understand**
    - how population synthesis simulations create large evolved populations of stars and binaries
    - how ``cogsworth`` connects population synthesis to galactic dynamics self-consistently
- **Be able to**
    - create your own simulations using ``cogsworth``
    - track the timing and location of supernovae in galaxies
- **Have ideas**
    - about the general capabilities of the code
    - for how to use ``cogsworth`` in your own research!

.. raw:: html

    <hr style="margin: 4rem 0;">


.. toctree::
    :maxdepth: 4
    :caption: Lab Outline

    astronuc/part-1
    astronuc/part-2
    astronuc/part-3
    astronuc/part-4
