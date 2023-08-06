from ...types import VarInt, UnsignedShort, Long, String, NextState, UnsignedByte, Byte, Bool, Int, ByteArray, Position, Float, Double, Short, Angle
from ...p import Night
from cubelib.proto.version_independent.ClientBound import ClassicLogin


class Login(ClassicLogin):
    pass

class Play:

    class JoinGame(Night):

        EntityID: Int
        Gamemode: UnsignedByte
        Dimension: Byte
        Difficulty: UnsignedByte
        MaxPlayers: UnsignedByte
        LevelType: String
        ReducedDebugInfo: Bool

    class PluginMessage(Night):

        Channel: String
        Data: ByteArray

    class ServerDifficulty(Night):

        Difficulty: UnsignedByte

    class SpawnPosition(Night):

        Location: Position

    class PlayerAbilities(Night):

        Flags: Byte
        FlyingSpeed: Float
        FOVModifier: Float

    class ChatMessage(Night):

        Json_Data: String
        Position: Byte

    class KeepAlive(Night):

        KeepAliveID: VarInt

    class PlayerPositionAndLook(Night):

        X: Double
        FeetY: Double
        Z: Double
        Yaw: Float
        Pitch: Float
        Flags: Byte

    class TimeUpdate(Night):

        WorldAge: Long
        TimeOfDay: Long

    class WindowItems(Night):

        WindowID: UnsignedByte
        Count: Short
        SlotData: ByteArray

    class EntityRelativeMove(Night):

        EntityID: VarInt
        DeltaX: Byte
        DeltaY: Byte
        DeltaZ: Byte
        OnGround: Bool

    class EntityLook(Night):

        EntityID: VarInt
        Yaw: Angle
        Pitch: Angle
        OnGround: Bool

    class EntityLookAndRelativeMove(Night):

        EntityID: VarInt
        DeltaX: Byte
        DeltaY: Byte
        DeltaZ: Byte
        Yaw: Angle
        Pitch: Angle
        OnGround: Bool

    class EntityHeadLook(Night):

        EntityID: VarInt
        HeadYaw: Angle

    class EntityVelocity(Night):

        EntityID: VarInt
        VelocityX: Short
        VelocityY: Short
        VelocityZ: Short

    class EntityStatus(Night):

        EntityID: Int
        EntityStatus: Byte

    class Disconnect(Night):
        Reason: String

    class EntityEquipment(Night):

        EntityID: VarInt
        Slot: Short
        Item: ByteArray  # ?slot

    map = {
        0x00: KeepAlive,
        0x01: JoinGame,
        0x02: ChatMessage,
        0x03: TimeUpdate,
        0x04: EntityEquipment,
        0x05: SpawnPosition,
        0x06: None,  # UpdateHealth,
        0x07: None,  # Respawn,
        0x08: PlayerPositionAndLook,
        0x09: None,  # HeldItemChange,
        0x0A: None,  # UseBed,
        0x0B: None,  # Animation,
        0x0C: None,  # SpawnPlayer,
        0x0D: None,  # CollectItem,
        0x0E: None,  # SpawnObject,
        0x0F: None,  # SpawnMob,
        0x10: None,  # SpawnPainting,
        0x11: None,  # SpawnExperienceOrb,
        0x12: EntityVelocity,
        0x13: None,  # DestroyEntities,
        0x14: None,  # Entity,
        0x15: EntityRelativeMove,
        0x16: EntityLook,
        0x17: EntityLookAndRelativeMove,
        0x18: None,  # EntityTeleport,
        0x19: EntityHeadLook,
        0x1A: EntityStatus,
        0x1B: None,  # AttachEntity,
        0x1C: None,  # EntityMetadata,
        0x1D: None,  # EntityEffect,
        0x1E: None,  # RemoveEntityEffect,
        0x1F: None,  # SetExperience,
        0x20: None,  # EntityProperties,
        0x21: None,  # ChunkData,
        0x22: None,  # MultiBlockChange,
        0x23: None,  # BlockChange,
        0x24: None,  # BlockAction,
        0x25: None,  # BlockBreakAnimation,
        0x26: None,  # MapChunkBulk,
        0x27: None,  # Explosion,
        0x28: None,  # Effect,
        0x29: None,  # SoundEffect,
        0x2A: None,  # Particle,
        0x2B: None,  # ChangeGameState,
        0x2C: None,  # SpawnGlobalEntity,
        0x2D: None,  # OpenWindow,
        0x2E: None,  # CloseWindow,
        0x2F: None,  # SetSlot,
        0x30: WindowItems,
        0x31: None,  # WindowProperty,
        0x32: None,  # ConfirmTransaction,
        0x33: None,  # UpdateSign,
        0x34: None,  # Map,
        0x35: None,  # UpdateBlockEntity,
        0x36: None,  # OpenSignEditor,
        0x37: None,  # Statistics,
        0x38: None,  # PlayerListItem,
        0x39: PlayerAbilities,
        0x3A: None,  # TabComplete,
        0x3B: None,  # ScoreboardObjective,
        0x3C: None,  # UpdateScore,
        0x3D: None,  # DisplayScoreboard,
        0x3E: None,  # Teams,
        0x3f: PluginMessage,
        0x40: Disconnect,
        0x41: None,  # ServerDifficulty,
        0x42: None,  # CombatEvent,
        0x43: None,  # Camera,
        0x44: None,  # WorldBorder,
        0x45: None,  # Title,
        0x46: None,  # SetCompression,
        0x47: None,  # PlayerListHeaderAndFooter,
        0x48: None,  # ResourcePackSend,
        0x49: None,  # UpdateEntityNBT
    }
    inv_map = {v: k for k, v in map.items()}
