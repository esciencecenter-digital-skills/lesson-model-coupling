---
title: "MUSCLE3 - coupling and running"
teaching: 60
exercises: 2
---

::: questions

- How do you couple multiple sub-models using MUSCLE3?
- How do you run a coupled simulation with MUSCLE3?

:::

::: objectives

- Demonstrate how MUSCLE3 implements the Multiscale Modelling and Simulation Language (MMSL)
- Configure a coupled simulation with MUSCLE3
- Run a coupled simulation using MUSCLE3

:::

## Introduction

We managed to connect one of our sub-models, the reaction model, to MUSCLE. In order to make a coupled simulation, we need at least two models. The second model here is the diffusion model. We prepared it for you, adding the necessary MUSCLE bindings and comments similar to what we did for the reaction model. Open it from 

## Investigating the macro model


## Connecting the models together

With both models defined, we now need to instruct MUSCLE3 on how to connect them together. To find out how to connect the models, we first need to apply the MMSF to this particular simulation. The reaction and diffusion processes act simultaneously on the same spatial and temporal domain. The discretisation of that domain in space is also the same for the two models, so that they have the same spatial scale. As mentioned before, we're going to configure the models to have temporal scale separation, with the diffusion model the slow macromodel and the reaction model the fast micromodel.

According to the MMSF, this means we have to use the Call-and-Release coupling template, with one instance of each submodel:

![gMMSL diagram for the reaction-diffusion model](fig/ep04-reaction-diffusion-coupling.png){alt='gMMSL diagram for the reaction-diffusion model. Two boxes labeled macro and micro represent the two submodels. A line connects a filled circle labeled state_out on macro to an open diamond labeled state_in on micro. A second line connects a filled diamond labeled final_state on micro to an open circle labeled state_in on macro.'}

This diagram shows that there are two components named macro and micro. A conduit connects port state_out on macro to state_in on micro. The symbols at the ends of the conduit show the operators that the ports belong to, O_I for macro.state_out and F_INIT for micro.state_in. Another conduit connects port micro.final_state (O_F) to macro.state_in (S).

Since diagrams aren’t valid Python, we need an alternative way of describing this model in our code. For this, we will create a MUSCLE configuration file written in the yMMSL language. This file tells the MUSCLE manager about the existence of each submodel and how it should be connected to the other components.

::: challenge

Complete this yMMSL file for the reaction-diffusion model:

```yaml
ymmsl_version: v0.1

model:
  name: reaction_diffusion_python

  components:
    macro:
      implementation: diffusion_python
      ports:
        o_i: state_out
        ...

    ...
      implementation: reaction_python
      ...

  conduits:
    macro.state_out: micro.initial_state
    ...
```


::: solution

```yaml
ymmsl_version: v0.1

model:
  name: reaction_diffusion_python

  components:
    macro:
      implementation: diffusion_python
      ports:
        o_i: state_out
        s: state_in

    micro:
      implementation: reaction_python
      ports:
        f_init: initial_state
        o_f: final_state

  conduits:
    macro.state_out: micro.initial_state
    micro.final_state: macro.state_in
```

:::
:::

First, we describe the two components in this model. Components can be submodels, or helper components that convert data, control the simulation, or otherwise implement required non-model functionality. The name of a component is used by MUSCLE as an address for communication between the models. The implementation name is intended for use by a launcher, which would start the corresponding program to create an instance of a component. It is these instances that form the actual running simulation. In this example, we have two submodels: one named macro and one named micro. Macro is implemented by an implementation named diffusion_python, while micro is implemented by an implementation named reaction_python.

Second, we need to connect the components together. This is done by conduits, which have a sender and a receiver. Here, we connect sending port state_out on component macro to receiving port initial_state on component micro.

## Adding settings

The above specifies which submodels we have and how they are connected together. Next, we need to configure them by adding the settings to the yMMSL file. These will be passed to the models, who get them using the `Instance.get_settings()` function:

```yaml
settings:
  micro.t_max: 2.469136e-6
  micro.dt: 2.469136e-8
  macro.t_max: 1.234568e-4
  macro.dt: 2.469136e-6
  x_max: 1.01
  dx: 0.01
  k: -4.05e4    # reaction parameter
  d: 4.05e-2    # diffusion parameter
```

## Specifying resources

Finally, we need to tell MUSCLE3 whether and if so how each model is parallelised, so that it can reserve adequate resources for each component. In this case, the models are single-threadedso that is what we specify:

```yaml
resources:
  macro:
    threads: 1
  micro:
    threads: 1
```

Note that we specify resources for each component, not for each implementation.

## Launching the simulation

This gives us all the pieces needed to construct a coupled simulation.

TODO: make new Python file, import reaction and diffusion functions, put all the above YAML into a string, ymmsl.load() it (this is different from the tutorial, but I think it's nicer actually), and call libmuscle.run_simulation()




## Log output



## Bonus exercise

TODO: do this or not?

- turn reaction.py and diffusion.py into stand-alone Python programs
- put the yMMSL into a separate YAML file
- add implementations: section pointing to those files
- run using muscle_manager --start-all


?
