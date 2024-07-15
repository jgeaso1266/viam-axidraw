import sys
from typing import ClassVar, Mapping, Sequence, Any, Dict, Optional, Tuple, Final, List, cast
from typing_extensions import Self

from typing import Any, Dict, Final, List, Optional

from pyaxidraw import axidraw



from viam.components.gantry import Gantry
from viam.module.types import Reconfigurable
from viam.operations import run_with_operation
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName
from viam.resource.base import ResourceBase
from viam.resource.types import Model, ModelFamily

from viam.logging import getLogger

import time
import asyncio

LOGGER = getLogger(__name__)

MM_TO_INCHES = 0.0393 #TODO check the resolution of this gantry
class axidrawer(Gantry, Reconfigurable):
    
    """
    An AxiDraw Gantry component that connects to the controller via a usb connection and
    sets the starting positions of the plotter to 0,0,0.
    The lengths correspond to the AxiDrawV3  lengths and the servo is assumed 
    """
    def __init__(self, name: str):
        super().__init__(name)
        # Starting State
        self.lengths = [430.0 ,291.0,17.0]
        self.position = [0.0 ,0.0,0.0]
        self.is_stopped = True
        self.axi_draw = axidraw.AxiDraw()
        # Initialize class from viam-axidraw's axidraw package
        self.axi_draw.interactive()       # Enter interactive context
        if not self.axi_draw.connect():   # Open serial port to AxiDraw;
            sys.exit()                  # Exit, if no connection.

    def __del__(self):
        self.axi_draw.disconnect()

    MODEL: ClassVar[Model] = Model(ModelFamily("jalen", "viam-axidraw"), "axidraw")
    
    # create any class parameters here, 'some_pin' is used as an example (change/add as needed)
    some_pin: int

    # Constructor
    @classmethod
    def new(cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        my_class = cls(config.name)
        my_class.reconfigure(config, dependencies)
        return my_class

    # Validates JSON Configuration
    @classmethod
    def validate(cls, config: ComponentConfig):
        """ does nothing, there are no attributes to change in this model """

    # Handles attribute reconfiguration
    def reconfigure(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]):
        """ reconfigure does nothing, there are no attributes to change in this model"""

    @run_with_operation
    async def get_position(self, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None, **kwargs) -> List[float]:
        """
        Get the positions of the axes of the gantry in millimeters.

        ::

            my_gantry = Gantry.from_robot(robot=robot, name="my_gantry")

            # Get the current positions of the axes of the gantry in millimeters.
            positions = await my_gantry.get_position()

        Returns:
            List[float]: A list of the position of the axes of the gantry in millimeters.

        For more information, see `Gantry component <https://docs.viam.com/components/gantry/>`_.
        """
        ...

    
    async def move_to_position(
        self,
        positions: List[float],
        speeds: List[float],
        *,
        extra: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs,
    ):
        """
        Move the axes of the gantry to the desired positions (mm) at the requested speeds (mm/sec).

        ::

            my_gantry = Gantry.from_robot(robot=robot, name="my_gantry")

            # Create a list of positions for the axes of the gantry to move to. Assume in
            # this example that the gantry is multi-axis, with 3 axes.
            examplePositions = [1, 2, 3]

            exampleSpeeds = [3, 9, 12]

            # Move the axes of the gantry to the positions specified.
            await my_gantry.move_to_position(
                positions=examplePositions, speeds=exampleSpeeds)

        Args:
            positions (List[float]): A list of positions for the axes of the gantry to move to, in millimeters.
            speeds (List[float]): A list of speeds in millimeters per second for the gantry to move at respective to each axis.

        For more information, see `Gantry component <https://docs.viam.com/components/gantry/>`_.
        """
        operation = self.get_operation(kwargs)
        self.is_stopped = False
        self.position = positions

        positions_inches = positions*MM_TO_INCHES

        if positions[2] > 0: # zero is the ground plane for the third axis - the servo
            #TODO: servo up/down through their position or an extra parameter as a bool
            # ask for user preference.
            self.axi_draw.moveto(
                # Move with pen up
                positions_inches[0], 
                positions_inches[1]) 
        else:
             # Move with pen down
            self.axi_draw.lineto(
                positions_inches[0], 
            positions_inches[1])

        self.is_stopped = True
        # Check if the operation is cancelled and, if it is, stop the gantry's motion
        if await operation.is_cancelled():
            await self.stop()

    
    async def home(self, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None, **kwargs) -> bool:
        """
        Run the homing sequence of the gantry to re-calibrate the axes with respect to the limit switches.

        ::

            my_gantry = Gantry.from_robot(robot=robot, name="my_gantry")

            await my_gantry.home()

        Returns:
            bool: Whether the gantry has run the homing sequence successfully.

        For more information, see `Gantry component <https://docs.viam.com/components/gantry/>`_.
        """
        self.move_to_position([0,0,0])
        return True

    
    async def get_lengths(self, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None, **kwargs) -> List[float]:
        """
        Get the lengths of the axes of the gantry in millimeters.

        ::

            my_gantry = Gantry.from_robot(robot=robot, name="my_gantry")

            # Get the lengths of the axes of the gantry in millimeters.
            lengths_mm = await my_gantry.get_lengths()

        Returns:
            List[float]: A list of the lengths of the axes of the gantry in millimeters.

        For more information, see `Gantry component <https://docs.viam.com/components/gantry/>`_.
        """
        return self.lengths

    
    async def stop(self, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None, **kwargs):
        """
        Stop all motion of the gantry. It is assumed that the gantry stops immediately.

        ::

            my_gantry = Gantry.from_robot(robot=robot, name="my_gantry")

            # Stop all motion of the gantry. It is assumed that the gantry stops
            # immediately.
            await my_gantry.stop()

        For more information, see `Gantry component <https://docs.viam.com/components/gantry/>`_.
        """
        self.is_stopped = True

    
    async def is_moving(self) -> bool:
        """
        Get if the gantry is currently moving.

        ::

            my_gantry = Gantry.from_robot(robot=robot, name="my_gantry")

            # Stop all motion of the gantry. It is assumed that the
            # gantry stops immediately.
            await my_gantry.stop()

            # Print if the gantry is currently moving.
            print(my_gantry.is_moving())

        Returns:
            bool: Whether the gantry is moving.

        For more information, see `Gantry component <https://docs.viam.com/components/gantry/>`_.
        """
        return not self.is_stopped

