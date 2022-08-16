---
title: "MUSCLE3 - connecting a model to MUSCLE"
teaching: 60
exercises: 2
---

:::::::::::::::::::::::::::::::::::::: questions

- How do you connect an existing python model code to MUSCLE3?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Identify the inputs and outputs of your submodel and link them to ports
- Recognize the Submodel Execution Loop structure in your code
- Learn to connect your own model to the MUSCLE3 library
- Run a single uncoupled model using the MUSCLE3 manager

::::::::::::::::::::::::::::::::::::::::::::::::

## Introduction

MUSCLE3 is the third incarnation of the Multiscale Coupling Library and Environment. Its purpose is to make creating coupled multiscale simulations easy, and to then enable efficient Uncertainty Quantification of such models using advanced semi-intrusive algorithms.

MUSCLE3 uses the Multiscale Modelling and Simulation Language (MMSL) to describe the structure of a multiscale model and you will notice that the terminology in MUSCLE3 closely links to what you have learned in the previous episode about MMSF.

We continue with the reaction-diffusion model example from the previous episode and in this episode we will connect a 1-dimensional implementation of the reaction model to the MUSCLE3 library.

::::::::::::::::::::::::::::::::::::: challenge

## Challenge 1: Can you recognize the Submodel execution loop?
In the previous episode we have discussed the Submodel Execution Loop (SEL). 
Open the file called reaction.py. Can you recognize the various operators (F_INIT, S and O_F) and the state update loop in this submodel? 

```python
def reaction(initial_state):
    """A simple exponential reaction model on a 1D grid.
    """
    t_max = 2.469136e-6
    dt = 2.469136e-8
    k = -4.05e4

    U = initial_state

    t_cur = 0
    while t_cur + dt < t_max:
        U += k * U * dt
        t_cur += dt

    return U
```

:::::::::::::::::::::::: solution

## Solution

```python
def reaction(initial_state):
    """A simple exponential reaction model on a 1D grid.
    """
    # begin F_INIT
    t_max = 2.469136e-6
    dt = 2.469136e-8
    k = -4.05e4

    U = initial_state

    t_cur = 0
    # end F_INIT

    # begin state_update_loop
    while t_cur + dt < t_max:
        # begin S
        U += k * U * dt
        t_cur += dt
        # end S
    # end state_update_loop

    # begin O_F
    return t_cur
    # end O_F
```

:::::::::::::::::::::::::::::::::


## Challenge 2: how do you nest solutions within challenge blocks?

:::::::::::::::::::::::: solution 

You can add a line with at least three colons and a `solution` tag.

:::::::::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::::::::

## Figures

You can use standard markdown for static figures with the following syntax:

`![optional caption that appears below the figure](figure url){alt='alt text for
accessibility purposes'}`

![You belong in The Carpentries!](https://raw.githubusercontent.com/carpentries/logo/master/Badge_Carpentries.svg){alt='Blue Carpentries hex person logo with no text.'}

## Math

One of our episodes contains $\LaTeX$ equations when describing how to create
dynamic reports with {knitr}, so we now use mathjax to describe this:

`$\alpha = \dfrac{1}{(1 - \beta)^2}$` becomes: $\alpha = \dfrac{1}{(1 - \beta)^2}$

Cool, right?

::::::::::::::::::::::::::::::::::::: keypoints 

- Use `.md` files for episodes when you want static content
- Use `.Rmd` files for episodes when you need to generate output
- Run `sandpaper::check_lesson()` to identify any issues with your lesson
- Run `sandpaper::build_lesson()` to preview your lesson locally

::::::::::::::::::::::::::::::::::::::::::::::::

[r-markdown]: https://rmarkdown.rstudio.com/
