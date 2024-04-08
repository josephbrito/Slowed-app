import os
import soundfile as sf
import subprocess
import time
import shutil

from pydub import AudioSegment
from AudioFusion import Fusion
from pedalboard import Pedalboard
from pedalboard import Reverb
from pedalboard import Convolution

def main(path):
    try:
        #allowed formats
        ext_allowed = ['.mp3', '.wav']

        # tsp = timestamp
        tsp = str(time.time()).split('.')[0]

        path_song = path

        song_name = os.path.basename(path_song).split('.')[0] + "-" + tsp

        file_type = os.path.splitext(path_song)[1]

        if file_type not in ext_allowed:
            print("Formato não permitido. Abortando sistema!")
            return None

        slow_or_fast = '-slowed'

        # output folder
        destination = 'output/'

        # file .mp3 to .wav
        if file_type == ".mp3":
            dst = os.path.join(destination, song_name + '.wav')
            subprocess.call(['ffmpeg', '-i', path_song, dst])
            song_path = dst
        else:
            shutil.copy(path_song, os.path.join(destination, song_name + file_type))
            song_path = os.path.join(destination, song_name + file_type)

        song = Fusion.loadSound(song_path)
        song = Fusion.effectSlowed(song, speedMultiplier=0.80)
        Fusion.saveSound(song, os.path.join(destination, song_name))

        reverb = Pedalboard([
            Convolution(song_path, 0.10),
            Reverb(room_size=0.30, wet_level=.40, dry_level=.40),
        ])

        total_steps = 3  # number of steps

        print("Carregando...")

        # Step 1: Set effects pedalboard
        print_progress(1, total_steps)

        audio_3, sample_rate_3 = sf.read(song_path)
        all_effects = reverb(audio_3, sample_rate_3)
        sf.write(song_path, all_effects, sample_rate_3)

        # Step 2 File to .mp3
        print_progress(2, total_steps)

        final_wav = AudioSegment.from_wav(song_path)
        final_wav.export(os.path.join(destination, song_name + slow_or_fast + ".mp3"), format="mp3")

        # Step 3: Clear temp files
        print_progress(3, total_steps)

        os.remove(song_path)
        os.remove(os.path.join(path))

        print("\nConcluído!")

        return os.path.join(destination, song_name + slow_or_fast + ".mp3")
    except Exception as e:
        print('Ocorreu um erro: \n', e)

def print_progress(step, total):
    percentage = (step / total) * 100
    progress_bar = '[' + '=' * int(percentage / 10) + ' ' * (10 - int(percentage / 10)) + ']'
    print(f"\rProgresso: {percentage:.2f}% {progress_bar}", end='', flush=True)

if __name__ == '__main__':
    main()