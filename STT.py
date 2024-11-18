from vosk import Model, KaldiRecognizer
import sounddevice as sd
import queue
import sys
import json

print("Display input/output devices")
print(sd.query_devices())

# get the samplerate - this is needed by the Kaldi recognizer
device_info = sd.query_devices(sd.default.device[0], 'input')
samplerate = int(device_info['default_samplerate'])

# display the default input device
print("===> Initial Default Device Number:{} Description: {}".format(sd.default.device[0], device_info))

# setup queue and callback function
q = queue.Queue()

def recordCallback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

# build the model and recognizer objects.
# download vosk-model-en-us-0.22 from https://alphacephei.com/vosk/models and name the file model
print("===> Build the model and recognizer objects.  This will take a few minutes.")
#replace the file path to where model is saved
model = Model(r"C:\Users\vahl_\Projects\STT\model")
recognizer = KaldiRecognizer(model, samplerate)
recognizer.SetWords(False)

print("===> Begin recording. Press Ctrl+C to stop the recording ")
try:
    with sd.RawInputStream(dtype='int16',
                           channels=1,

                           callback=recordCallback):
        while True:
            data = q.get()        
            if recognizer.AcceptWaveform(data):
                recognizerResult = recognizer.Result()
                # convert the recognizerResult string into a dictionary  
                resultDict = json.loads(recognizerResult)
                if not resultDict.get("text", "") == "":
                    print(recognizerResult)
                    #Print into text file most recent result
                    with open('test.txt', 'w') as f:
                        f.write(recognizerResult)
                        f.write('\n')
                else:
                    print("no input sound")

except KeyboardInterrupt:
    print('===> Finished Recording')
except Exception as e:
    print(str(e))
