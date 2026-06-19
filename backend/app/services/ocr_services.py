from paddleocr import PaddleOCR
import numpy as np
import cv2

gender_dict = {
    "M": 0, "F": 1, "Other": 2
}

def convert_to_opencv(contents: bytes):
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return image

def process_image(image):
    ocr = PaddleOCR(use_angle_cls=True, lang='en')
    result = ocr.ocr(image, cls=True)
    return result

def get_locations(ocr_result):
    locations = []
    for line in ocr_result[0]:

        box = line[0]
        text = line[1][0]
        confidence = line[1][1]

        # top-left corner of the box
        x = box[0][0]
        y = box[0][1]

        locations.append({
            "text": text,
            "x": x,
            "y": y,
            "confidence": confidence
        })
    return locations

def find_value_below(locations, label_keyword, x_tolerance=30, max_y_distance=120):
    # find wanted label
    for item in locations:
        if label_keyword.lower() in item["text"].lower():

            label_x = item["x"]
            label_y = item["y"]

            best_candidate = None
            best_distance = float("inf")

            # find block under label
            for other in locations:

                # ignore self
                if other == item:
                    continue

                x_diff = abs(other["x"] - label_x)
                y_diff = other["y"] - label_y

                if (
                    y_diff > 0 and
                    y_diff < max_y_distance and
                    x_diff < x_tolerance
                ):

                    # keep closest
                    if y_diff < best_distance:
                        best_distance = y_diff
                        best_candidate = other

            return best_candidate
    return None

def extract_user_profile(locations):
    profile = {}
    surname = find_value_below(locations, "NOM")['text'].capitalize()
    first_name = find_value_below(locations, "Prenoms")['text']
    dob = find_value_below(locations, "DATE DE NA")['text']
    gender_string = find_value_below(locations, "SEXE")['text']

    name = f"{surname} {first_name}"
    email = f"{first_name.lower()}.{surname.lower()}@example.com"
    age = 2026 - int(dob[4:8])
    gender = gender_dict[gender_string]
    
    return {
        "name": name,
        "email": email,
        "age": age,
        "gender": gender
    }