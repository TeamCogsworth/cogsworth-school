Part 3: Inspect supernovae
--------------------------

Now that we can simulate Populations of binaries and identify specific subpopulations, it's time to track down those supernovae! I'll start with a demo of how to do this for common-envelope events and then you'll get a chance to do the same for supernovae.

Demo
****

Create a population with lots of massive stars
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

First things first, let's make a slightly different population, which preferentially samples higher mass binaries. This will give us more common-envelopes and supernovae to work with.

.. margin::

    Note that this population still stores the total mass in binaries and singles stars required to create this population (in the :attr:`~cogsworth.pop.Population.mass_binaries` and :attr:`~cogsworth.pop.Population.mass_singles` attributes). So you can renormalise without worrying that you've preferentially sampled from the IMF.

.. code-block:: python

    import cogsworth

    p = cogsworth.pop.Population(
        n_binaries=2000,
        use_default_BSE_settings=True,
        final_kstar1=[13, 14],          # aim to sample systems that produce a NS/BH
        final_kstar2=[13, 14],          # same for secondary star
    )
    p.create_population()

Find the common-envelope events
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Our goal here is to find the times at which common-envelope events occur in our population. The table of interest in this case is the ``bpp`` table, which tracks the properties of each binary at every "important" time step in the simulation.

.. tip::

    The :ref:`output documentation <output>` has a detailed description of (a) what different ``evol_type`` and ``kstar`` values mean and (b) definitions of every column in the ``bpp`` table. I recommend keeping this documentation open as you work through this part of the lab.

Common-envelope events are indicated by an ``evol_type`` value of 7. Any row with this value corresponds to the start of a common-envelope event. Let's find these rows!

.. code-block:: python

    # find the times at which a common-envelope event starts
    ce_mask = p.bpp["evol_type"] == 7

    # mask the rows in the Pandas DataFrame
    ce_rows = p.bpp[ce_mask]
    print(ce_rows)

We can now take a look at the distribution of times at which these events occur.

.. code-block:: python

    fig, ax = plt.subplots()
    ax.hist(ce_rows["tphys"], bins="auto")
    ax.set(
        xlabel="Time in frame of binary [Myr]",
        ylabel="Number of common-envelope events",
    )
    plt.show()

.. figure:: ../../../_static/astronuc/ce_times_binary.png
    :align: center
    :width: 80%
    :alt: Histogram of common-envelope event times in the frame of the binary

    Distribution of common-envelope event times in the frame of the binary.

It's important to note here that these times are in the frame of the binary, so they don't correspond to any particular time in the galaxy. We'll see how to convert these to galactic times next.

.. admonition:: Question for you
    :class: admonition-question

    What drives the timing of these common-envelope events?
    
    What would happen if you made a scatter plot of these times against the initial primary mass of the binary? Or the initial orbital period?

    .. dropdown:: Click here to reveal the answer
        :color: danger

        A common-envelope event occurs when a star overflows its Roche lobe in an unstable manner. So if we simplify a little, the timing is mainly driven by:
        
        (a) when the star evolves off the main sequence and expands 
        (b) how far apart the stars are
        (c) how large the Roche lobe is (which depends on the mass ratio).
        
        It's a little more complicated in practice, since the typically stability of mass transfer is different depending on the evolutionary stage of the star when it overflows its Roche lobe (case A, B, or C).

        But in general, we would expect common-envelope events to occur sooner for higher mass stars since those will expand sooner. We would also expect common-envelope events to be more common and to occur faster for shorter initial orbital periods.

    

Compute the timing on Galactic timescales
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now let's try converting these times to the galactic frame. Each binary was born at a specific time in the galaxy, which is given by the :attr:`~cogsworth.sfh.StarFormationHistory.tau` attribute of the :attr:`~cogsworth.pop.Population.initial_galaxy` object. Remember that this is a "lookback time", so the binary was born :math:`\tau` Myr before the present day. So to convert the common-envelope event times to the galactic frame, we can do the following:

.. math::

    t_{\rm gal} = t_{\rm present} - \tau + t_{\rm ce}

where :math:`t_{\rm ce}` is the time of the common-envelope event in the binary frame and :math:`t_{\rm present}` is the present day time in the galaxy (which is 12 Gyr by default, but is stored in the :attr:`~cogsworth.pop.Population.max_ev_time` attribute).

Let's try computing the times of the common-envelope events in the galactic frame!

.. code-block:: python

    # get the bin_nums of the common-envelope events
    ce_bin_nums = ce_rows["bin_num"]

    # get the indices of these bin_nums in the p.bin_nums array
    ce_indices = np.searchsorted(p.bin_nums, ce_bin_nums)

    # use these indices to get tau
    ce_tau = p.initial_galaxy.tau[ce_indices]

    # compute the galactic times
    ce_t_gal = p.max_ev_time - ce_tau + ce_rows["tphys"].values * u.Myr

Let's take a look at the distribution of these galactic times!

.. code-block:: python

    fig, ax = plt.subplots()
    ax.hist(ce_t_gal.to(u.Gyr).value, bins="auto")
    ax.set(
        xlabel="Age of Milky Way [Gyr]",
        ylabel="Number of common-envelope events",
    )
    plt.show()

.. figure:: ../../../_static/astronuc/ce_times_galaxy.png
    :align: center
    :width: 80%
    :alt: Histogram of common-envelope event times in the frame of the galaxy

    Distribution of common-envelope event times in the frame of the galaxy.

.. admonition:: Question for you
    :class: admonition-question

    What drives the distribution of timing of these common-envelope events on Galactic timescale?
    
    .. dropdown:: Click here to reveal the answer
        :color: danger

        The timing in the frame of the binary is relatively short on the scale of the galaxy (most occur within 100 Myr, see earlier plot). So the main driver of the distribution on galactic timescales is the star formation history of the galaxy. In this case, we have a Milky Way-like SFH, which means that most stars (and therefore most common-envelope events) occur early on in the galaxy's history, which is why we see a peak at early times in the histogram.

Locate the common-envelope events in the galaxy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As we've seen before, each binary has an ``orbit`` associated with it, which tracks its trajectory through the galaxy. Let's take a look at one of these objects to get a sense of what a ``gala`` :class:`~gala.dynamics.Orbit` object looks like.

.. code-block:: python

    # let's take the first orbit
    orbit_example = p.orbits[0]
    print(orbit_example)

    # it stores the time and position at each timestep
    print(orbit_example.t)
    print(orbit_example.pos)

Did you notice that the orbit times end at 12 Gyr? The initial time of the orbit is actually the birth time of the binary in the galaxy, these orbit times are already based in the Galactic frame.

So we need to:

- Go through each of the common-envelope events
- Find the corresponding orbit
- Compute the last timestep just before the common-envelope
- Get the position of the binary at this time

Let's do it!

.. code-block:: python

    ce_positions = np.zeros((len(ce_rows), 3)) * u.kpc

    # go through each of the common-envelope events
    for i in range(len(ce_indices)):
        # find the corresponding orbit
        ce_orbit = p.orbits[ce_indices[i]]

        # compute the last timestep where orbit.t is less than ce_t_gal[i]
        closest_time_index = np.where(ce_orbit.t < ce_t_gal[i])[0][-1]

        # get the position of the binary at this time
        ce_positions[i] = ce_orbit.pos.xyz[:, closest_time_index]

And now we can plot the positions of these common-envelope events in the galaxy!

.. code-block:: python

    fig, axes = plt.subplots(2, 1, figsize=(8, 9), gridspec_kw={"height_ratios": [1, 4]})

    XMAX = 20
    ZMAX = 5

    axes[0].scatter(
        ce_positions[:, 0], ce_positions[:, 2],
        c=ce_t_gal.to(u.Gyr).value, s=5,
        cmap="magma", vmin=0, vmax=12
    )
    axes[0].set(
        ylabel="$z$ [kpc]",
        xlim=(-XMAX, XMAX),
        ylim=(-ZMAX, ZMAX),
        aspect="equal",
    )

    axes[1].scatter(
        ce_positions[:, 0], ce_positions[:, 1],
        c=ce_t_gal.to(u.Gyr).value, s=5,
        cmap="magma", vmin=0, vmax=12
    )
    axes[1].set(
        xlabel="Galactocentric $x$ [kpc]",
        ylabel="Galactocentric $y$ [kpc]",
        xlim=(-XMAX, XMAX),
        ylim=(-XMAX, XMAX),
        aspect="equal",
    )

    fig.colorbar(axes[0].collections[0], ax=axes, label="Age of Milky Way at CE [Gyr]")

    plt.show()

.. figure:: ../../../_static/astronuc/ce_positions.png
    :align: center
    :width: 80%
    :alt: Positions of common-envelope events in the galaxy

    Positions of common-envelope events in the galaxy. The colour indicates the age of the Milky Way at which the common-envelope event occurs.

.. raw:: html

    <hr style="margin: 4rem 0;">

Tasks
*****

Now it's your turn to do the same for supernovae! The code from the demo above should be helpful for this


