import enum


@enum.unique
class InviteTargetType(enum.IntEnum):
    """https://discord.com/developers/docs/resources/invite#invite-object-invite-target-types"""
    STREAM = 1
    EMBEDDED_APPLICATION = 2
