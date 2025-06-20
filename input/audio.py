import pyaudio
import wave
import sys

def getHardwareSpecs(p):
    print("\nAvailable Input Devices:")
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if info['maxInputChannels'] > 0:
            print(f"Device {i}: {info['name']}")
            print(f"  Sample Rate: {info['defaultSampleRate']}")
            print(f"  Max Input Channels: {info['maxInputChannels']}\n")

def makeFormat():
    return {
        'rate': 48000, # based on input channel
        'format': pyaudio.paInt16,
        'channels': 1,  # mono
        'frames_per_buffer': 2048
    }

def recordClip(p, audio_format, DEVICE_INDEX, seconds):
    try:
        stream = p.open(
            format=audio_format['format'],
            channels=audio_format['channels'],
            rate=audio_format['rate'],
            input=True,
            input_device_index=DEVICE_INDEX,
            frames_per_buffer=audio_format['frames_per_buffer']
        )
    except Exception as e:
        print(f"Failed to open audio stream: {e}")
        p.terminate()
        sys.exit(1)

    print(f"Recording Started - {seconds} Seconds")
    frames = []

    try:
        for _ in range(0, int(audio_format['rate'] / audio_format['frames_per_buffer'] * seconds)):
            data = stream.read(audio_format['frames_per_buffer'], exception_on_overflow=False)
            frames.append(data)
    except Exception as e:
        print(f"Error during recording: {e}")

    stream.stop_stream()
    stream.close()
    p.terminate()

    return frames

def saveClip(p, audio_format, frames):
    output_filename = "recording.wav"
    with wave.open(output_filename, 'wb') as wf:
        wf.setnchannels(audio_format['channels'])
        wf.setsampwidth(p.get_sample_size(audio_format['format']))
        wf.setframerate(audio_format['rate'])
        wf.writeframes(b''.join(frames))

    print(f"Saved recording to '{output_filename}'")


def main():
    p = pyaudio.PyAudio()
    #getHardwareSpecs(p)

    DEVICE_INDEX = 9  # Uncomment getHardwareSpecs to see available input devices
                    # Update DEVICE_INDEX & makeFormat parameters accordingly.

    audio_format = makeFormat()
    frames = recordClip(p, audio_format, DEVICE_INDEX, 3)
    saveClip(p, audio_format, frames)


if __name__ == "__main__":
    main()


