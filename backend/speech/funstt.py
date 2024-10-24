
from __future__ import annotations

import dataclasses
import io
import wave
from dataclasses import dataclass
from state import State
import asyncio
import soundfile
from funasr import AutoModel
import librosa
import os


@dataclass
class _STTOptions:
    language: str
    detect_language: bool
    model: str


class FUN_STT:
    chunk_size = [0, 10, 5]  # [0, 10, 5] 600ms, [0, 8, 4] 480ms
    encoder_chunk_look_back = 4  # number of chunks to lookback for encoder self-attention
    decoder_chunk_look_back = 1  # number of encoder chunks to lookback for decoder cross-attention
    def __init__(
        self,
        *,
        language: str = "en",
        detect_language: bool = False,
        model: str = "whisper-1",
        base_url: str | None = None,
        api_key: str | None = None,
        client: openai.AsyncClient | None = None,
    ):
        """
        Create a new instance of OpenAI STT.

        ``api_key`` must be set to your OpenAI API key, either using the argument or by setting the
        ``OPENAI_API_KEY`` environmental variable.
        """


        if detect_language:
            language = ""

        self._opts = _STTOptions(
            language=language,
            detect_language=detect_language,
            model=model,
        )


        self._client = AutoModel(model="paraformer-zh-streaming")
        self.punc_client = AutoModel(model="ct-punc")
        self.vad_client = AutoModel(model="fsmn-vad")

    def _sanitize_options(self, *, language: str | None = None) -> _STTOptions:
        config = dataclasses.replace(self._opts)
        config.language = language or config.language
        return config

    async  def recognize(
        self, buffer, state: State, language: str | None = None
    ) :
        result = ''
        try:
            print("recognize start1",state.filename)
            with wave.open(state.filename, "wb") as wav:
                wav.setnchannels(2)
                wav.setsampwidth(2)  # 16-bit
                wav.setframerate(state.sample_rate)
                wav.writeframes(buffer)

            #重采样
            speech, sample_rate = librosa.load(state.filename, sr=None)
            dst_sig = librosa.resample(speech, orig_sr=sample_rate, target_sr=16000)
            soundfile.write(state.filename, dst_sig, 16000)
            speech, sample_rate = soundfile.read(state.filename)
            print("time speech",len(speech) / sample_rate)
            vad_res = self.vad_client.generate(input=state.filename)
            print("vad_res",vad_res[0]['value'])
            print("vad_res_len", len(vad_res[0]['value']))
            #判断噪音
            if len(vad_res[0]['value']) == 0:
                try:
                    os.remove(state.filename)
                except OSError:
                    pass
                return
            chunk_stride = self.chunk_size[1] * 960  # 600ms

            cache = {}
            total_chunk_num = int(len((speech) - 1) / chunk_stride + 1)

            for i in range(total_chunk_num):
                speech_chunk = speech[i * chunk_stride:(i + 1) * chunk_stride]
                is_final = i == total_chunk_num - 1

                res =  self._client.generate(input=speech_chunk, cache=cache, is_final=is_final, chunk_size=self.chunk_size,
                                     encoder_chunk_look_back=self.encoder_chunk_look_back,
                                     decoder_chunk_look_back=self.decoder_chunk_look_back)

                if i == 0:
                    state.response_player.channel.send(f"Human: start-response")
                result += res[0]["text"]
                if is_final:
                    result = self.punc_client.generate(input=result)[0]['text']
                state.response_player.channel.send(f"Human: {result}")
                print(result)
                await asyncio.sleep(0)
            return result
        except Exception as e:
            print(f"recognize errer {e}")




