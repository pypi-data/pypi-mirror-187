import sys
import typing
import bpy.types

from . import types
from . import utils
from . import app
from . import ops
from . import path
from . import msgbus
from . import context
from . import props

data: 'bpy.types.BlendData' = None
''' Access to Blender's internal data
'''
