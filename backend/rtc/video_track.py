import numpy as np
from aiortc import VideoStreamTrack


class VideoTrack(VideoStreamTrack):
    def __init__(self, track):
        super().__init__()
        self.track = track

    async def recv(self):
        frame = await self.track.recv()
        # 将帧数据转换为图像
        return frame

