import asyncio
from typing import Optional

from aiortc import MediaStreamTrack, RTCDataChannel
from aiortc.contrib.media import MediaPlayer
import uuid
from collections import deque
import numpy as np
import av
import time

class PlaybackStreamTrack(MediaStreamTrack):
    kind = "audio"
    response_ready: bool = False
    previous_response_silence: bool = False
    track: MediaStreamTrack = None
    counter: int = 0
    time: float = 0.0
    channel: Optional[RTCDataChannel] = None
    filename: Optional[str] = None
    id: Optional[str] = None


    def __init__(self):
        self.id = str(uuid.uuid4())
        super().__init__()  # don't forget this!
        self.audio_frame_queue = asyncio.Queue()
        self.lock = asyncio.Lock()
        self.sample_rate = 24000
        self.channels = 1  # 单声道
        self.frame_length = 1024  # 每帧的样本数

    def select_track(self):
        if self.response_ready:
            self.track = MediaPlayer(self.filename, format="wav", loop=False).audio
        else:
            self.track = MediaPlayer("silence.wav", format="wav", loop=False).audio
        if self.channel is not None and self.channel.readyState == "open":
            if self.response_ready:
                self.channel.send("playing: response")
                self.previous_response_silence = False
            else:
                if not self.previous_response_silence:
                    print("select_track silence")
                    self.channel.send("playing: silence")
                    self.previous_response_silence = True

    async def recv(self):
        self.counter += 1
        if self.track is None:
            print("No track found")
            self.select_track()
        try:
            frame = await self.track.recv()
        except Exception as e:
            self.speeking = False
            if self.response_ready:
                self.response_ready = False
            self.select_track()
            frame = await self.track.recv()
        if frame.pts < frame.sample_rate * self.time:
            frame.pts = frame.sample_rate * self.time
        self.time += 0.02
        return frame

    async def recv2(self):
        # 从队列中获取音频帧
        if self.audio_frame_queue:
            import time
            try:
                frame = await self.audio_frame_queue.get()  # 从队列中取出音频数据
                frame = frame["frame"]
                sample_rate = frame.sample_rate
                samples = int(0.02 * sample_rate)

                if hasattr(self, "_timestamp"):
                    self._timestamp += samples
                    wait = self._start + (self._timestamp / sample_rate) - time.time()
                    await asyncio.sleep(wait)
                else:
                    self._start = time.time()
                    self._timestamp = 0
                frame.pts = self._timestamp
                await asyncio.sleep(0)
                return frame
            except Exception as e:
                # 如果队列为空，可以选择返回静音帧
                print("recv queue error",e)
                frame = await MediaPlayer("silence.wav", format="wav", loop=False).audio.recv()
                if frame.pts < frame.sample_rate * self.time:
                    frame.pts = frame.sample_rate * self.time
                self.time += 0.02
                return frame
        else:
            self._timestamp = 0
            # 如果队列为空，可以选择返回静音帧
            frame = await MediaPlayer("silence.wav", format="wav", loop=False).audio.recv()
            if frame.pts < frame.sample_rate * self.time:
                frame.pts = frame.sample_rate * self.time
            self.time += 0.02
            return frame


    def _create_av_packet(self, audio_data):
        # 将 numpy 数组转换为 AVPacket
        frame = av.AudioFrame.from_ndarray(audio_data)
        return frame
