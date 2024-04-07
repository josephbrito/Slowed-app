import os
import soundfile as sf
import subprocess
import time
import shutil

import pyrubberband as prband

from pydub import AudioSegment

from AudioFusion import Fusion
from pedalboard import Pedalboard
from pedalboard import Reverb
from pedalboard import Convolution
from pedalboard import PitchShift

def main(path):
    try:
        #allowed formats
        ext_allowed = ['.mp3', '.wav']

        # tsp = timestamp
        tsp = str(time.time()).split('.')[0]

        path_song = path

        song_name = path_song.split('.')[-2]
        song_name = song_name.split('/')[-1] + "-" + tsp

        file_type = "." + path_song.split('.')[-1]

        exists = file_type in ext_allowed

        if not exists:
            print("Format not allowed. Aborting system!")
            return None

        slow_or_fast = '-slowed'

        # Default output
        destination = 'output/'

        # Song to wav file if file_type == '.mp3'
        if (file_type == ".mp3"):
            dst = destination + song_name + '.wav'
            subprocess.call(['ffmpeg', '-i', path_song, dst ])
            file_type = ".wav"
            song_path = destination + song_name.replace('/', '') + file_type
        elif (file_type == ".wav"):
            shutil.copy(path_song, destination + song_name.replace('/', '') + file_type)
            song_path = destination + song_name.replace('/', '') + file_type

        song = Fusion.loadSound(song_path)
        song = Fusion.effectSlowed(song, speedMultiplier=0.80)

        Fusion.saveSound(song, destination + song_name.replace('/', ''))

        reverb = Pedalboard([
            Convolution(song_path, 0.10),
            Reverb(room_size=0.30, wet_level=.40, dry_level=.40),
        ])

        total_steps = 5  # Número total de etapas

        print("Loading...")

        # Step 1: Load and process audio
        print_progress(1, total_steps)

        audio, sample_rate = sf.read(song_path)
        tempo_shift = prband.time_stretch(audio, sample_rate, 100/100.0)
        sf.write(destination + song_name+slow_or_fast+".wav", tempo_shift, sample_rate, format="wav")

        # Step 2: Shift de pitch
        print_progress(2, total_steps)

        audio_2, sample_rate_2 = sf.read(song_path)
        pitch_shift = prband.pitch_shift(audio_2, sample_rate_2, 100/100.0)
        sf.write(destination + song_name+slow_or_fast+".wav", pitch_shift, sample_rate_2, format="wav")

        # Step 3: pedalboard effects
        print_progress(3, total_steps)

        audio_3, sample_rate_3 = sf.read(song_path)
        all_effects = reverb(audio_3, sample_rate_3)
        sf.write(song_path, all_effects, sample_rate_3)

        # Step 4: to mp3 file
        print_progress(4, total_steps)

        final_wav = AudioSegment.from_wav(song_path)
        final_wav.export(destination + song_name+slow_or_fast+".mp3")

        # Step 5: clear temp files
        print_progress(5, total_steps)

        os.remove(song_path)
        os.remove(destination + song_name + slow_or_fast + ".wav")
        os.remove(path)

        print("\nFinished!")

        return destination + song_name + slow_or_fast + ".mp3"
    except Exception as e:
        print('An error occured: \n', e)
    

def print_progress(step, total):
    percentage = (step / total) * 100
    progress_bar = '[' + '=' * int(percentage / 10) + ' ' * (10 - int(percentage / 10)) + ']'
    print(f"\rProgress: {percentage:.2f}% {progress_bar}", end='', flush=True)


def printUsage():
    print("""Usage: python main.py [input_song_path] [output_song_path]

#Options:
the output slowed reverb file is optional [default is in output folder]
""")

if __name__ == '__main__':
    main()