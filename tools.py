import time
import cv2 as cv

def add_text_and_timing(frame, start_time, is_processing):
    recording_duration = 3  # Duration of recording in seconds
    processing_duration = 1  # Duration of processing in seconds

    elapsed_time = time.time() - start_time
    #print(f"{elapsed_time} and {is_processing}")

    if (elapsed_time <= recording_duration) and not is_processing:
        is_processing = False
    elif (elapsed_time <= recording_duration + processing_duration):
        is_processing = True
    else:
        start_time = time.time()
        is_processing = False
    
    # Draw text on the frame
    if is_processing:
        cv.putText(frame, "Processing", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    else:
        cv.putText(frame, "Recording", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    return frame, start_time, is_processing


def draw_circles(frame, coordinates):
    for coord in coordinates:
        cv.circle(frame, coord, 5, (0, 0, 255), -1)
    return frame


# Normalize coordinates to a range of 0 to 1
def normalize_coordinates(frame, coordinates):
    normalized_coordinates = []
    for coord in coordinates:
        x = coord[0] / frame.shape[1]
        y = coord[1] / frame.shape[0]
        normalized_coordinates.append((x, y))
    return normalized_coordinates
    