"""
This file registers the model with the Python SDK.
"""

from viam.components.gantry import Gantry
from viam.resource.registry import Registry, ResourceCreatorRegistration

from .axidraw import axidraw

Registry.register_resource_creator(Gantry.SUBTYPE, axidraw.MODEL, ResourceCreatorRegistration(axidraw.new, axidraw.validate))
