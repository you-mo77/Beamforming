import numpy as np
import librosa as lib
import soundfile as sf
import PySimpleGUI as gui

#実験環境
mic_num = 30
mic_dis = 5e-3
sound_speed = 340
angle = 45 #degrees

#GUI
layout = [[gui.Text("Input original data's path")],
          [gui.Input(key = 'original_data',default_text = r"sample_musics\\akinoayumi.mp3")],
          [gui.Text("Input noise data's path")],
          [gui.Input(key = 'noise_data', default_text = 'sample_musics\elegy.mp3')],
          [gui.Button('Run')]]

window = gui.Window("beamforming test",layout)
while True:
    event, values = window.read()

    if event == 'Run':

        #音声ファイル読み込み
        noise_path = values['noise_data']
        original_path = values['original_data']
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
            original_data = np.append(original_data,0.0)
            data_length = data_length + 1



        #debug
        #for i in range(len(original_data)):
            #highest = 0
            #index = 0

            #if original_data[i] > highest:
                #highest = original_data[i]
                #index = i

        #print(highest)
        #print(index)
        ####結果####
        #2.739009e-07
        #2845439



        #マイクロホンアレイ生成
        mic_array = np.zeros((mic_num, data_length),dtype="float64")



        #到達音声代入(遅延込み雑音と対象音声代入)
        for i in range(mic_num):
            delaied_time = i * mic_dis * np.sin(angle * (np.pi / 180)) / sound_speed
            delaied_sample = noise_rate * delaied_time

        #print(delaied_time)
        #print(delaied_sample)

            mic_array[i] = original_data + np.roll(noise_data,int(delaied_sample))

        #マイク0に到達した音(遅延なしの雑音が入った音)
        sf.write("mic0_sound.wav",mic_array[0],original_rate)

        #遅延和実行(マイク数除算込み)
        for i in range(1,mic_num):
            mic_array[0] = mic_array[0] + mic_array[i]

        mic_array[0] = mic_array[0] / mic_num

        #結果出力
        sf.write("output.wav",mic_array[0],original_rate)
    
    if event == gui.WIN_CLOSED:
        break

window.close()