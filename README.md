# PiCaApp
Raspberry Pi Camera App designed for small displays with preview and few buttons. Configurable through files and API for more advanced options.

I'm new to python, and even newer to the Pi Camera, so any help will be appreciated.

## Features in development and planned

* Designed for small embedded displays (ie. HyperPixel 4) - will likely need someone to test and configure for different sized displays
* Configurable UI
* API for full camera control (will later develop a web app for this)
* Support for the different camera modules - will likely need someone to test and configure for the other V1 and V2 Cameras
* Point and shoot mode - a mode that makes preview fullscreen and clicking will take a picture, long-clicking will take sequence of pictures or video
* Grid overlay in preview

## Notes on camera preview and GUI
With the Pi Camera the preview is tied to the camera resolution. This means that when taking a picture of a certain resolution, the preview may change if the res of the picture is different than the preview, but we change it back after the picture is taken. This also means the preview frame rate will depend on the set camera resolution.

The `gui_config.json` and `camera_config.json` files have settings to set these values(later will allow configuring from GUI and API). This means that in order for the GUI to be properly set, it's best to ensure the camera res and preview size are the same aspect ratio. Ideally, if the videos and pictures you're going to take are of different aspect ratios(ie. video in 16:9 and pictures in 4:3), then ideally the GUI configurations should be ready to handle both.

I'm still developing the GUI but the idea is to try and minimize these issues when it's ready. When taking pictures or video, the max width or max height of the preview should never come in the way of any part of the interface while always allowing you to see the full preview.

## Camera modules and displays
I'm developing this on Raspberry Pi 4, an HyperPixel 4(resoluton of 800x480) and the HQ Camera module. My idea is to make the GUI completely configurable to allow different sized displays and for the different modules but I might need help for both. 

The `camera_config.json` file will have all the different capabilities according to the module, along with other settings. Sample configs for other modules will be stored in `/configs/modules`.

The `gui_config.json` file will have all the settings for the interface elements. This includes settings for the preview size and position, and all the buttons with their respective position, size and action(ie. capture, switch to video/photo, some selections for choosing res, AWB, ISO, etc.). Sample configs for specific resolutions or displays will be stored in `/configs/displays`.
