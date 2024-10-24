import argparse
import asyncio
import json
import logging
import os
import ssl
import threading
from asyncio import create_task, AbstractEventLoop
from typing import Optional
from aiohttp import web
import aiohttp_cors
from aiortc import RTCSessionDescription, MediaStreamTrack
from av import AudioFrame, VideoFrame

import copy
from util.utils import deleteFile, is_ending_with_punctuation, merge_frame

from chain import Chain
from state import State
import numpy as np
from  speech.stt import STT
from speech.tts import TTS
from speech.funstt import FUN_STT
from speech.edgs_tts import EDGS_TTS
import openai
logger = logging.getLogger("pc")
ROOT = os.path.dirname(__file__)

from dotenv import load_dotenv

load_dotenv()

pcs = set()


stt = FUN_STT()
tts = EDGS_TTS()


async def offer(request):
    params = await request.json()

    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

    state = State()
    pcs.add(state)


    state.log_info("Created for %s", request.remote)

    state.pc.addTrack(state.response_player)

    @state.pc.on("iceconnectionstatechange")
    async def on_iceconnectionstatechange():
        state.log_info("ICE connection state is %s", state.pc.iceConnectionState)
        if state.pc.iceConnectionState == "failed":
            await state.pc.close()

    async def record():
        track = state.track
        state.log_info("Recording %s", state.filename)
        pre_frame_time = 0
        sum_duration = 0
        sum_speaking_duration = 0
        check_speech = False
        while True:
            frame: AudioFrame = await track.recv()
            if state.recording:

                durantion = frame.time-pre_frame_time
                pre_frame_time = frame.time

                # 将音频帧转换为 PCM 格式 (16-bit, 16 kHz, 单声道)
                buffer = frame.to_ndarray().flatten().astype(np.int16)
                # 检查音频帧是否包含语音
                is_speech = state.vad.is_speech(buffer, frame.sample_rate)

                if is_speech:
                    check_speech = True
                    state.append_frame_orgin(frame)
                    state.sample_rate = frame.sample_rate

                    sum_duration = 0
                    #print("audio frame length", len(state.buffer))

                if check_speech and is_speech is False:
                    sum_duration += durantion

                # 如果静音帧数超过阈值（假设阈值为3秒）
                if check_speech and sum_duration > 1:

                    check_speech = False
                    state.counter += 1
                    if not os.path.exists("./tmp"):
                        os.makedirs("./tmp")
                    state.filename = f"./tmp/{state.id}_{state.counter}.wav"
                    state.response_player.filename = f"./tmp/{state.response_player.id}_{state.counter}.wav"
                    # 在此处添加将音频转换成文字的逻辑
                    print("开始转换音频成文字")
                    await asyncio.sleep(0.1)
                    tmp_buffer = state.buffer
                    state.buffer = []

                    try:
                        await transcribe_request(tmp_buffer)
                    except:
                        pass

            await asyncio.sleep(0)


    async def record_video():
        track = state.video_track
        while True:
            try:
                frame: VideoFrame = await track.recv()
                state.video_frame = frame
            except:
                pass
            #print("video frame",frame)

            await asyncio.sleep(0)

    @state.pc.on("track")
    async def on_track(track: MediaStreamTrack):
        print("Track received",track.kind)
        state.log_info("Track %s received", track.kind)

        if track.kind == "audio":
            state.log_info("Received %s", track.kind)
            state.track = track
            state.task = create_task(record())

        if track.kind == "video":
            state.log_info("Received %s", track.kind)
            state.video_track = track
            state.video_task = create_task(record_video())

        @track.on("ended")
        async def on_ended():
            print("Track %s ended", track.kind)
            state.task.cancel()
            state.video_task.cancel()
            track.stop()

    # handle offer
    await state.pc.setRemoteDescription(offer)

    # send answer
    answer = await state.pc.createAnswer()
    print("answer", answer)
    await asyncio.sleep(0)
    await state.pc.setLocalDescription(answer)

    @state.pc.on("datachannel")
    async def on_datachannel(channel):
        state.log_info("DataChannel")
        state.response_player.channel = channel

        @channel.on("message")
        async def on_message(message):
            state.log_info("Received message on channel: %s", message)
            if message == "get_response":
                state.response_player.response_ready = True
            if message == "get_silence":
                state.response_player.response_ready = False
            if message == "start_recording":
                state.log_info("Start Recording")
                state.response_player.response_ready = False
                state.buffer = []
                state.recording = True
            if message == "stop_recording":

                state.log_info("Stop Recording")
                state.recording = False
                # state.task.cancel()
                # state.video_task.cancel()
                # state.track.stop()
                # state.response_player.stop()
                # state.video_track.stop()

            if message[0:7] == "preset:":
                preset = message[7:]
                state.log_info("Changed voice preset to %s", preset)
            if message[0:6] == "model:":
                model = message[6:]
                chain.set_model(model)
                state.log_info("Changed model to %s", model)
            if message[0:6] == "Human:":
                data = message[6:]
                await ai_request(data)



    async def transcribe_request_openai(data):
        response = None
        #transcription = whisper.transcribe(data)
        print("transcribe_request start")
        #使用openai stt
        buffuer = merge_frame(data)
        transcription = await stt.recognize(buffuer,state)
        print("Transcription is: %s", transcription)

        state.response_player.channel.send(f"Human: {transcription[0].text}")
        state.log_info(transcription[0].text)
        tmp_content = ''
        try:
            state.response_player.channel.send(f"AI: start-response")
            response =  chain.get_chain().invoke({"human_input": transcription[0].text})
            for txt in response:
                state.response_player.channel.send(f"AI: {txt}")
                tmp_content += txt
                print("response",txt)
            state.response_player.channel.send(f"AI: end-response")
            await asyncio.sleep(0)
            continue_to_synthesize = True
        except Exception as e:
            state.response_player.channel.send("AI: Error communicating with Ollama")
            state.response_player.channel.send(f"AI: {e}")
            state.response_player.channel.send("playing: response")
            state.response_player.channel.send("playing: silence")
            continue_to_synthesize = False
        return continue_to_synthesize, tmp_content


    async def ai_request(data):
        print("ai_request start",data)


        tmp_content = ''
        try:

            state.response_player.channel.send(f"AI: start-response")
            try:
                response =  chain.get_img_chain(data)
                await asyncio.sleep(0)
                for txt in response:
                    print("response", txt)
                    state.response_player.channel.send(f"AI: {txt}")
                    await asyncio.sleep(0)
                    tmp_content += txt

            except Exception as e:
                print("Transcription errer",e)
            state.response_player.channel.send(f"AI: end-response")

        except Exception as e:
            state.response_player.channel.send("AI: Error communicating with openai")
            state.response_player.channel.send(f"AI: {e}")
            state.response_player.channel.send("playing: response")
            state.response_player.channel.send("playing: silence")
    # 示例调用
    async def transcribe_request(data):
        print("transcribe_request start")
        #使用funasr stt
        buffuer = merge_frame(data)
        transcription = await stt.recognize(buffuer,state)

        if len(transcription.strip()) > 0:
            state.response_player.channel.send(f"Human: end-response")
        print("Transcription is: %s", transcription)
        tmp_content = ''
        seg_content = ''
        response=''
        try:

            state.response_player.channel.send(f"AI: start-response")
            try:
                response =  chain.get_img_chain(transcription,state.video_frame)
                await asyncio.sleep(0)
                for txt in response:
                    print("response", txt)
                    state.response_player.channel.send(f"AI: {txt}")
                    await asyncio.sleep(0)
                    tmp_content += txt
                    seg_content += txt
                    if is_ending_with_punctuation(seg_content):
                        print("response seg_content", seg_content)
                        await synthesize_response_edgs(seg_content[:-1],state)
                        seg_content = ''
            except Exception as e:
                print("Transcription errer",e)
            state.response_player.channel.send(f"AI: end-response")
            # await tts.synthesize(tmp_content, state)
            # state.response_player.track = None
            # state.response_player.response_ready = True
            # state.response_player.speeking = True
        except Exception as e:
            state.response_player.channel.send("AI: Error communicating with Ollama")
            state.response_player.channel.send(f"AI: {e}")
            state.response_player.channel.send("playing: response")
            state.response_player.channel.send("playing: silence")

    async def synthesize_response_edgs(response,state):
        await tts.synthesize(response, state)
        state.response_player.track = None
        state.response_player.response_ready = True
        state.response_player.speeking = True
    async def synthesize_response(response):
        if len(response.strip()) > 0:
            #state.response_player.channel.send(f"AI: {response}")
            #bark.synthesize(response,state.response_player.filename)
            print("synthesize_response start")
            await tts.synthesize(response,state.response_player.filename)
            print("synthesize_response done")
            state.response_player.track = None
            state.response_player.response_ready = True
        else:
            state.response_player.channel.send("playing: response")
            print(" synthesize_response playing: silence")
            state.response_player.channel.send("playing: silence")
        await asyncio.sleep(0)

    return web.Response(
        content_type="application/json",
        text=json.dumps(
            {"sdp": state.pc.localDescription.sdp, "type": state.pc.localDescription.type}
        ),
    )

async def on_shutdown(app):
    # close peer connections
    coros = [state.pc.close() for state in pcs]
    for state in pcs:
        deleteFile(state.filename)
    await asyncio.gather(*coros)


# https://gist.github.com/ultrafunkamsterdam/8be3d55ac45759aa1bd843ab64ce876d
def create_bg_loop():
    def to_bg(loop):
        asyncio.set_event_loop(loop)
        try:
            loop.run_forever()
        except asyncio.CancelledError as e:
            print('CANCELLEDERROR {}'.format(e))
        finally:
            for task in asyncio.all_tasks(loop):
                task.cancel()
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.stop()
            loop.close()

    new_loop = asyncio.new_event_loop()
    t = threading.Thread(target=to_bg, args=(new_loop,))
    t.start()
    return new_loop

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WebRTC AI ")
    parser.add_argument("--cert-file", help="SSL certificate file (for HTTPS)")
    parser.add_argument("--key-file", help="SSL key file (for HTTPS)")
    parser.add_argument(
        "--host", default="0.0.0.0", help="Host for HTTP server (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port", type=int, default=8089, help="Port for HTTP server (default: 8080)"
    )

    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)

    chain = Chain()


    if args.cert_file:
        ssl_context = ssl.SSLContext()
        ssl_context.load_cert_chain(args.cert_file, args.key_file)
    else:
        ssl_context = None

    app = web.Application()

    # 创建一个CORS配置
    # 配置 CORS
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })


    # 启动CORS中间件
    app.on_shutdown.append(on_shutdown)
    cors.add(app.router.add_post("/offer", offer))
    web.run_app(app, host=args.host, port=args.port, ssl_context=ssl_context)
