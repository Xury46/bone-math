__author__ = "Xury Greer"

# Built-ins
from typing import (
    TYPE_CHECKING,
    Literal,
    cast,
)

# Third Party
import bpy
from bpy.types import (
    Armature,
    Context,
    KinematicConstraint,
    Object,
    Operator,
    PoseBone,
)

# First Party
from .pole_angle import (
    get_pole_angle,
)

if TYPE_CHECKING:
    # https://b3d.interplanety.org/en/how-to-properly-specify-the-return-type-of-the-blender-operator-execute-function/
    from bpy.stub_internal.rna_enums import (
        OperatorReturnItems,
    )

    PosePositionItems = Literal["POSE", "REST"]


class OT_BoneMath_CalculatePoleAngle(Operator):
    """Calculate and set the correct pole angle for all selected pose bones that have Inverse Kinematics constraints."""

    bl_idname = "bone_math.calculate_pole_angle"
    bl_label = "Calculate Pole Angle"
    bl_icon = "CON_ROTLIMIT"

    @classmethod
    def poll(cls, context: Context) -> bool:
        if context.mode != "POSE":
            return False

        pose_bones: list[PoseBone] = context.selected_pose_bones
        if not pose_bones:
            return False

        armature_object: Object | None = context.active_object
        if armature_object is None:
            return False

        return True

    def execute(self, context: Context) -> set["OperatorReturnItems"]:
        pose_bones: list[PoseBone] = context.selected_pose_bones
        armature_object: Object = cast(Object, context.active_object)
        armature: Armature = cast(Armature, armature_object.data)

        # Cache the pose position the user had the armature set to.
        original_pose_position: PosePositionItems = armature.pose_position

        for pose_bone in pose_bones:
            # set_pole_angle(context, armature_object, pose_bone)

            ik_constraint: KinematicConstraint | None = None
            for constraint in pose_bone.constraints:
                if constraint.type == "IK":
                    ik_constraint = cast(KinematicConstraint, constraint)
                    break
            else:
                continue

            base_bone: PoseBone = pose_bone

            chain_length: int = ik_constraint.chain_count
            if chain_length == 0:
                # With a chain length of 0,
                # the chain keeps going until it reaches a bone with no parent.
                while base_bone.parent:
                    base_bone = base_bone.parent
            else:
                # Walk up the bone parent hierarchy to find the start of the chain.
                for _ in range(1, ik_constraint.chain_count):
                    base_bone = base_bone.parent

            if base_bone is None:
                return {"CANCELLED"}

            pole_bone = ik_constraint.pole_target
            if pole_bone is None:
                return {"CANCELLED"}

            if pole_bone.type == "ARMATURE":
                pole_bone = armature_object.pose.bones[ik_constraint.pole_subtarget]

            if pole_bone is None:
                return {"CANCELLED"}

            if (base_bone is not None) and (pole_bone is not None):
                # Switch to rest pose and force an update so we can work with the bones in their resting positions.
                armature.pose_position = "REST"
                bpy.context.view_layer.update()

                pole_angle: float = get_pole_angle(base_bone, pose_bone, pole_bone.matrix.translation)

                # Switch back to the pose position the user had previously.
                armature.pose_position = original_pose_position

                ik_constraint.pole_angle = pole_angle

        return {"FINISHED"}


classes: list[type] = [OT_BoneMath_CalculatePoleAngle]


def register() -> None:
    for class_to_register in classes:
        bpy.utils.register_class(class_to_register)


def unregister() -> None:
    for class_to_unregister in classes:
        bpy.utils.unregister_class(class_to_unregister)
