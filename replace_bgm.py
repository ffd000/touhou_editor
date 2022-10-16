# Prepare input audio file
# -vn -acodec pcm_s16le -ar 44100 -ac 2 output.wav

from os.path import exists
import wave

# wave data in thbgm.dat, loops in th<xx>.dat/thbgm.fmt
BGM_FILENAME = 'thbgm.dat'

class bgminfo:
    start_position = 0x1821BA30
    rel_loop = 0x00145E20
    rel_end = 0x01DBD790

class bgm:
    def __init__(self, filename: str = "thbgm.dat") -> None:
        self.filename = filename

class riff:
    FILE_NAME: str
    CHANNELS: int
    BITS: int
    SAMPLE: int
    _WAV_FILE: wave.Wave_write

    def __init__(self, fileName: str, data: bytes, channels=2, sample=44100, bits=16) -> None:
        self.FILE_NAME = fileName
        # self.PCM_DATA = data
        self.CHANNELS = channels
        self.SAMPLE = sample
        self.BITS = bits
        self._WAV_FILE = wave.open(fileName, 'wb')
        self._WAV_FILE.setnchannels(channels)
        self._WAV_FILE.setsampwidth(bits//8)
        self._WAV_FILE.setframerate(sample)
        self._WAV_FILE.writeframes(data)
        
    def write(self,bytesData: bytes) -> None:
        self._WAV_FILE.writeframes(bytesData)

    def close(self) -> None:
        self._WAV_FILE.close()

def replace_bgm():
    with open("thbgm.dat", "r+b") as bgm:
        bgm.seek(bgminfo.start_position, 0)

        wav_file = wave.open("track2.wav", 'rb')
        wav_bytes = wav_file.readframes(wav_file.getnframes())

        bgm.write(wav_bytes)
        wav_file.close()


def extract_wav():
    if not exists(BGM_FILENAME):
        raise FileNotFoundError(f'{BGM_FILENAME} not found')

    with open(BGM_FILENAME, 'rb') as bgmdat:
        # Main Header
        chunk_id = bgmdat.read(4)
        print(chunk_id)

        bgmdat.seek(bgminfo.start_position, 0)
        bytes = bgmdat.read(bgminfo.rel_end) # Read the entire length
        
        wav = riff("test.wav", bytes)
        bgmdat.seek(bgminfo.start_position+bgminfo.rel_loop, 0)
        loopBytes = bgmdat.read(bgminfo.rel_end - bgminfo.rel_loop)
        wav.write(loopBytes)
        wav.close()

if __name__ == '__main__':
    replace_bgm()