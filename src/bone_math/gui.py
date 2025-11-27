__author__ = "Xury Greer"

# Built-ins
from typing import cast

# Third Party
import bpy
from bpy.types import (
    Context,
    KinematicConstraint,
    UILayout,
)

# First Party
from .operators import OT_BoneMath_CalculatePoleAngle


def calculate_pole_angle_context_menu(self, context: Context) -> None:
    """Append CalculatePoleAngle operator to the
    right-click context menu of the Inverse Kinematic constraint.

    :param context: The current Blender context.
    """

    try:
        ik_constraint: KinematicConstraint | None = getattr(context, "constraint")
        if isinstance(ik_constraint, KinematicConstraint):
            cast(UILayout, self.layout).operator(
                operator=OT_BoneMath_CalculatePoleAngle.bl_idname,
                icon=OT_BoneMath_CalculatePoleAngle.bl_icon,
                text=OT_BoneMath_CalculatePoleAngle.bl_label,
            )
    except AttributeError:
        pass


def register() -> None:
    bpy.types.UI_MT_button_context_menu.append(
        calculate_pole_angle_context_menu,
    )


def unregister() -> None:
    bpy.types.UI_MT_button_context_menu.remove(
        calculate_pole_angle_context_menu,
    )
