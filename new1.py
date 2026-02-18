from ultralytics import YOLO
import cv2 

model= YOLO('yolov8n.pt')

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    
    results= model(frame)
    
    annotated_frame = results[0].plot()
    annotated_frame =cv2.resize(annotated frame, (1400,580))
    cv2.imshow('YOLO Object Detection', annotated_frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# release resources
cap.release()
cv2.destroyAllWindows()