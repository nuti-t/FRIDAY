from tensorflow_core.python.keras.layers import Dropout
import librosa
import os
import numpy as np

training_log = []
train_path = 'Dataset/MS-SNSD/clean_train/'
audio_file = os.listdir(train_path)
for file in audio_file:
    signal , sample_rate = librosa.load(str(train_path + file))
    power_squared = np.abs(librosa.stft(signal)) ** 2
    log_spectrum = librosa.feature.melspectrogram(S = power_squared)
    training_log = np.array(log_spectrum)
    print("Converted file {}".format(file))
print(training_log)
print("Shape {}". format(training_log.shape))
print("Everything is ready")
