from funasr import AutoModel

chunk_size = [0, 10, 5] #[0, 10, 5] 600ms, [0, 8, 4] 480ms
encoder_chunk_look_back = 4 #number of chunks to lookback for encoder self-attention
decoder_chunk_look_back = 1 #number of encoder chunks to lookback for decoder cross-attention

model = AutoModel(model="iic/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch")
model_prnc = AutoModel(model="ct-punc")
import soundfile



import librosa
speech, sample_rate = soundfile.read("./test.wav")
speech, sample_rate = librosa.load('./test.wav', sr=None)
print("s1",sample_rate)
dst_sig = librosa.resample(speech,orig_sr=sample_rate,target_sr=16000)
soundfile.write("./my.wav",dst_sig,16000)
speech, sample_rate = soundfile.read("./my.wav")
print("s2",sample_rate)

chunk_stride = chunk_size[1] * 960 # 600ms

cache = {}
total_chunk_num = int(len((speech)-1)/chunk_stride+1)
for i in range(total_chunk_num):
    speech_chunk = speech[i*chunk_stride:(i+1)*chunk_stride]
    is_final = i == total_chunk_num - 1
    print("is_final",is_final)
    res = model.generate(input=speech_chunk, cache=cache, is_final=is_final, chunk_size=chunk_size, encoder_chunk_look_back=encoder_chunk_look_back, decoder_chunk_look_back=decoder_chunk_look_back)
    if is_final:
        res = model_prnc.generate(input=res[0]['text'])
    print(res)
