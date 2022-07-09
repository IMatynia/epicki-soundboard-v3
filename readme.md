# Epicki soundboard V3

## Features

- Playing audio on **2 devices at once** (the default device and a custom one, like a virtual cable)
- Support for adding sounds with **youtube-dl** from a link to the media
- Indirect support for **all FFMPEG-supported media formats** (automatic conversion to ogg)
- Ability to speak all **google TTS** languages, as well as **translate**. This effectively gives you the ability to speak a different language! (this works one way however, since there is no speech recognistion and translation (yet?))
- Maximum of **256 pages** of hotkeys (if thats not enough you can edit it in the code)

## How to run

Windows might think this app is a keylogger. To an extent it is, if you consider hotkeys as a form key logging... Windows is complaining because I use pynput library and its keyboard listener. I need it for hotkeys and key scanning (src/hotkey_listener.py and src/hotkey_scanner.py).

After installing dependencies:

```sh
> py main.py
```

## Dependencies

App is written in python, so you need [Python 3.8+](https://www.python.org/downloads/) :I

Additionally, you need these python libraries installed on your system:

- [PySide2](https://pypi.org/project/PySide2/) - the GUI
- [sounddevice](https://pypi.org/project/sounddevice/) - Audio playback
- [soundfile](https://pypi.org/project/SoundFile/) - Data for audio playbacks
- [pynput](https://pypi.org/project/pynput/) - Keyboard hooks
- [gTTS](https://pypi.org/project/gTTS/) - Text to speech
- [translators](https://pypi.org/project/translators/) - Prompt translation
- [numpy](https://pypi.org/project/numpy/)
- [bitarray](https://pypi.org/project/bitarray/)

### Optional dependencies

Having these programs in path is necessary for some functionalities

- [FFMPEG](https://ffmpeg.org/) - necessary for conversion of any media to ogg format, TTS and youtube-dl
- [youtube-dl](https://youtube-dl.org/) (or any other fork like yt-dlp) - necessary for youtube-dl downloads

## How to use

Quick tips:
- There exist hotkeys for:
    - Switching pages (Page Up/ Page Down)
    - Openning TTS manager ( ']' )
- Edit settings under Data->Edit settings

<!-- Dialog windows and explanations -->

## Known limitaions

- Sometimes, for reasons beyond my understanding, some key combinations are not registered.
- Audio playback is only supported on devices with hostapi == 0 and >2 output channels and 0 input channels. This might exclude your virtual cable or device (go ahead and change it in the code if you want (src\audio_devices.py:37))
- *Only* 256 hotkey pages are supported (go ahead and change it in the code if you want (src\audio_hotkey.py:94))