Preparing for the labs
======================

Hi there! Before starting the labs, please follow these instructions to set up your coding environment so you're ready to go on the day!

Install ``cogsworth``
---------------------

You can follow the instructions in the ``cogsworth`` documentation to install the code on your machine. If you have any issues, please don't hesitate to ask for help!

.. button-link:: https://cogsworth.readthedocs.io/en/latest/pages/install.html
    :color: primary
    :shadow:
    :align: center

    Go to installation instructions

Test your installation
----------------------

Once you've installed ``cogsworth``, you can test that everything is working by running the following code in a Python environment

.. code-block:: python

    import cogsworth

    print(cogsworth.__version__)

And you should see something like "v3.6.2" (or something more up-to-date).

If this works then you'll all set up. You can fully test your installation by running through the quickstart guide in the documentation, which will show you how to create a population and evolve it. This should give you a good preview for the sorts of things we'll be doing in the labs.

.. button-link:: https://cogsworth.readthedocs.io/en/latest/pages/getting_started.html
    :color: primary
    :shadow:
    :align: center

    Go to quickstart guide

Download the lab materials
--------------------------

You can clone the whole repository of lab materials to get everything locally by running

.. code-block:: bash

    git clone https://github.com/TeamCogsworth/cogsworth-school.git
