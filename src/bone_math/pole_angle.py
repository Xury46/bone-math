"""
Adapted from: https://blender.stackexchange.com/a/19755
by Jaroslav Jerryno Novotny
"""

__author__ = "Xury Greer"

# Third Party
from bpy.types import (
    PoseBone,
)
from mathutils import (
    Vector,
)


def signed_angle(
    vector_a: Vector,
    vector_b: Vector,
    normal: Vector,
) -> float:
    """Get the signed angle between two vectors.

    :param vector_a: The first vector.
    :param vector_b: The second vector.
    :param normal: Sign will be determined by this orientation.
    :return: The signed angle between the two vectors around the given normal axis.
    """

    angle: float = vector_a.angle(vector_b)
    if vector_a.cross(vector_b).angle(normal) < 1.0:
        angle = -angle
    return angle


def get_pole_angle(
    start_bone: PoseBone,
    end_bone: PoseBone,
    pole_location: Vector,
) -> float:
    """Calculate the pole angle for bones in an IK chain.
    The resulting angle will align the IK chain so that the bones don't move from their rest positions.

    Pole angle is a signed angle between the start_bone's X axis and
    the projected pole_axis onto start_bone's XZ plane.
    The direction of projection is IK_axis.

    :param start_bone: The first bone in the IK chain.
    :param end_bone: The final bone in the IK chain.
    :param pole_location: The location of the pole target.
    :return: The signed angle value in radians that is required to make the IK chain aim
        at the pole target so that it matches the resting pose.
    """

    # Axis aimed from the base of the chain to the end of the chain.
    start_to_end: Vector = end_bone.tail - start_bone.head

    # Axis aimed from the base of the chain, to the pole target.
    start_to_pole: Vector = pole_location - start_bone.head

    pole_normal: Vector = start_to_end.cross(start_to_pole)

    projected_pole_axis: Vector = pole_normal.cross(start_bone.y_axis)

    pole_angle: float = signed_angle(
        start_bone.x_axis,
        projected_pole_axis,
        start_bone.y_axis,
    )

    return pole_angle
