import numpy as np
import librosa as lib
import soundfile as sf

#音声ファイル読み込み
noise_path = "sample_musics\akinoayumi.mp3"
original_path = "sample_musics\elegy.mp3"
noise_data, noise_rate = lib.load(noise_path)
original_data, original_rate = lib.load(original_path)

#データ長調整
if len(noise_data) < len(original_data):
    noise_data = np.pad(noise_data,(0,int(len(original_data) - len(noise_data))),mode = 'constant')
else:
    original_data = np.pad(original_data,(0,int(len(noise_data) - len(original_data))),mode = 'constant')


