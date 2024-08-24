import mediapipe as mp
import time
from tools import add_text_and_timing, draw_circles, normalize_coordinates
import cv2 as cv
import easyocr


# Detects the finger tip and track its movement
class FingerTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.mp_drawing = mp.solutions.drawing_utils


    def track_finger(self, image, previous_coordinates):
        image = cv.flip(image, 1)
        results = self.hands.process(cv.cvtColor(image, cv.COLOR_BGR2RGB))

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for point in hand_landmarks.landmark:
                    x, y = int(point.x * image.shape[1]), int(point.y * image.shape[0])
                    cv.circle(image, (x, y), 5, (0, 0, 255), -1)

                    if point == hand_landmarks.landmark[8]:
                        print(f"Index Finger Tip: ({x}, {y})")
                        previous_coordinates.append((x, y))

                        # Track the coordinates of the index finger tip
                        index_finger_tip_x = x
                        index_finger_tip_y = y
                        # Draw a circle at the index finger tip
                        cv.circle(img=image, center=(index_finger_tip_x, index_finger_tip_y), radius=10, color=(150, 255, 20), thickness=-1)

                self.mp_drawing.draw_landmarks(image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

        return image, previous_coordinates[-30:]
    
    def close(self):
        self.hands.close()


def main():
    cap = cv.VideoCapture(0)
    finger_tracker = FingerTracker()

    # Initialize variables for timing
    start_time = time.time()
    is_processing = False

    previous_coordinates = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame, previous_coordinates = finger_tracker.track_finger(frame, previous_coordinates)

        frame, start_time, is_processing = add_text_and_timing(frame, start_time, is_processing)

        if not is_processing:
            frame = draw_circles(frame, previous_coordinates)
        else:
            previous_coordinates = []

        normalized_coordinates = normalize_coordinates(frame, previous_coordinates)
        print(normalized_coordinates)
            
        
        cv.imshow("Finger Tracker", frame)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    finger_tracker.close()
    cap.release()
    cv.destroyAllWindows()



if __name__ == "__main__":
    main()
