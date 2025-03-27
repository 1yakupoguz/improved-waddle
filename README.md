# 🚗 Object Tracker - Vehicle Detection and Counting System

The **object_track.py** script detects and tracks vehicles passing on the road. It identifies the center points of the vehicles and tracks their movement based on position changes. Each vehicle is assigned a unique **ID**, ensuring that the same vehicle is not counted multiple times. The system performs vehicle counting in different lanes categorized as **incoming, outgoing, and lanes 1, 2, 3, 4**.

## 📌 Features

- 📍 **Vehicle Detection**: Identifies passing vehicles in a video.
- 🔢 **Unique ID Tracking**: Prevents duplicate counting of the same vehicle.
- 🛣️ **Lane-Based Counting**: Categorizes vehicles into **incoming, outgoing, and lanes 1, 2, 3, 4**.
- 🎥 **Video Input**: Works with both live camera feed and pre-recorded videos.
- 📊 **Real-Time Analysis**: Tracks movement direction and vehicle flow.