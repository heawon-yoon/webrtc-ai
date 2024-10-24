
from __future__ import annotations

import dataclasses
import io
import os
import wave
from dataclasses import dataclass
from state import State
import httpx
import asyncio

import openai




@dataclass
class _STTOptions:
    language: str
    detect_language: bool
    model: str


class STT:
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

        # throw an error on our end
        api_key = api_key or os.environ.get("OPENAI_API_KEY")
        base_url = base_url or os.environ.get("OPENAI_API_BASE")
        print("STT",api_key,base_url)
        if api_key is None:
            raise ValueError("OpenAI API key is required")

        self._client = client or openai.AsyncClient(
            api_key=api_key,
            base_url=base_url,

        )

    def _sanitize_options(self, *, language: str | None = None) -> _STTOptions:
        config = dataclasses.replace(self._opts)
        config.language = language or config.language
        return config

    async  def recognize(
        self, buffer, state: State, language: str | None = None
    ) :
        resp = None
        try:
            print("recognize start1")
            config = self._sanitize_options(language='en')
            io_buffer = io.BytesIO()
            with wave.open(io_buffer, "wb") as wav:
                wav.setnchannels(2)
                wav.setsampwidth(2)  # 16-bit
                wav.setframerate(state.sample_rate)
                wav.writeframes(buffer)
            print("recognize start2")
            resp = await  self._client.audio.transcriptions.create(
                file=(state.filename, io_buffer.getvalue(), "audio/wav"),
                model=self._opts.model,
                language=config.language,
                response_format="json",
            )
            await asyncio.sleep(0)
            print("recognize resp",resp)
            return resp
        except Exception as e:
            print(f"recognize errer {e}")




