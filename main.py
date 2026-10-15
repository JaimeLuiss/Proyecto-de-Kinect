import os
import time
import urllib.request
import winsound
import cv2
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python.vision import HandLandmarker, HandLandmarkerOptions, RunningMode

# ================================================
# Configuración general
# ================================================
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
DEBOUNCE_SECONDS = 0.30

NOTE_FREQUENCIES = {
    "Do": 261.63,
    "Re": 293.66,
    "Mi": 329.63,
    "Fa": 349.23,
    "Sol": 392.00,
}

KEY_ORDER = ["Do", "Re", "Mi", "Fa", "Sol"]

JINGLE_BELLS = [
    "Mi", "Mi", "Mi", "Mi",
    "Mi", "Mi", "Mi", "Sol",
    "Do", "Re", "Mi", "Fa",
    "Fa", "Fa", "Fa", "Fa",
    "Mi", "Mi", "Mi", "Mi",
    "Re", "Re", "Mi", "Re",
    "Sol", "Sol", "Sol",
    "Mi", "Mi", "Mi", "Mi",
    "Do", "Re", "Mi", "Fa",
    "Fa", "Fa", "Fa", "Fa",
    "Mi", "Mi", "Mi", "Mi",
    "Re", "Re", "Mi", "Re",
    "Sol"
]

# ================================================
# Audio con winsound
# ================================================
def play_note(note_name: str, duration_ms: int = 200):
    frequency = int(NOTE_FREQUENCIES[note_name])
    winsound.Beep(frequency, duration_ms)


def play_demo_melody():
    for note in JINGLE_BELLS:
        play_note(note, 180)
        time.sleep(0.09)


# ================================================
# Teclado virtual grande
# ================================================
def build_keys():
    keys = []
    margin_x = 60
    bottom_gap = 40
    key_h = int(WINDOW_HEIGHT * 0.34)
    key_y = WINDOW_HEIGHT - key_h - bottom_gap
    total_width = WINDOW_WIDTH - (2 * margin_x)
    key_w = total_width / len(KEY_ORDER)

    for i, note_name in enumerate(KEY_ORDER):
        x = int(margin_x + i * key_w + 10)
        width = int(key_w) - 20
        rect = (x, key_y, width, key_h)
        keys.append({
            "name": note_name,
            "freq": NOTE_FREQUENCIES[note_name],
            "rect": rect,
            "pressed": False,
            "touching_by_hand": set(),
            "last_trigger_by_hand": {},
        })
    return keys


KEYS = build_keys()


def point_in_rect(x, y, rect):
    rx, ry, rw, rh = rect
    return rx <= x <= rx + rw and ry <= y <= ry + rh


# ================================================
# Interfaz visual
# ================================================
def draw_background(frame):
    cv2.rectangle(frame, (0, 0), (WINDOW_WIDTH, WINDOW_HEIGHT), (16, 18, 24), -1)
    cv2.rectangle(frame, (30, 20), (WINDOW_WIDTH - 30, 120), (28, 34, 48), -1)
    cv2.rectangle(frame, (30, 20), (WINDOW_WIDTH - 30, 120), (100, 180, 255), 2)

    cv2.putText(frame, "Piano virtual con manos", (60, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 1.3, (255, 255, 255), 2)

    cv2.putText(frame, "M = melodía • Q = salir", (900, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (180, 210, 255), 2)


def draw_keyboard(frame):
    for key in KEYS:
        x, y, w, h = key["rect"]
        if key["pressed"]:
            color = (0, 220, 120)
            border = (70, 255, 180)
        else:
            color = (96, 142, 255)
            border = (255, 255, 255)

        cv2.rectangle(frame, (x, y), (x + w, y + h), color, -1)
        cv2.rectangle(frame, (x, y), (x + w, y + h), border, 4)

        cv2.putText(frame, key["name"], (x + 30, y + h - 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.3, (255, 255, 255), 2)


# ================================================
# Detección de manos con MediaPipe Tasks API
# ================================================
MODEL_URL = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
MODEL_PATH = os.path.join(os.path.dirname(__file__), "hand_landmarker.task")


def ensure_model_downloaded():
    if not os.path.exists(MODEL_PATH):
        print("Descargando modelo de MediaPipe...")
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
        print("Modelo listo.")


ensure_model_downloaded()

hand_landmarker = HandLandmarker.create_from_options(
    HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=MODEL_PATH),
        running_mode=RunningMode.VIDEO,
        num_hands=2,
        min_hand_detection_confidence=0.6,
        min_hand_presence_confidence=0.5,
        min_tracking_confidence=0.5,
    )
)


def process_hand(frame, landmarks, hand_id):
    h, w, _ = frame.shape

    index_tip = landmarks[8]
    x = int(index_tip.x * w)
    y = int(index_tip.y * h)
    cv2.circle(frame, (x, y), 12, (0, 255, 255), -1)
    cv2.putText(frame, f"Mano {hand_id + 1}", (x + 18, y - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

    now = time.time()

    for key in KEYS:
        key["pressed"] = False

    for key in KEYS:
        if point_in_rect(x, y, key["rect"]):
            if hand_id not in key["touching_by_hand"]:
                key["touching_by_hand"].add(hand_id)
                last = key["last_trigger_by_hand"].get(hand_id, 0.0)
                if now - last >= DEBOUNCE_SECONDS:
                    play_note(key["name"], 180)
                    key["last_trigger_by_hand"][hand_id] = now
            key["pressed"] = True
        else:
            key["touching_by_hand"].discard(hand_id)


# ================================================
# Cámara
# ================================================
def open_camera():
    for index in (0, 1, 2, 3):
        cap = cv2.VideoCapture(index)
        if cap.isOpened():
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, WINDOW_WIDTH)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, WINDOW_HEIGHT)
            return cap
        cap.release()
    return None


# ================================================
# Bucle principal
# ================================================
def main():
    cap = open_camera()
    if cap is None:
        print("No se pudo abrir la cámara. Comprueba que esté conectada y disponible.")
        return

    print("Proyecto ejecutándose.")
    print("Controles: 'M' = melodía • 'Q' = salir")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("No se pudo capturar el frame de la cámara.")
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        timestamp_ms = int(time.time_ns() / 1_000_000)
        results = hand_landmarker.detect_for_video(rgb, timestamp_ms)

        draw_background(frame)
        draw_keyboard(frame)

        if results.hand_landmarks:
            for hand_id, hand_landmarks in enumerate(results.hand_landmarks):
                process_hand(frame, hand_landmarks, hand_id)

        cv2.putText(frame, "Toca la nota con el dedo índice", (60, 160),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 220, 255), 2)

        cv2.imshow("Piano Virtual - Jingle Bells", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break
        elif key == ord('m'):
            play_demo_melody()

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
