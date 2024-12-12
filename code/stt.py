import os
import time
import subprocess

def get_audio(length=5):
    os.system(f'arecord --device=hw:2,0 --format S16_LE --rate 48000 --duration={length} test.wav')
    '''print('start')
    recording = subprocess.Popen([f'arecord --device=hw:2,0 --format S16_LE --rate 48000 test.wav'], shell=True)
    input()
    recording.terminate()
    print('finished recording')'''

def translate():
    try:
        os.system('vosk-transcriber -i test.wav -o test.txt')
        f = open('test.txt', 'r').read().strip('/n')
        return(f)
    except:
        print('error')
        return None
        
def get_speech():
    get_audio()
    time.sleep(2)
    text = translate()
    return text

if __name__ == '__main__':
    while True:
        print(get_speech())
