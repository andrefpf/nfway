from pathlib import Path

import cv2


def read_qrcode(image_path: Path) -> str | None:
    img = cv2.imread(str(image_path))

    detector = cv2.QRCodeDetector()
    data, _, _ = detector.detectAndDecode(img)

    if not data:
        from qreader import QReader

        qreader = QReader()
        data, *_ = qreader.detect_and_decode(image=img)

    return data if data else None
