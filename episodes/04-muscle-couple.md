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


## Connecting it all together
With both models defined, we now need to instruct MUSCLE3 on how to connect them together. We do this by creating an object of type ymmsl.Configuration, which contains all the information needed to run the simulation. Remember the diagram we drew in episode 2: 

![Diagram to be added](/fig/ep01-plane-model-coupling.png){alt='alt text for accessibility purposes'}

It shows that there are two components named macro and micro. A conduit connects port state_out on macro to state_in on micro. The symbols at the ends of the conduit show the operators that the ports belong to, O_I for macro.state_out and F_INIT for micro.state_in. Another conduit connects port micro.final_state (O_F) to macro.state_in (S).

Note that there’s a mnemonic here: Operators O_I and S, which are within the state update loop, have a circular symbol, while F_INIT and O_F use a diamond shape. Also, filled symbols designate ports on which messages are sent, while open symbols designate receiving ports. We can therefore see that for each state update, macro will send on state_out, after which micro will do a full run and send its final result as input for the next state update of macro.

Since diagrams aren’t valid Python, we need an alternative way of describing this model in our code. For this, we will create a MUSCLE configuration file written in ymmsl language. This file tells the MUSCLE manager about the existence of each submodel and what kind of messages it should send to and receive from that sub-model.

::: callout
It is often convenient to split your configuration over multiple files. That way, you can easily run the same simulation with different settings for example: just specify a different settings file while keeping the others the same.
:::

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

resources:
  macro:
    threads: 1
  micro:
    threads: 1
```

First, we describe the two components in this model. Components can be submodels, or helper components that convert data, control the simulation, or otherwise implement required non-model functionality. In this simple example, we only have two submodels: one named macro and one named micro. Macro is implemented by an implementation named diffusion, while micro is implemented by an implementation named reaction.

The name of a component is used by MUSCLE as an address for communication between the models. The implementation name is intended for use by a launcher, which would start the corresponding program to create an instance of a component. It is these instances that form the actual running simulation.

```python
conduits = [
        Conduit('macro.state_out', 'micro.initial_state'),
        Conduit('micro.final_state', 'macro.state_in')]

model = Model('reaction_diffusion', components, conduits)
```
Next, we need to connect the components together. This is done by conduits, which have a sender and a receiver. Here, we connect sending port state_out on component macro to receiving port initial_state on component micro. Note that these ports are actually defined in the implementations, and not in this configuration file, and they are referred to here.

The components and the conduits together form a Model, which has a name and those two sets of objects.

```python
settings = Settings({
    'micro.t_max': 2.469136e-6,
    'micro.dt': 2.469136e-8,
    'macro.t_max': 1.234568e-4,
    'macro.dt': 2.469136e-6,
    'x_max': 1.01,
    'dx': 0.01,
    'k': -4.05e4,     # reaction parameter
    'd': 4.05e-2      # diffusion parameter
    })

```

## Launching the simulation

TODO 

## Log output

?