import logging
from pathlib import Path

import libmuscle
from libmuscle.runner import run_simulation
import ymmsl


from diffusion import diffusion
from reaction import reaction


# Configure Python logging
logging.basicConfig()
logging.getLogger('yatiml').setLevel(logging.WARNING)

# Set this to logging.DEBUG to get some more information
logging.getLogger().setLevel(logging.INFO)

# Load configuration
configuration = ymmsl.load(Path('reaction_diffusion.ymmsl'))

# Connect the model functions to the configuration
implementations = {'diffusion': diffusion, 'reaction': reaction}

# And run the coupled simulation!
run_simulation(configuration, implementations)
