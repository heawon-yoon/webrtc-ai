#!/usr/bin/env python3

"""
Basic audio streaming example.

This example shows how to stream the audio data from the TTS engine,
and how to get the WordBoundary events from the engine (which could
be ignored if not needed).

The example streaming_with_subtitles.py shows how to use the
WordBoundary events to create subtitles using SubMaker.
"""

import asyncio

import edge_tts

TEXT = "可以,听到我说话吗"
VOICE = "zh-CN-XiaoyiNeural"
OUTPUT_FILE = "tts.mp3"


async def amain() -> None:
    """Main function"""
    communicate = edge_tts.Communicate(TEXT, VOICE)
    with open(OUTPUT_FILE, "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                print(f"WordBoundary: {chunk}")


if __name__ == "__main__":
    asyncio.run(amain())
