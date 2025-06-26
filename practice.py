import cv2
from ultralytics import YOLO

model = YOLO('yolov8s.pt')
video_path = 'sample_video.mp4'
cap = cv2.VideoCapture(video_path)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    results = model(frame)
    for result in results:
        for box in result.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            label = result.names[cls_id]
            
            if label not in ('person','car') or conf < 0.4:
                continue 
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            
            color = (0, 255, 0) if label == 'person' else (0, 0, 255)
            
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, f'{label} {conf:.2f}', (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            
    cv2.imshow('YOLOv8 Detection', frame)

    key = cv2.waitKey(1)
    if key == 27:
        break
    
cap.release()

cv2.destroyAllWindows()