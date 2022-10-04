---
title: "MUSCLE3 - connecting a model to MUSCLE"
teaching: 30
exercises: 30
---

::: questions

- How do you connect an existing python model code to MUSCLE3?

:::

::: objectives

- Identify the inputs and outputs of your submodel and link them to ports
- Recognize the Submodel Execution Loop structure in your code
- Learn to connect your own model to the MUSCLE3 library

:::

## Introduction

MUSCLE3 is the third incarnation of the Multiscale Coupling Library and Environment. Its purpose is to make creating coupled multiscale simulations easy, and to then enable efficient Uncertainty Quantification of such models using advanced semi-intrusive algorithms.

MUSCLE3 uses the Multiscale Modelling and Simulation Language (MMSL) to describe the structure of a multiscale model and you will notice that the terminology in MUSCLE3 closely links to what you have learned in the previous episode about MMSF.

MUSCLE3 consist of three components:

**libmuscle** is a library that is used to connect component intances (e.g new or existing submodels) to a coupled simulation.

**muscle_manager** is the central manager of MUSCLE3 that starts up submodels and coordinates their interaction.

**ymmsl-python** is a Python library that contains class definitions to represent an MMSL model description. A yMMSL file serves as the interface between us (humans) and the muscle manager and is meant to describe the multiscale simulation and tell the muscle manager what to do.

We continue with the reaction-diffusion model example that we used the previous episode and in this episode we will connect an implementation of the reaction model to the MUSCLE3 library step by step.

## Disect your model

In the previous episode we have discussed the Submodel Execution Loop (SEL) and the various operators that are asociated with it.

::: challenge

## Exercise 1: Can you recognize the Submodel Execution Loop?

Open the file called reaction.py in a text editor. Can you recognize the beginning and end of the various operators ($F_{init}$, $O_I$, $S$ and $O_F$ ) and the state update loop in this submodel? Mark them with comments in the code (e.g. `# begin F_init`).

```python
def reaction(initial_state: np.array) -> np.array:
    """
    ...
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

:::::: solution

## Solution

```python
def reaction(initial_state: np.array) -> np.array:
    """
    ...
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
        # begin O_I
        # end O_I

        # begin S
        U += k * U * dt
        t_cur += dt
        # end S
    # end state_update_loop

    # begin O_F
    return U
    # end O_F
```

The Submodel Execution Loop specifies another operator within the state update loop, which is called $O_I$ and comes before $S$. This is where you can send a message to the outside world with (part of) the current state. In this case, the $O_I$ operator is empty; we’re not sending anything.
:::::

:::

## The constructor

To let a model communicate with the muscle manager, other submodels and the outside world we need to create a `libmuscle.Instance` object:

```python
from libmuscle import Instance

def some_example_submodel():
    instance = Instance({
            Operator.F_INIT: ['initial_state_a', 'initial_state_b'],
            Operator.O_I: ['some_intermediate_state'],
            Operator.S: ['some_other_intermediate_state'],
            Operator.O_F: ['final_state_a', 'final_state_b']})
```

The constructor takes a single argument, a dictionary that maps operators to lists of ports. Ports are used by submodels to exchange messages with the outside world and eachother. These messages usually contain the state of the model, but they can also contain other information. Ports can be input ports or output ports, but not both at the same time, the operator that they are mapped to determines how the port is used. The names of the available operators correspond to their theoretical counterparts ($F_{init}$, $O_I$, $S$ and $O_F$ ).

::: challenge

## What ports do we need?

Question: In our example of the reaction submodel, what ports do we need to communicate the model state to the outside world? Come up with good names. What operators would we need to map them to?

:::::: solution

In this model, we need:

- a single input port that will receive an initial state (e.g. named "initial_state") at the beginning of the model run and it should be mapped to the $F_{init}$ operator
- a single output port that sends the final state (e.g. named "final_State") at the end of the reaction simulation to the rest of the simulation, it should be mapped to the $O_F$ operator
::::::

:::

In multiscale simulations, submodels often have to run multiple times, for instance because they are used as a micro model or because they are part of an ensemble that cannot be completely parallelised. In order to accomplish this, the entire submodel is wrapped into a loop. Exactly when this loop needs to end often depends on the behaviour of the whole model, and is not easy to determine beforehand, but fortunately MUSCLE will do that for us if we call the `libmuscle.Instance.reuse_instance()` method.

```python
    while instance.reuse_instance():
        # F_INIT
        # State update loop
        # O_F
```

::: challenge

## Exercise 2: Constructing your submodel

Add the following to our reaction model code:

- a `libmuscle.Instance` object with the appropriate operator-port dictionary
- the reuse loop

:::: solution

```python
from libmuscle import Instance

def reaction(U_init: np.array) -> np.array:
    """
    ...
    """
    instance = Instance({
            Operator.F_INIT: ['initial_state'],       # np.array
            Operator.O_F: ['final_state']})           # np.array

    while instance.reuse_instance():
        # begin F_INIT
        t_max = 2.469136e-6
        dt = 2.469136e-8
        k = -4.05e4

        U = U_init

        t_cur = 0
        # end F_INIT

        # begin state_update_loop
        while t_cur + dt < t_max:
            # begin O_I
            # end O_I

            # begin S
            U += k * U * dt
            t_cur += dt
            # end S
        # end state_update_loop

        # begin O_F
        return U
        # end O_F
```

Note that the type of data that is sent is documented in a comment. This is obviously not required, but it makes life a lot easier if someone else needs to use the code or you haven’t looked at it for a while, so it’s highly recommended.

::::

:::

## Settings

Next is the first part of the model, in which the model is initialised. Nearly every model needs some settings that define how it behaves (e.g. the size of a timestep or ). We would like to control these settings centrally suing the MUSCLE manager when starting up the coupled simulation so we don't have to change it in our model code every time if we want to try a range of values for instance to perform a sensitivity analysis. We can use the `libmuscle.Instance.get_setting` function instead to ask the MUSCLE manager for the values. The values, or ranges of values, should be recorded in the configuration file which we will cover in the next chapter.

```python
    some_variable = instance.get_setting('variable_name', 'variable_type')
```

::: callout
The second argument, which specifies the expected type, is optional. If it is given, MUSCLE will check that the user specified a value of the correct type, and if not raise an exception.
:::

::: challenge

## Exercise 3: 
In our example several settings have been hard-coded into the model: the total time to simulate `tmax`, the time step to use `dt`, and the model parameter `k`. Change the code such that we request these settings from the MUSCLE manager.

:::::: solution

```python
from libmuscle import Instance

def reaction(U_init: np.array) -> np.array:
    """
    ...
    """
    instance = Instance({
            Operator.F_INIT: ['initial_state'],       # np.array
            Operator.O_F: ['final_state']})           # np.array

    while instance.reuse_instance():
        # begin F_INIT
        t_max = instance.get_setting('t_max', 'float')
        dt = instance.get_setting('dt', 'float')
        k = instance.get_setting('k', 'float')

        U = U_init

        t_cur = 0
        # end F_INIT

        # begin state_update_loop
        ...
```

Note that getting settings needs to happen within the reuse loop; doing it before can lead to incorrect results.

::::::
:::

## Receiving messages
After getting our settings, we want to receive the initial state for this submodel on the `initial_state` port. Note that we have declared that port above, and declared it to be associated with the F_INIT operator. During F_INIT, messages can only be received, not sent, so that declaration makes `initial_state` a receiving port.

```python
    msg = instance.receive('initial_state')
```

The message that we receive can contain several pieces of information. Here, we are interested in the `data` and `timestamp` attributes. We assume the data to be a grid of floats containing our initial state and the time stamp tells us the simulated time at which this state is valid.

```python
    U = msg.data.array.copy()
    t_cur = msg.timestamp
```

::: callout
The msg.data attribute holds an object of type libmuscle.Grid, which holds a read-only NumPy array and optionally a list of index names. Here, we take the array and make a copy of it for U, so that we can modify U in our upcoming state update. Without calling `.copy()`, U would end up pointing to the same read-only array, and we’d get an error message if we tried to modify it.

The `timestamp` attribute is a double precision float containing the number of simulated (not wall-clock) seconds since the whole simulation started. 
:::::::::::

## State update loop
Last thing is a small change in our state update loop. Instead of checking whether the simulation time does not exceed `t_max`, we have to now add up the time when we started the submodel instance, since we are part of a larger simulation.

```python
    # begin state_update_loop
        while t_cur + dt < msg.timestamp + t_max:
```

The actual state update happens in the operator `S` in the Submodel Execution Loop, and in this model, it is determined entirely by the current state. Since no information from outside is needed, we do not receive any messages, and in our `libmuscle.Instance` declaration above, we did not declare any ports associated with `Operator.S`. 

The operator `I_O` provides for observations of intermediate states. In other words, here is where you can send a message to the outside world with (part of) the current state. In this case, the O_I operator is empty; we’re not sending anything.

## Sending messages

To send a message we first have to construct a Message object containing the current simulation time and the current state. We need to convert the np.array to a MUSCLE `libmuscle.Grid` object to do so. 

::: callout
We convert our `numpy.array` U explicitly into a `libmuscle.Grid object`, so that we can add the name of the dimensions. In this case there is only one, and x is not very descriptive, so we could have also passed U directly, in which case MUSCLE would have sent a `libmuscle.Grid` without index names automatically.

Note that grids (and NumPy arrays) are much more efficient than lists and dictionaries. If you have a lot of data to send, then you should use those as much as possible. For example, a set of agents is best sent as a dictionary of 1D NumPy arrays, with one array/grid for each attribute. A list of dictionaries will be quite a bit slower and use a lot more memory, but it should work up to a million or so objects.
:::

The optional second parameter is a second timestamp, which is only used in [more advance applications](https://muscle3.readthedocs.io/en/latest/tutorial.html#message-timestamps) and can be set to `None` here.

```python
from libmuscle import Grid, Message
my_message = Message(my_timestamp, None, Grid(my_state, ['x']))
```

To send the message we specify the port on which to send which again needs to match the declaration.

```python
libmuscle.Instance.send('final_state', final_message)
```

::::::::::::::::::::::::::::::::::::: challenge

## Exercise 4: Send back the result

In the O_F operator of your model construct a message and replace the return statement with a call to `libmuscle.Instance.send()` to send the final state to the outside world.

::: solution

```python
from libmuscle import Instance, Grid, Message

def reaction(U_init: np.array) -> np.array:
    """
    ...
    """
    instance = Instance({
            Operator.F_INIT: ['initial_state'],       # np.array
            Operator.O_F: ['final_state']})           # np.array

    while instance.reuse_instance():
        # begin F_INIT
        t_max = instance.get_setting('t_max', 'float')
        dt = instance.get_setting('dt', 'float')
        k = instance.get_setting('k', 'float')

        msg = instance.receive('initial_state')
        U = msg.data.array.copy()

        t_cur = msg.timestamp
        # end F_INIT

        # begin state_update_loop
        while t_cur + dt < msg.timestamp + t_max:
            # begin O_I
            # end O_I

            # begin S
            U += k * U * dt
            t_cur += dt
            # end S
        # end state_update_loop

        # begin O_F
        final_message = Message(t_cur, None, Grid(U, ['x']))
        instance.send('final_state', final_message)
        # end O_F
```

::::::::::::
:::::::::::::

Right now your sub-model is ready to be used by the muscle manager. We will connect it to another submodel and configure it to run the coupled simulation in the next chapter. 

::: keypoints

- MUSCLE3 implements the MMSL theory
- MORE KEYPOINTS!

::::::::::::::
