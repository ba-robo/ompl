# MORSE builder script
# requires name of the environment *.blend file as a parameter

import sys

import bpy
import morse.builder

# IMPORTANT! Set this manually for now
OMPL_DIR='/home/caleb/repos/ompl_morse'

# Add a robot (TODO: make user-specified)
robot = morse.builder.ATRV()

# Determine the blend file to load (first argument after '--')
envpath = sys.argv[sys.argv.index('--') + 1]
print("\n* Loading scene <%s>.\n" % envpath)
env = morse.builder.Environment(envpath)

# Create '__planner' object so we can set up the game engine
bpy.ops.object.add()
obj = bpy.context.object
obj.name = "__planner"

# Add 'Tick' sensor
bpy.ops.logic.sensor_add(type='DELAY', name='Tick')
tick = obj.game.sensors['Tick']
tick.use_repeat = True

# Add '__communicator.py' text block
bpy.ops.text.open(filepath=OMPL_DIR + "scripts/morse/communicator.py")

# Add 'Comm' controller
bpy.ops.logic.controller_add(type='PYTHON', name='Comm')
comm = obj.game.controllers['Comm']
comm.mode = 'MODULE'
comm.module = 'communicator.main'

# Link Tick with Comm so it's run every frame
tick.link(comm)

env.create()


