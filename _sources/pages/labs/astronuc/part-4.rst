Part 4: Varying our assumptions
-------------------------------

In this final part, we are going to do what *any* good user of population synthesis codes does --- vary our assumptions and see how it changes our results!

.. tip::

    For a full list of the initial conditions and binary physics variations you could use, check out `this page of the COSMIC docs <https://cosmic-popsynth.github.io/COSMIC/pages/inifile.html>`_. Specifically, the sampling parameters are `found here <https://cosmic-popsynth.github.io/COSMIC/pages/inifile.html#sampling>`_ and the binary physics parameters are `here <https://cosmic-popsynth.github.io/COSMIC/pages/inifile.html#binary-physics>`_.

Demo
****

Let's start by quickly creating a template population to use for our variations. At first, let's just sample the binaries but not do any evolution yet. This will make it easy to use the same initial population for all of our variations, so that we can isolate the impact of changing our assumptions about the physics.

.. code-block:: python

    import cogsworth

    template = cogsworth.pop.Population(
        n_binaries=10_000,
        use_default_BSE_settings=True,
        final_kstar1=[13, 14],
        final_kstar2=[13, 14],
    )
    template.sample_initial_binaries()

We can then copy this template and use it to run a fiducial population.

.. code-block:: python

    fiducial = template.copy()
    fiducial.perform_stellar_evolution()
    fiducial.perform_galactic_evolution()

.. note::

    Notice that I didn't do ``fiducial.create_population()`` here. This is because I want to have the same initial population for all of my variations, so I just copied the template and then ran the evolution steps separately.

Now let's consider some different assumptions that we could vary.

Initial population distributions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. margin::

    IMF = Initial Mass Function

``cogsworth`` makes some default assumptions about the initial population distributions. For example, it assumes you want to use an IMF following Kroupa 2001 and the initial orbital period distribution from Sana+2012. You can change these assumptions by changing the parameters in ``sampling_params`` in the ``Population`` constructor.

Let's make a copy of our population and change the orbital period distribution to a custom power law distribution.

.. code-block:: python

    # copy the old population
    diff_porb = template.copy()

    # update sampling parameters and re-run
    diff_porb.sampling_params["porb_model"] = {'min': 0.15, 'max': 5.5, 'slope': 0.5}
    diff_porb.create_population()

Now we can compare the initial orbital period distributions of these two populations.

.. code-block:: python

    fig, ax = plt.subplots()

    bins = np.logspace(0.15, 5.5, 30)
    ax.hist(fiducial.initial_binaries["porb"], bins=bins, label="Sana+2012")
    ax.hist(diff_porb.initial_binaries["porb"], bins=bins, label="Custom power law", alpha=0.7)
    ax.set(
        xscale="log",
        xlabel="Initial orbital period [days]",
        ylabel="Number of binaries",
    )
    ax.legend()
    plt.show()

.. figure:: ../../../_static/astronuc/vary_init_porb.png
   :align: center
   :alt: Initial orbital period distribution comparison

   The initial orbital period distribution for the two populations.

One can imagine that this change in the initial orbital period distribution could have a significant impact on the properties of the binary population at later times. Let's see how it changes the number of mergers that occur in our population.

.. admonition:: Question for you
    :class: admonition-question

    Before looking at the results, can you predict how the rate of mergers will change when we switch from the Sana+2012 distribution to our custom power law distribution?

.. code-block:: python

    for pop, label in [(fiducial, "Sana+2012"), (diff_porb, "Custom power law")]:
        n_mergers = (pop.final_bpp["sep"] == 0.0).sum()
        print(f"Number of mergers with {label} porb distribution:", n_mergers)

Binary physics settings
^^^^^^^^^^^^^^^^^^^^^^^

There's also a lot of uncertainty in the physics of binary interactions. It's therefore important that we vary our assumptions about these interactions to see how they impact our results. For example, we could change the common envelope efficiency parameter, or vary the strength of supernova natal kicks.

Let's make a copy of our template population, but alter the strength of supernova natal kicks.

.. code-block:: python

    weak_kick = template.copy()
    weak_kick.BSE_settings["sigma"] = 20  # km/s
    weak_kick.perform_stellar_evolution()
    weak_kick.perform_galactic_evolution()

By decreasing the strength of supernova natal kicks, it's much less likely that binaries will be disrupted by supernovae. Let's check that we're getting fewer disruptions in this population compared to our fiducial population.

.. code-block:: python

    for pop, label in [(fiducial, "Fiducial"), (weak_kick, "Weak kicks")]:
        n_disrupted = pop.disrupted.sum()
        print(f"Number of disrupted binaries with {label}:", n_disrupted)

.. admonition:: Bonus task
    :class: admonition-task

    Try finding a binary that disrupts in the fiducial population but not in the weak kick population. Plot the orbit of this binary in both populations and see how the different kick strengths lead to different outcomes.

    .. dropdown:: Click here to reveal the answer
        :color: danger

        .. code-block:: python

            fid_dis_nums = fiducial.bin_nums[fiducial.disrupted]
            weak_dis_nums = weak_kick.bin_nums[weak_kick.disrupted]

            # find one that is disrupted in fiducial but not in weak_kick
            example = weak_kick.bin_nums[
                np.isin(weak_kick.bin_nums, fid_dis_nums)
                & ~np.isin(weak_kick.bin_nums, weak_dis_nums)
            ][0]

            # plot both orbits together to see the difference
            fig, axes = fiducial.plot_orbit(example, show=False)
            weak_kick.plot_orbit(example, fig=fig, axes=axes, show_legend=False)

            # perhaps try changing t_max to look at earlier times?

        .. figure:: ../../../_static/astronuc/vary_kick_orbits.png
           :align: center
           :alt: Orbit comparison for different kick strengths

           The orbit of a binary that disrupts in the fiducial population but not in the weak kick population.

Galactic potential
^^^^^^^^^^^^^^^^^^

Finally, we could also vary the potential of the galaxy that we are integrating through. In this case, we don't need to repeat the stellar evolution step, since the galactic potential doesn't impact the binary interactions (or at least, we are assuming that).

Let's create a new potential that's an NFW profile with :math:`M_{\rm halo} = 10^{12} M_\odot`.

.. code-block:: python

    import gala.potential as gp

    nfw = gp.NFWPotential(mhalo=1e12 * u.Msun, r_s=15.63 * u.kpc)

    nfw_pop = fiducial.copy()
    nfw_pop.galactic_potential = nfw
    nfw_pop.perform_galactic_evolution()

Now let's compare the orbit of a random binary that disrupts.

.. code-block:: python

    disrupted_num = fiducial.bin_nums[fiducial.disrupted][0]
    for pop in [fiducial, nfw_pop]:
        pop.plot_orbit(disrupted_num, t_max=2000 * u.Myr)

.. figure:: ../../../_static/astronuc/vary_gal_pot_orbits_fid.png
   :align: center
   :alt: Orbit comparison for different galactic potentials

   The orbit of a binary that disrupts in the fiducial population, evolved through the fiducial potential.

.. figure:: ../../../_static/astronuc/vary_gal_pot_orbits_nfw.png
   :align: center
   :alt: Orbit comparison for different galactic potentials

   The same binary as the previous figure, but evolved through the NFW potential we created.

.. raw:: html

    <hr style="margin: 4rem 0;">

Tasks
*****

You'll not have time to do all of these tasks in the lab, so just pick whichever one looks more interesting to you (and no one's stopping you doing the others later!).




