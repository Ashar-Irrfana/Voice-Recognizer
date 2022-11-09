import speech_recognition as sr
from tkinter import filedialog
import os
import mpv


def my_log(loglevel, component, message):
    print('[{}] {}: {}'.format(loglevel, component, message))


if __name__ == "__main__":
    cur_idx = 0
    file_paths = filedialog.askopenfilenames(parent=None,
                                             initialdir=os.getcwd(),
                                             title="Select file(s) to play:",
                                             filetypes=[('MP4 video', '.mp4'),
                                                        ('Matroska video', '.mkv'),
                                                        ('MP3 audio', '.mp3'),
                                                        ('all files', '.*')
                                                        ])

    r = sr.Recognizer()
    r.dynamic_energy_threshold = True
    word = ""

    player = mpv.MPV(log_handler=my_log, ytdl=True,
                     input_default_bindings=True, input_vo_keyboard=True)
    player.play(file_paths[cur_idx])
    old_vol = 0

    with sr.Microphone() as mic:
        print("Calibrating silence.")
        r.adjust_for_ambient_noise(mic)

        while word != "exit":
            try:
                print("Speak:")
                audio = r.record(mic, duration=3)
                print("Done listening.")
                word = r.recognize_google(audio).lower()

                vol = player["volume"]
                if word == "play":
                    player['pause'] = False
                if word == "stop":
                    player['pause'] = True
                if word == "unmute":
                    player["volume"] = old_vol
                if word == "mute":
                    old_vol = player["volume"]
                    player["volume"] = 0
                if word == "higher":
                    player["volume"] = vol + 30
                if word == "down":
                    player["volume"] = vol - 30
                if word == "next":
                    cur_idx += 1
                    if cur_idx >= len(file_paths):
                        cur_idx = len(file_paths) - 1
                    player.play(file_paths[cur_idx])
                if word == "previous":
                    cur_idx -= 1
                    if cur_idx < 0:
                        cur_idx = 0
                    player.play(file_paths[cur_idx])
                print(word)
            except sr.UnknownValueError:
                pass
            except sr.WaitTimeoutError:
                print("out of time")
            except sr.RequestError as e:
                pass
