"""
This file registers the model with the Python SDK.
"""

from viam.components.gantry import Gantry
from viam.resource.registry import Registry, ResourceCreatorRegistration

from .axidraw import axidrawer

Registry.register_resource_creator(Gantry.SUBTYPE, axidrawer.MODEL, ResourceCreatorRegistration(axidrawer.new, axidrawer.validate))
