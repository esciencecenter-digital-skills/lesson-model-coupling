---
title: "Model coupling theory: the Multiscale Modelling and Simulation Framework"
teaching: 25
exercises: 20
---

:::::::::::::::::::::::::::::::::::::: questions

- When coupling models together, how do you figure out which information needs
  to be exchanged when?
- How does that depend on the spatial and temporal scales of the simulated
  processes?
- What does that mean for how submodels should be implemented?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Explain how to couple models using the concepts of the Multiscale Modelling
  and Simulation Framework

::::::::::::::::::::::::::::::::::::::::::::::::

## Introduction

Coupling models can be a difficult task, especially when there are many models
involved that model processes in different ways and at different scales in time
and space. To make a coupled simulation, you need to figure out which
information needs to be passed between which submodels, when it needs to be sent
and received, and how it can be represented, and that can be quite a puzzle.
Fortunately, there is a theory of model coupling that can help you do this. It
is called the Multiscale Modelling and Simulation Framework (MMSF), and despite
its name, it also includes same-scale couplings.

In this episode, we'll work through a slightly extended version of the MMSF's
process for coupling two models representing two processes.


## Domains

Mathematical and simulation models represent some kind of process, which takes
place in a certain location in time and in space: its domain. The weather takes
place in the atmosphere, earthquakes in the Earth's crust, a forest fire in a
forest. In time, that forest fire begins with a lightning strike and ends when
the flames are extinguished, and even continuous processes like the airflow
around an aeroplane wing can be considered to start when circumstances change
and end when a steady state is reached again.

The domains of two models can be the *same*, *overlapping*, *adjacent*, or
*separated*, in both space and time. This is important for the coupling between
them, because it decides what is sent (state or boundary conditions) and when it
is sent.

::::::::::::::::::::::::::::::::::::: challenge

## Challenge 1: Models and domains

Think of two models that could potentially be coupled, and describe each model's
domain in time and space and the relation between them.

Some things to ponder:

- What does it mean for two models to have adjacent time domains?
- What if their spatial domains are separated?

:::::::::::::::::::::::: solution

## Example solution

### Example coupled model

The sun drives local convection in the atmosphere by heating up the Earth's
surface, which then heats up the air above it. We can model how this plays out
over the course of a day by coupling two models:

Model 1 simulates the heating of the Earth's surface as the sun shines on it.
Model 2 simulates the flow of the air above as it warms up and starts rising.
In time, both domains extend from sunrise to sunset. In space, the heating
process takes place on the Earth's surface, while the airflow process operates
on the atmosphere. In time, the domains overlap, while in space they are
adjacent.

### Questions

- If two models have adjacent time domains, then one model starts at the same
  moment that the other ends. Typically, this occurs when one process triggers
  another.
- If the spatial domains of two models are separated, then there is no direct
  exchange of information between the models, unless some kind of remote
  communication is possible. As a result, the models can be run separately and
  don't need to be coupled, unless some other model has a domain adjacent to
  both.

:::::::::::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::::::::::


## Scales

A second important property of a physical process is the scales, again in time
and in space, on which it takes place. A scale can be defined by its grain and
extent. There are many other terms in use for these, but we'll use these here
because they're less ambiguous than most. The *grain* refers to the smallest
detail that the model can represent. In practice, that is usually set by the
timestep (in time), grid spacing, or size of an agent (in space). If these can
vary throughout the domain, pick the smallest. The *extent* refers to the size
of the process in space and time, so the size of its domain. How long does it
take to complete (or to reach a steady state), and how large an area is
modelled?

::::::::::::::::::::::::::::::::::::: challenge

## Challenge 2: Models and scales

What are the scales of the models you previously considered the domains of? What
are their grain and extent in space and in time?

:::::::::::::::::::::::: solution

## Example solution

Model 1 simulates the heating of the Earth's surface as the sun shines on it.

The temperature of the Earth's surface only changes slowly during the day, and
we can probably say there are no significant changes from one minute to the
next, or even for a somewhat larger interval. So the time grain of model 1 is on
the order of a few minutes, perhaps up to an hour. The time extent of the model
is one day, as it will repeat itself after that.

In space, the grain depends on the research question, and could be as small as
10cm if we are looking at the detailed thermal environment around a building, or
as large as a few kilometers if we want to make a national weather forecast. The
extent is the size of the area of study.

Model 2 simulates the flow of the air above as it warms up and starts rising.
This is probably done using a computational fluid dynamics model. Both the
temporal and spatial scales will depend on the research question here, and
grains (time steps and grid spacing) may range from milliseconds and centimeters
to minutes and kilometers. The spatial extent may be the same as that of Model
1, but it could be larger if a very tall column of air is modeled. In time, the
atmosphere won't reach a static equilibrium, but we could choose to run the
simulation for the course of a day and use that as the temporal extent.

Note that you often cannot give an exact number, and that the scales are often
something of a modeling decision. That's usually alright, as we will see below.

:::::::::::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::::::::::

Just like with domains, the scales of two models can be compared and their
relation determined. The Scale Separation Map (SSM) is a nice tool for this. The
SSM is a graph with on its horizontal axis a range of durations, and on its
vertical axis a range of sizes. Each model can then be plotted as a box, with
the left edge at the temporal grain, the right edge at the temporal extent, the
lower edge at the spatial grain, and the upper edge at the spatial extent. Here
is an example:

SSM EXAMPLE

The SSM may look very counterintuitive at first, because we are used to plotting
locations, not sizes. So look at the graph carefully and think about what you
see and what it means. It does get easier to understand once you get the hang of
it.

As you can see, we can plot multiple models on a Scale Separation Map and when
we do, the map shows the relationship between the scales of two models. Both
horizontally and vertically, model rectangles can have a gap between them (i.e.
be separated), or be adjacent, or overlap, and the corresponding models are said
to be scale separated, scale adjacent or scale overlapping in space and/or in
time.

For coupling, it is actually only these relationships that matter. Even if you
don't know the exact grain or extent of a particular model, you can often decide
whether it's smaller, larger or the same as the grain or extent of another model
and draw them correspondingly.

::::::::::::::::::::::::::::::::::::: challenge

## Challenge 3: Scale Separation Map

Draw a scale separation map for the models you would like to couple.

:::::::::::::::::::::::: solution

## Example solution

SSM with Surface Heating model with time 10 min -> 1 day, space 1m -> 100m and
Atmosphere 1s -> 1 day, space 10 cm -> 100m

:::::::::::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::::::::::


## Models

So far, we have talked about domains and scales of models, which we can do based
on the physical properties of the modelled system, and the research questions we
ask about that system. In order to be able to technically couple models however,
we need to know what a model is. In the MMSF, this is done using a universal
model-of-a-model called the Submodel Execution Loop (SEL):

SEL diagram

According to the MMSF, each model starts by initialising itself, a stage (or
*operator*) known as `F_INIT`. This puts the model into its initial state.
During `F_INIT`, information may be received from other models in a coupled
simulation, which the model can use to initialise itself.

Second, some output based on that state is produced in the `O_I` operator. This
is Intermediate Output, or, looking from the outside in, we Observe an
Intermediate state, hence `O_I`. This output may be sent to other models, where
it can for example be used as boundary conditions.

Third, a state update may be performed using the `S` operator, which moves the
model to its next state (timestep). During `S`, information may be received from
other models to help perform the state update.

After `S`, the model may loop back to before `O_I`, and repeat those two
operators for a while, until the end of the time scale is reached. This leaves
the model with a final state, which may be output in the `O_F` operator (for
Final output or observation).

This basic model is quite flexible. If the loop is run zero times, then the
model is a simple function. Timesteps may be of any length, and vary during the
run, and the model may decide to stop and exit the state update loop at any
time. The state may represent anything at all in any way, and it may be updated
in whichever way is suitable for the model. Any simulation code you may want to
use is very likely to fit these minimal constraints.


## Coupling templates

Now that we know what a model is and how models may be related in terms of their
domains and scales, we can decide how to set up the coupled simulation. We do
this by looking at all pairs of two models under consideration, one pair at a
time, and consider the relationships between their temporal and spatial scales
as well as their domains.

Of the different properties, those governing time are the most interesting, and
also potentially the most confusing. Let's look at the possible scenarios one by
one.

### Adjacent or separated time domains

A simple case is when the time domains are adjacent, meaning one process starts
right when the other process finishes, or separated, meaning one process starts
some time after the other process finishes. In this case, the final output of
the first model is used to initialise the subsequent model.

### Overlapping time domains and the same temporal scale

If two processes do not happen one after the other, then they occur at least
partially simultaneously, and their models have overlapping time domains. The
simplest among these cases is when the two processes start and end at the same
time, and have the same timestep. In that case, each model updates its state
to the next timestep, then sends some information based on the new state (e.g.
boundary conditions) to the other model, receives information from the other
model in return, and goes to do the next state update.

### Overlapping time domains and temporal scale separation

A third interesting case is when two processes happen at the same time, but one
process is much faster than the other, so that it runs to completion in (much)
less time than it takes the other to do a timestep. In that case, the fast
model needs to do an entire run for every timestep of the slow model.


::::::::::::::::::::::::::::::::::::: challenge

## Challenge 4: Coupling with the Submodel Execution Loop

We can represent each of the two models in the scenarios above as a Submodel
Execution Loop. To connect the models, we then have to send information between
the operators of the models. For each of the three cases, figure out how to
connect the Submodel Execution Loops of the two models so that the correct
communication pattern is implemented.

:::::::::::::::::::::::: solution

## Example solution

If the time domains are adjacent or separated, then the final output of the
first model is used to initialise the subsequent model. We can implement this
by sending information from the first model's `O_F` to the second model's
'F_INIT'.

If the temporal scales are the same, then the models exchange information every
time they have a new state. This can be done by connecting each model's `O_I`
to the other model's `S`, thus sending information at each step.

In case of temporal scale separation, the fast model needs to be reinitialised
at every timestep of the slow model, do an entire run, and return some
information based on its final state to the slow model. This can be
accomplished by sending from the slow model's `O_I` to the fast model's
`F_INIT` and from the fast model's `O_F` back to the slow model's `S`.

:::::::::::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::::::::::


These three cases demonstrate the three *Coupling Templates* defined by the
MMSF. The first one, `O_F` to `F_INIT`, is called *dispatch*. The second one,
`O_I` to `S` is called *interact*. The third one has two parts, `O_I` to
`F_INIT` (*call*) and `O_F` to `S` (*release*).

Given the constraints of which operators can send and which can receive, these
are in fact all four possible types of connections.



TODO






- Coupling templates
    - Spatial scale separation
        - Overlap -> one-on-one
        - Separation and adjacency -> one-to-many

What is sent in those messages depends on the models, but in general if they
share a domain this will be (part of) the domain's state, while if they occupy
adjacent domains then boundary conditions will be exchanged.

- Data integration(?)

- MMSL
    - Components
    - Operators
    - Conduits


This is a lesson created via The Carpentries Workbench. It is written in
[Pandoc-flavored Markdown](https://pandoc.org/MANUAL.txt) for static files and
[R Markdown][r-markdown] for dynamic files that can render code into output.
Please refer to the [Introduction to The Carpentries 
Workbench](https://carpentries.github.io/sandpaper-docs/) for full documentation.

What you need to know is that there are three sections required for a valid
Carpentries lesson:

 1. `questions` are displayed at the beginning of the episode to prime the
    learner for the content.
 2. `objectives` are the learning objectives for an episode displayed with
    the questions.
 3. `keypoints` are displayed at the end of the episode to reinforce the
    objectives.

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: instructor

Inline instructor notes can help inform instructors of timing challenges
associated with the lessons. They appear in the "Instructor View"

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: challenge 

## Challenge 1: Can you do it?

What is the output of this command?

```r
paste("This", "new", "lesson", "looks", "good")
```

:::::::::::::::::::::::: solution 

## Output
 
```output
[1] "This new lesson looks good"
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

- Physical processes take place on a domain and at certain scales in time and
  space
- Simulation models are described by the Submodel Execution Loop
- Given two models and their domains and scales, we can decide which coupling
  template to use to connect them
- An MMSL diagram can be used to visualise a complete coupled simulation

- Use `.md` files for episodes when you want static content
- Use `.Rmd` files for episodes when you need to generate output
- Run `sandpaper::check_lesson()` to identify any issues with your lesson
- Run `sandpaper::build_lesson()` to preview your lesson locally

:::::::::::::::::::::::::::::::::::::::::::::::

[r-markdown]: https://rmarkdown.rstudio.com/
