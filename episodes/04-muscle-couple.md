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



Next we will create a MUSCLE configuration file. This file tells the MUSCLE manager about the existence of each submodel and what kind of messages it should send to and receive from that sub-model.
