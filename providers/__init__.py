"""Official video-provider adapters.

MixReel does not relay generation through a hosted gateway. Each adapter calls
one vendor's public API with a key the user supplies.
"""

from .base import MediaRef, ProviderError, TaskStatus, VideoProvider, VideoRequest
from .minimax_video import MiniMaxVideo
from .seedance_video import SeedanceVideo

__all__ = [
    "MediaRef",
    "MiniMaxVideo",
    "ProviderError",
    "SeedanceVideo",
    "TaskStatus",
    "VideoProvider",
    "VideoRequest",
]
