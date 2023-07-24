import numpy as np
import librosa as lib
import soundfile as sf

#実験環境
mic_num = 30
mic_dis = 5e-3
sound_speed = 340


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

data_length = len(original_data)

if data_length % 2 != 0:
    noise_data = np.append(noise_data,0.0)
    original_data = np.append(original_data,0,0)
    data_length = data_length + 1

#マイクロホンアレイ生成
mic_array = np.zeros((mic_num, data_length))

#到達音声代入
for i in range(mic_num):
    mic_array[i] = 