# Copyright 2023 LiveKit, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import AsyncContextManager
import wave
import io
import httpx

import openai


OPENAI_TTS_SAMPLE_RATE = 24000
OPENAI_TTS_CHANNELS = 1


@dataclass
class _TTSOptions:
    model: str
    voice: str
    speed: float


class TTS:
    def __init__(
        self,
        *,
        model: str = "tts-1",
        voice: str = "alloy",
        speed: float = 1.0,
        base_url: str | None = None,
        api_key: str | None = None,
        client: openai.AsyncClient | None = None,
    ) -> None:
        """
        Create a new instance of OpenAI TTS.

        ``api_key`` must be set to your OpenAI API key, either using the argument or by setting the
        ``OPENAI_API_KEY`` environmental variable.
        """



        # throw an error on our end
        api_key = api_key or os.environ.get("OPENAI_API_KEY")
        base_url = base_url or os.environ.get("OPENAI_API_BASE")
        if api_key is None:
            raise ValueError("OpenAI API key is required")

        # self._client = client or openai.AsyncClient(
        #     api_key=api_key,
        #     base_url=base_url,
        #     http_client=httpx.AsyncClient(
        #         timeout=5.0,
        #         follow_redirects=True,
        #         limits=httpx.Limits(
        #             max_connections=1000,
        #             max_keepalive_connections=100,
        #             keepalive_expiry=120,
        #         ),
        #     ),
        # )

        self._client = openai.AsyncOpenAI(api_key=api_key,
             base_url=base_url,)

        self._opts = _TTSOptions(
            model=model,
            voice=voice,
            speed=speed,
        )

    async def synthesize(self, text: str, filename: str):
        print("synthesize",text)
        try:
            stream =  await self._client.audio.speech.create(
                input=text,
                model=self._opts.model,
                voice=self._opts.voice,
                response_format="wav",
                speed=self._opts.speed,
            )
        except Exception as e:
            print("synthesize errer",e)

        stream.stream_to_file(filename)
