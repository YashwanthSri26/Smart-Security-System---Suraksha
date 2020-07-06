'''import pyaudio
import wave
import pyttsx3
import pandas as pd
import numpy
import csv
import signal
import os
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', 140)
engine.say('hey there . I am Suraksha speaking . May i know your name please?')
engine.runAndWait()
x=input("Enter your name in caps: ")
if x=='TARUN':
   speak=1
elif x=='YASHWANTH':
     speak=2
elif x=='RUPAKALI':
     speak=3
elif x=='NYMISH':
     speak=4
else:
    print("WARNING! UNAUTHORIZED ACCESS")
    engine.say("Warning! . unauthorized access  i repeat   unauthorized access")
    engine.runAndWait()
    os.kill(os.getppid(), signal.SIGHUP)
row=['/home/yashwanth/vc/output.wav',speak]
with open('/home/yashwanth/vc/cfg/test_list.csv', 'a') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(row)
csvFile.close()

engine.say(' hi '+ x )
print("---------------------AUTHRNTICATION REQUIRED!------------------------")
engine.say('  Authentication Required! . Please record Your voice for first step verification.')
engine.runAndWait()
engine.stop()
WAVE_OUTPUT_FILENAME ="output.wav"
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")
frames = []
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
print("* done recording")
stream.stop_stream()
stream.close()
p.terminate()
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
if x=='TARUN':
   speak=1
elif x=='YASHWANTH':
     speak=2
elif x=='RUPAKALI':
     speak=3
elif x=='NYMISH':
     speak=4
row=['/home/yashwanth/vc/output.wav',speak]
with open('/home/yashwanth/vc/cfg/test_list.csv', 'a') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(row)
csvFile.close()'''

import os
import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist, euclidean, cosine
from glob import glob

from model import vggvox_model
from wav_reader import get_fft_spectrum
import constants as c


def build_buckets(max_sec, step_sec, frame_step):
	buckets = {}
	frames_per_sec = int(1/frame_step)
	end_frame = int(max_sec*frames_per_sec)
	step_frame = int(step_sec*frames_per_sec)
	for i in range(0, end_frame+1, step_frame):
		s = i
		s = np.floor((s-7+2)/2) + 1  # conv1
		s = np.floor((s-3)/2) + 1  # mpool1
		s = np.floor((s-5+2)/2) + 1  # conv2
		s = np.floor((s-3)/2) + 1  # mpool2
		s = np.floor((s-3+2)/1) + 1  # conv3
		s = np.floor((s-3+2)/1) + 1  # conv4
		s = np.floor((s-3+2)/1) + 1  # conv5
		s = np.floor((s-3)/2) + 1  # mpool5
		s = np.floor((s-1)/1) + 1  # fc6
		if s > 0:
			buckets[i] = int(s)
	return buckets


# def get_embedding(model, wav_file, max_sec):
# 	buckets = build_buckets(max_sec, c.BUCKET_STEP, c.FRAME_STEP)
# 	signal = get_fft_spectrum(wav_file, buckets)
# 	embedding = np.squeeze(model.predict(signal.reshape(1,*signal.shape,1)))
# 	return embedding


# def get_embedding_batch(model, wav_files, max_sec):
# 	return [ get_embedding(model, wav_file, max_sec) for wav_file in wav_files ]


def get_embeddings_from_list_file(model, list_file, max_sec):
	buckets = build_buckets(max_sec, c.BUCKET_STEP, c.FRAME_STEP)
	result = pd.read_csv(list_file, delimiter=",")
	result['features'] = result['filename'].apply(lambda x: get_fft_spectrum(x, buckets))
	result['embedding'] = result['features'].apply(lambda x: np.squeeze(model.predict(x.reshape(1,*x.shape,1))))
	return result[['filename','speaker','embedding']]


def get_id_result():
	print("Loading model weights from [{}]....".format(c.WEIGHTS_FILE))
	model = vggvox_model()
	model.load_weights(c.WEIGHTS_FILE)
	model.summary()

	print("Processing enroll samples....")
	enroll_result = get_embeddings_from_list_file(model, c.ENROLL_LIST_FILE, c.MAX_SEC)
	enroll_embs = np.array([emb.tolist() for emb in enroll_result['embedding']])
	speakers = enroll_result['speaker']

	print("Processing test samples....")
	test_result = get_embeddings_from_list_file(model, c.TEST_LIST_FILE, c.MAX_SEC)
	test_embs = np.array([emb.tolist() for emb in test_result['embedding']])

	print("Comparing test samples against enroll samples....")
	distances = pd.DataFrame(cdist(test_embs, enroll_embs, metric=c.COST_METRIC), columns=speakers)

	scores = pd.read_csv(c.TEST_LIST_FILE, delimiter=",",header=0,names=['test_file','test_speaker'])
	scores = pd.concat([scores, distances],axis=1)
	scores['result'] = scores[speakers].idxmin(axis=1)
	scores['correct'] = (scores['result'] == scores['test_speaker'])*1. # bool to int

	print("Writing outputs to [{}]....".format(c.RESULT_FILE))
	result_dir = os.path.dirname(c.RESULT_FILE)
	if not os.path.exists(result_dir):
	    os.makedirs(result_dir)
	with open(c.RESULT_FILE, 'w') as f:
		scores.to_csv(f, index=False)



if __name__ == '__main__':
	get_id_result()
