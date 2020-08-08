# Remote controller GUI
## Introduction
The Remote Controller GUI is design for controlling the robot. I'm new to PyQt5, so it's

## Functions
It's currently has two main functions:
1. RTMP video streaming.
2. Send keypress events to control the robot through HTTP.

## Requirements
The Remote Controller requires `OpenCV` to deal with streaming video, `PyQt5` to build the GUI and `requests` to send events to the robot. It's build in <strong><font color=#ff0000>`Python 3.8.4 64 bits`</font></strong>

You can run the following instruction in the CMD or PowerShell to install them:

```
pip install -r requirements.txt
```


## How to use it ?
As you install all packages, just run `GUI.py`. You can press `F11` to enter full-screen mode. I will enlarge the size of labels in the future version.

1. RTMP server URL: URL to connect to the streaming video.
2. Terrain data source: URL to connect to the Lidar video.
3. Backend server: URL to send instructions to the robot.

![](https://i.imgur.com/uBPDhXP.png)


You have to connect to the robot, or the following keypress won't have any response.
| Keyboard Instructions | Function      |
| --------------------- | ------------- |
| Ctrl + Q              | Quit the GUI  |
| Upwards               | Go Forward    |
| Downwards             | Go Backward   |
| Leftwards             | Go Leftwards  |
| Rightwards            | Go Rightwards |
| W                     | Stretch       |
| S                     | Shrink        |




