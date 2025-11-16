__author__ = "Xury Greer"

# Third Party
import bpy
from bpy.types import (
    Context,
)


def placeholder(context: Context) -> None:
    """Placeholder function.

    :param context: The current Blender context.
    """

    print(context.active_object)
