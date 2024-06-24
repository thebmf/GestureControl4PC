# GestureControl4PC

## GestureControl4PC is a Python project that allows you to control your computer's mouse using hand gestures. By utilizing a camera to track finger movements, the project enables intuitive and touch-free interaction with your computer. When the index and middle fingers are brought together, a mouse click is performed.

## Features

Hand Detection: Tracks hands and fingers using a camera.

Finger Recognition: Identifies specific fingers and their positions.

Mouse Movement: Controls the mouse pointer based on finger movements.

Click Detection: Performs mouse clicks when specific gestures are detected.

Customizable: Adjustable parameters for hand detection and tracking.

## Installation
To use GestureControl4PC, you'll need to install the required dependencies. You can do this using the requirements.txt file provided.

```
pip install -r requirements.txt
```
## Usage
To start controlling your computer with hand gestures:

1. Run the script
```
python gesture_control.py
```
2. Open the application window.

3. Point your webcam towards your hand.

4. Use your index finger to control the mouse cursor.

5. Touch your index finger and middle finger to perform a left click.

## Customization:
You can adjust the smoothing variable in the script to control the sensitivity of cursor movement.

Modify the click_distance threshold within the find_distance function to adjust the distance between your index and middle finger for click detection.
