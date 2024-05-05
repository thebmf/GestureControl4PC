import cv2
import numpy as np
import mediapipe as mp
import math
import pyautogui
# from pynput.mouse import Controller
# import pydirectinput

class HandDetector():
    def __init__(self, mode = False, max_hands = 2, compl = 1, detectionCon = 0.5, trackCon = 0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.compl = compl
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.max_hands, self.compl, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

    def find_hands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        
        return img
    
    def find_position(self, img, handNo = 0, draw = True):
        xList, yList, bbox = [], [], []
        self.lmList = []

        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                xList.append(cx)
                yList.append(cy)

                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
                
            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            bbox = xmin, ymin, xmax, ymax

        return self.lmList, bbox
    
    def fingers_up(self):
        fingers = []
        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range(1, 5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)    
        return fingers
    
    def find_distance(self, p1, p2, img, draw = True, r = 10, t = 2):
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)

        return length, img, [x1, y1, x2, y2, cx, cy]

def setup_camera(width=800, height=600):
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    return cap

def get_cursor_position(x, y, frame, screen_width, screen_height):
    x = np.interp(x, (frame, Cam_width-frame), (0, screen_width))
    y = np.interp(y, (frame, Cam_height-frame), (0, screen_height))
    return x, y

def smooth_movement(cloc, ploc, new_loc, smoothing):
    return ploc + (new_loc - ploc) / smoothing

Cam_width, Cam_height = 800, 600
Screen_width, Screen_height = pyautogui.size()
frame, smoothing = 75, 1
previous_location = (0, 0)
detector = HandDetector(max_hands=1)

cap = setup_camera(Cam_width, Cam_height)

while True:
    success, img = cap.read()
    if not success:
        continue
    
    img = detector.find_hands(img)
    lmList, bbox = detector.find_position(img)
    
    if lmList:
        index_finger = lmList[8][1:]
        middle_finger = lmList[12][1:]
        fingers_up = detector.fingers_up()

        if fingers_up[1] and not fingers_up[2]:
            cv2.rectangle(img, (frame, frame), (Cam_width - frame, Cam_height - frame), (0, 0, 255), 2)
            cursor_x, cursor_y = get_cursor_position(index_finger[0], index_finger[1], frame, Screen_width, Screen_height)
            current_location = (
                smooth_movement(previous_location[0], previous_location[0], cursor_x, smoothing),
                smooth_movement(previous_location[1], previous_location[1], cursor_y, smoothing)
            )
            pyautogui.moveTo(Screen_width - current_location[0], current_location[1])
            cv2.circle(img, index_finger, 10, (255, 0, 255), cv2.FILLED)
            previous_location = current_location

        if fingers_up[1] and fingers_up[2]:
            length, img, line_info = detector.find_distance(8, 12, img)
            if length < 31:
                cv2.circle(img, (line_info[4], line_info[5]), 10, (0, 255, 0), cv2.FILLED)
                pyautogui.click()

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()