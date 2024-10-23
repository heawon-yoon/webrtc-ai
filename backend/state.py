from asyncio import Task
import copy
import uuid

import librosa
import numpy as np
from aiortc import RTCPeerConnection, RTCDataChannel, MediaStreamTrack
from av import AudioFrame
import webrtcvad
from playback_stream_track import PlaybackStreamTrack
import logging
import soundfile
from rtc.video_track import VideoTrack


class State:
    track: MediaStreamTrack
    video_track: MediaStreamTrack
    buffer: list = []
    recording: bool = False
    task: Task
    video_task:Task
    sample_rate: int = 16000
    counter: int = 0
    response_player: PlaybackStreamTrack = PlaybackStreamTrack()
    video_frame = None

    logger = logging.getLogger("pc")

    def __init__(self):
        self.pc = RTCPeerConnection()
        self.id = str(uuid.uuid4())
        self.filename = f"{self.id}.wav"
        # 初始化 VAD
        self.vad = webrtcvad.Vad()
        self.vad.set_mode(3)  # 设置 VAD 模式
        self.silence_frames = 0  # 初始化静音帧数
        self.sample_rate = 16000
        self.logger = logging.getLogger("pc")

    def log_info(self, msg, *args):
        print("log_info",msg,*args)
        self.logger.info(self.id + " " + msg, *args)

    def append_frame(self, frame: AudioFrame):
        #print("append_frame")
        buffer = frame.to_ndarray().flatten().astype(np.int16)
        # check for silence
        max_abs = np.max(np.abs(buffer))
        if True or max_abs > 50:
            if self.sample_rate != frame.sample_rate * 2:
                self.sample_rate = frame.sample_rate * 2
            self.buffer.append(buffer)

    def append_frame_orgin(self, frame: AudioFrame):
        #print("append_frame")

        self.buffer.append(frame)

    def flush_audio(self):
        print("Flushing audio...")
        self.buffer = np.array(self.buffer).flatten()
        self.log_info(f"Buffer Size: {len(self.buffer)}")

        # write to file
        data = copy.deepcopy(self.buffer)
        data = librosa.util.buf_to_float(data)
        self.buffer = []
        data = librosa.resample(data, orig_sr=self.sample_rate,
                                target_sr=16000)
        soundfile.write(self.filename, data, 16000)
        print("Finished writing audio.")
        return data
