# Epicki soundboard V3
![logo](https://i.imgur.com/D5WVli0.png)
![intro image](https://i.imgur.com/Hf7BZNO.png)
## Features

- Playing audio on **2 devices at once** (the default device and a custom one, like a virtual cable)
- Support for adding/playing sounds from:
    - **youtube-dl** (or your fork of choice, configurable in the settings)
    - **any local media** file containing sound (via ffmpeg)
    - audio sources from the **internet** (downloading a file via http)
    - speak any language available in **google TTS** - including built in **translation** helper

## TODO
- [x]  use a package manager - uv
- [x] prepare UI generation scripts - just
- [ ] audiolab for audio processing
- [ ] better youtube-dl support (set custom yt-dlp path)
- [ ] better configuration support -> switch to using toml, configurable folders
- [ ] page number as an input field
- [ ] allow user to choose audio api

## How to use

Quick tips:
- There exist hotkeys for:
    - Switching pages (Page Up/ Page Down)
    - Openning TTS manager ( ']' )
- Edit settings under Data->Edit settings

<!-- Dialog windows and explanations -->

![dialog windows](https://i.imgur.com/tSqEz3L.png)

## Known limitaions

- Sometimes, for reasons beyond my understanding, some key combinations are not registered.
    - actually im pretty sure it depends on your keyboard: cheaper keyboard <=> less capacity for multiple key registering
- Audio playback is only supported on devices with hostapi == 0 and >2 output channels and 0 input channels. This might exclude your virtual cable or device (go ahead and change it in the code if you want (src\audio_devices.py:37))