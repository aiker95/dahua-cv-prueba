Scripts for analyzing video files using different algorithms and techniques.
-

####Capture.py
- Gets real time video from an IP camera using RTSP or HTTP. 
- Not recommended because it seems like there are some frames lost in streaming.

#### Motion.py
- Motion detection and tracking using OpenCV contours.
- Detects even the slightest movement, so it's not very accurate if you want specific object tracking.
