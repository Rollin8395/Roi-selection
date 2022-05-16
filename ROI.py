import cv2
import numpy as np
import sys
import pypyodbc as odbc

DRIVER = 'SQL Server'
SERVER_NAME = 'ROLLIN\SQLEXPRESS'
DATABASE_NAME = 'motion_detection'

drawing = False
point1 = ()
point2 = ()
text = ''
font = cv2.FONT_HERSHEY_COMPLEX
color = (255, 0, 0)


def connection_string(driver, server_name, database_name):
    conn_string = f"""
         DRIVER={{{driver}}};
         SERVER={server_name};
         DATABASE={database_name};
       """
    return conn_string

def sql(cameraip,coor):
    conn = odbc.connect(connection_string(DRIVER, SERVER_NAME, DATABASE_NAME))
    cursor = conn.cursor()

    sql1 = "INSERT INTO IP_Cordinates(Camera_IP,Cordinates) VALUES('{}','{}')".format(
        cameraip,coor)
    # print(val, 'New data added')
    cursor.execute(sql1)
    conn.commit()
    cursor.close()
    conn.close()

def mouse_drawing(event, x, y, flags, params):
    global point1, point2, drawing
    if event == cv2.EVENT_LBUTTONDOWN:

        if drawing is False:
            drawing = True
            point1 = (x, y)
            text = str(x) + "," + str(y)
            color = (0, 255, 0)

        else:
            drawing = False
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing is True:
            point2 = (x, y)



def Main(ip):
    cap = cv2.VideoCapture(ip)

    cv2.namedWindow("Frame")

    cv2.setMouseCallback("Frame", mouse_drawing)
    # cv2.setMouseCallback("Frame", mouse_drawing)

    while True:
        _, frame = cap.read()
        if point1 and point2:
            r = cv2.rectangle(frame, point1, point2, (100, 50, 200), 5)
            cv2.putText(frame, str(point1), (10, 35), font, 0.75, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(frame, str(point2), (400,400), font, 0.75, (255, 255, 255), 2, cv2.LINE_AA)

        cv2.imshow("Frame", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            co_ordinates=str(point1)+","+str(point2)
            print(co_ordinates)
            sql(ip,co_ordinates)

            break

    cap.release()
    cv2.destroyAllWindows()


Main(1)
