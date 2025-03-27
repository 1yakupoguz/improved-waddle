from ultralytics import YOLO
import cv2
import math
import time 

model = YOLO('C:\\Users\\yakup\\Desktop\\AYVOS STAJ\\yolomsu\\yolov11_car_detection.pt')

line_1_counter = 0
line_2_counter = 0
line_3_counter = 0
line_4_counter = 0

cap = cv2.VideoCapture('cars.mp4')

frame_number = 0
center_points_cur_frame = []
center_points_prev_frame = []
tracking_objects = {}
passed_objects = {}
track_id = 0

while cap.isOpened():
    ret, frame = cap.read()
    frame_number+=1 #frame sayısı
    if not ret:
        break

    results = model(frame)
    center_points_cur_frame = [] # her yeni framede liste sıfırlanır

    for result in results:
        boxes = result.boxes
        for box in boxes:
            conf = float(box.conf[0])
            if conf > 0.5:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cx = int((x1+x2)/2)
                cy = int((y1+y2)/2)
                center_points_cur_frame.append((cx,cy))
                print("FRAME NUMBER ",frame_number ," ", x1,y1,x2,y2)
                label = model.names[int(box.cls[0])]
                #cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
                cv2.rectangle(frame, (x1,y1), (x2, y2), (0, 255, 0), 1)

    if frame_number <= 2: # ilk iki kare için
        for pt in center_points_cur_frame:
            for pt2 in center_points_prev_frame:
                distance = math.hypot(pt2[0] - pt[0], pt2[1] - pt[1]) # öklid mesafesi bulunur
                if distance < 10:
                    tracking_objects[track_id] = pt
                    track_id += 1
    else:
        tracking_objects_copy = tracking_objects.copy() # döngüdeki hatayı düzeltmek için
        center_points_cur_frame_copy = center_points_cur_frame.copy() # döngüdeki hatayı düzeltmek için
        for object_id, pt2 in tracking_objects_copy.items():
            object_exists = False
            for pt in center_points_cur_frame_copy:
                distance = math.hypot(pt2[0] - pt[0], pt2[1] - pt[1])
                if distance < 10: # update ids position
                    tracking_objects[object_id] = pt
                    object_exists = True
                    if pt in center_points_cur_frame:
                        center_points_cur_frame.remove(pt)
                        continue
            
            if not object_exists: # nesne artık yoksa takip edilenler listesinden çıkartılır
                tracking_objects.pop(object_id)

        for pt in center_points_cur_frame: # mevcut karede olan ancak ilişkilendirilmeyen noktalar listeye ekleniyor
            tracking_objects[track_id] = pt
            track_id += 1

    for object_id, pt in tracking_objects.items():
        cv2.circle(frame, pt, 5,(0,0,255), -1)
        cv2.putText(frame, str(object_id),(pt[0],pt[1]-7), 0, 1, (0,0,255), 2)
        if object_id not in passed_objects:
            passed_objects[object_id] = set()
        if ( pt[0] < 490 and pt[0] > 410 ) and (pt[1]>400 and pt[1]<405) and "line_1" not in passed_objects[object_id]:
            line_1_counter += 1
            passed_objects[object_id].add("line_1")
        elif ( pt[0] < 575 and pt[0] > 500 ) and (pt[1]>400 and pt[1]<405) and "line_2" not in passed_objects[object_id]:
            line_2_counter += 1
            passed_objects[object_id].add("line_2")
        elif ( pt[0] < 775 and pt[0] > 700 ) and (pt[1]>400 and pt[1]<405) and "line_3" not in passed_objects[object_id]:
            line_3_counter += 1
            passed_objects[object_id].add("line_3")
        elif ( pt[0] < 850 and pt[0] > 780 ) and (pt[1]>400 and pt[1]<405) and "line_4" not in passed_objects[object_id]:
            line_4_counter += 1
            passed_objects[object_id].add("line_4")


    cv2.putText(frame, f"1.Serit:{line_1_counter}",(20,50), 0, 1, (0,0,255), 2)
    cv2.putText(frame, f"2.Serit:{line_2_counter}",(20,80), 0, 1, (0,0,255), 2)
    cv2.putText(frame, f"3.Serit:{line_3_counter}",(20,110), 0, 1, (0,0,255), 2)
    cv2.putText(frame, f"4.Serit:{line_4_counter}",(20,140), 0, 1, (0,0,255), 2)
    cv2.putText(frame, f"Gidis:{line_1_counter+line_2_counter}",(170,50), 0, 1, (120,120,120), 3)
    cv2.putText(frame, f"Gelis:{line_3_counter+line_4_counter}",(170,110), 0, 1, (120,120,120), 3)

    cv2.line(frame,(410,400),(490,400),(0,255,0),1) # line 1
    cv2.line(frame,(500,400),(575,400),(0,0,255),1) # line 2
    cv2.line(frame,(700,400),(775,400),(255,0,0),1) # line 3
    cv2.line(frame,(780,400),(850,400),(255,255,0),1) # line 4


    # print("Tracking objects")
    # print(tracking_objects)

    # print("CUR FRAME LEFT PTS")
    # print(center_points_cur_frame)
    # print("PREV_FRAME")
    # print(center_points_prev_frame)
    cv2.imshow('car_detection', frame)
    
    center_points_prev_frame = center_points_cur_frame.copy() #diğer frame geçmeden önce mevcutu eski olarak güncelliyoruz

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()


