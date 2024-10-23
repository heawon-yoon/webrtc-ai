from __future__ import annotations

import asyncio
import soundfile as sf
import librosa
import edge_tts
import av
import numpy as np
from state import State
import fractions
import uuid

class EDGS_TTS:

    def __init__(
        self,
        *,
        voice: str = "zh-CN-XiaoyiNeural",
        speed: float = 1.0,
    ) -> None:

        self.voice = voice

    async def synthesize(self, text: str, state: State):
        tmp_file = "./tmp/"+str(uuid.uuid4())+".wav"
        print("edgs synthesize", text, state.response_player.filename,tmp_file)
        try:
            communicate = edge_tts.Communicate(text, self.voice)
            with open(tmp_file, "wb") as file:
                  for chunk in communicate.stream_sync():
                    if chunk["type"] == "audio":

                        file.write(chunk["data"])
                    elif chunk["type"] == "WordBoundary":
                        print(f"WordBoundary: {chunk}")
            await asyncio.sleep(0)
            # 加载 MP3 文件
            audio, sr = librosa.load(tmp_file, sr=None)
            print("edgs synthesize start")
            while(state.response_player.speeking):
                await asyncio.sleep(0)
            print("edgs synthesize end")
            sf.write(state.response_player.filename, audio,sr)

            #转成wav文件 发送音频帧队列模式需要优化 暂留代码~_~
            # data, sample_rate = sf.read(tmp_file,dtype=np.int16)
            # # 获取通道数
            # CHANNELS = data.shape[1] if data.ndim > 1 else 1
            #
            # # 将数据按4096大小切分
            # frame_size = int(sample_rate*0.02)
            # num_frames = len(data) // frame_size
            #
            # # 创建 AudioFrame 对象的列表
            # _timestamp = 0
            # print(f"edgs start sp")
            #
            # for i in range(num_frames):
            #     # 提取每个帧
            #     frame_data = data[i * frame_size:(i + 1) * frame_size]
            #
            #     # 转换为所需格式
            #     audio_data = np.frombuffer(frame_data, dtype=np.int16).reshape(-1, 1)
            #
            #     # 创建 AudioFrame 对象
            #     frame = av.AudioFrame.from_ndarray(audio_data.T, format="s16",
            #                                     layout="stereo" if CHANNELS == 2 else "mono")
            #     frame.sample_rate = sample_rate
            #     frame.time_base = fractions.Fraction(1, sample_rate)
            #     _timestamp += frame_size
            #     frame.pts = _timestamp
            #     json = {'frame': frame, 'index': i}
            #
            #     await state.response_player.audio_frame_queue.put(json)
            # # 处理剩余的音频数据（如果有）
            # if len(data) % frame_size != 0:
            #     frame_data = data[num_frames * frame_size:]
            #     # 转换为所需格式
            #     audio_data = np.frombuffer(frame_data, dtype=np.int16).reshape(-1, 1)
            #
            #     # 创建 AudioFrame 对象
            #     frame = av.AudioFrame.from_ndarray(audio_data.T, format="s16",
            #                                        layout="stereo" if CHANNELS == 2 else "mono")
            #     frame.sample_rate = sample_rate
            #     frame.time_base = fractions.Fraction(1, sample_rate)
            #     _timestamp += frame_size
            #     frame.pts = _timestamp
            #
            #     json = {'frame': frame, 'index': frame_size}
            #     await state.response_player.audio_frame_queue.put(json)


        except Exception as e:
            print("synthesize errer",e)

