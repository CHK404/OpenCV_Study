import cv2
from ultralytics import YOLO

#YOLOv8 모델 로드
#yolov8s.pt는 사전에 학습된 경량 모델 파일
#처음 실행 시에 자동 다운
model = YOLO('yolov8s.pt')

#분석할 비디오 파일 경로 지정    
video_path = 'sample_video.mp4'

#openCV를 사용해서 비디오 파일 열기
cap = cv2.VideoCapture(video_path)

#무한 루프: 비디오 프레임을 한 장씩 읽으며 처리
while True:
    
    #cap.read()는 두 개 값을 반환:
    #ret - 프레임을 성공적으로 읽었으면 True, 아니면 False
    #frame - 읽은 프레임 이미지(배열)
    ret, frame = cap.read()
    
    #비디오의 끝에 도달하거나 프레임 읽기 실패 시 루프 종료
    if not ret:
        break
    
    #현재 프레임을 YOLO 모델에 입력하여 객체 감지 수정
    #results는 감지된 객체들의 정보가 담긴 리스트
    results = model(frame)
    
    #results에는 여러 개의 result 객체가 있을 수 있음 (보통 한 프레임에 한 개)
    for result in results:
        
        #result.boxes에는 감지된 모든 객체들의 바운딩 박스 정보가 담겨 있음
        for box in result.boxes:
            
            #box.cls는 탐지된 객체의 클래스 인덱스를 담은 배열 (여기서는 한개)
            cls_id = int(box.cls[0])
            
            #box.conf는 탐지된 객체의 신뢰도(confidence score)를 담음
            conf = float(box.conf[0]) #0~1 사이의 값, 높을수록 신뢰도 높음
            
            #result.names 딕셔너리에서 클래스 번호로 해당 클래스 이름을 조회
            label = result.names[cls_id] #person, car 등
            
            #사람 객체만 필터링, 신뢰도가 0.4 이상인 경우만 사용
            #신뢰도가 낮으면 잘못된 감지일 가능성이 높으므로 제외
            if label != 'person' or conf < 0.4:
                continue #조건에 맞지 않으면 다음 객체 처리로 넘어감
            
            #box.xyxy는 바운딩 박스 좌표를 담은 배열 [x1, y1, x2, y2]
            #(왼쪽 상단 x, 왼쪽 상단 y, 오른쪽 하단 x, 오른쪽 하단 y)
            #좌표는 실수형일 수 있어 정수로 변환해서 사용
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            
            #원본 프레임 위에 녹색(0, 255, 0) 선 두께 2의 사각형 그리기
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            #바운딩 박스 위쪽에 텍스트(클래스명 + 신뢰도)를 그림
            #위치: (x1, y1 - 10) -> 박스 위 약간 위쪽
            #글꼴: HERSHEY SIMPLEX, 크기: 0.7, 색상: 녹색, 두께: 2
            cv2.putText(frame, f'{label} {conf:.2f}', (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    #사람이 표시된 현재 프레임을 새로운 윈도우 창에 출력
    #창 이름: YOLOv8 Person Detection        
    cv2.imshow('YOLOv8 Person Detection', frame)

    #ESC 키 (아스키코드 27)가 입력되면 루프 종료 -> 프로그램 종료
    key = cv2.waitKey(1)
    if key == 27:
        break
    
cap.release()

cv2.destroyAllWindows()
