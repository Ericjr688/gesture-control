import cv2
import mediapipe
import pyautogui

camera = cv2.VideoCapture(0)
capture_hands = mediapipe.solutions.hands.Hands()
drawing_options = mediapipe.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
x1 = y1 = x2 = y2 = 0

while True:
    _, image = camera.read()
    H, W, _ = image.shape
    image = cv2.flip(image, 1)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    output_hands = capture_hands.process(rgb_image)
    all_hands = output_hands.multi_hand_landmarks

    if all_hands:
        for hand in all_hands:
            drawing_options.draw_landmarks(image, hand)
            one_hand_landmark = hand.landmark
            for id, lm in enumerate(one_hand_landmark):
                x = int(lm.x * W)
                y = int(lm.y * H)
                if id == 8:
                    mouse_x = int(screen_width * lm.x)
                    mouse_y = int(screen_height * lm.y)
                    cv2.circle(image, (x, y), 10, (0, 255, 0))
                    pyautogui.moveTo(mouse_x, mouse_y)
                    x1, y1 = x, y
                if id == 4:
                    cv2.circle(image, (x, y), 10, (0, 255, 0))
                    x2, y2 = x, y


        dist = y2 - y1
        if dist < 20:
            pyautogui.click()
    cv2.imshow("Hand movement video capture", image)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()