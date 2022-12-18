import os
duration = 0.1 # seconds
freq = 100  # Hz
os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))