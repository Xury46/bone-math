__author__ = "Xury Greer"

# Built-ins
from typing import TYPE_CHECKING

# Third Party
import bpy
from bpy.types import (
    Context,
    Operator,
)

# First Party
from .pole_angle import (
    placeholder,
)

if TYPE_CHECKING:
    # https://b3d.interplanety.org/en/how-to-properly-specify-the-return-type-of-the-blender-operator-execute-function/
    from bpy.stub_internal.rna_enums import OperatorReturnItems


class OT_BoneMath_CalculatePoleAngle(Operator):
    """Calculate and set the correct pole angle for the selected pose bones with Inverse Kinematics constraints."""

    bl_idname = "bone_math.calculate_pole_angle"
    bl_label = "Calculate pole angle"

    def execute(self, context: Context) -> set["OperatorReturnItems"]:
        placeholder(context)

        return {"FINISHED"}


classes: list[type] = [
    OT_BoneMath_CalculatePoleAngle,
]


def register() -> None:
    for class_to_register in classes:
        bpy.utils.register_class(class_to_register)


def unregister() -> None:
    for class_to_unregister in classes:
        bpy.utils.unregister_class(class_to_unregister)
