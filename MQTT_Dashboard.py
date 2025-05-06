import os
import random
from paho.mqtt import client as mqtt_client
from tkinter import *
from dotenv import load_dotenv

broker = os.getenv("MQTT_BROKER")
port = int(os.getenv("PORT"))
topic = os.getenv("DAILY_TOPIC")
topic_sub = os.getenv("DAILY_TOPIC")

client_id = f'{os.getenv("CLIENT_ID")}-{random.randint(0,1000)}'
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
device_id = os.getenv("DEVICE_ID")

daily_count = 0
monthly_count = 15


item_dict = {"item_0": False, "item_1": False, "item_2": False, "item_4": False,
              "item_5": False, "item_6": False, "item_7": False, "item_8": False, 
              "item_9": False, "item_10": False, "item_11": False, "item_12": False,               
              "item_13": False, "item_14": False, "item_15": False, "item_16": False, 
              "item_17": False, "item_18": False, "item_19": False, "item_20": False,
              "item_21": False, "item_22": False, "item_23": False, "item_24": False, 
              "item_25": False, "item_26": False, "item_27": False, "item_28": False,
              "item_29": False, "item_30": False, "item_31": False}
lst = []
water_frames = []
img_x = 0
img_y = 0

def connect_mqtt():

    def on_connect(client, userdata, flags, rc, properties):
        if rc==0:
            print("successfully connected to MQTT broker")
        else:
            print("failed to connect")
    client = mqtt_client.Client(client_id=client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client: mqtt_client):
    global daily_count
    def on_message(client, userdata, msg):
        print(f"recieved '{msg.payload.decode()}' from '{msg.topic}' topic")
        daily_count = int(msg.payload.decode())
        
    client.subscribe(topic_sub)
    client.on_message = on_message

def publish(client,counter):
    msg = counter
    result = client.publish(topic,msg)
    status = result[0]
    if status == 0:
        print(f"send '{msg}' to topic '{topic}'")
    else:
        print("failed")

 

def create_window(client):
    window = Tk()
    window.title("MQTT Dashboard")
    window.geometry('325x700')
    window.resizable(False,False)

    # background image
    canvas = Canvas(window, width=325, height=700, borderwidth=0, highlightthickness=0)
    background_img = PhotoImage(file="background.png")
    canvas.create_image(0,0, anchor=NW, image=background_img)

    # water tracker image
    frame_img = PhotoImage(file="F0.png")
    water_frames.append(frame_img)
    canvas.create_image(22*5,99*5, anchor=NW, image=frame_img)

    # garbage collection
    canvas.imgref = background_img
    canvas.pack()

 
    def glass_finished(client):
        global daily_count
        global monthly_count
        daily_count+=1

        if daily_count <= 8:
            for x in range(daily_count+1):
                frame_img = PhotoImage(file=f"F{str(x)}.png")
                water_frames.append(frame_img)
                canvas.create_image(22*5,99*5, anchor=NW, image=frame_img)

            publish(client, daily_count)


            if daily_count == 8:
                monthly_count+=1
                day_complete()
            print(daily_count)


    def day_complete():
        global monthly_count
        if monthly_count < 31:
            for x in range(monthly_count):
                #x = random.randint(0,2)
                if (item_dict.get("item_"+str(x)) == False):

                    active_img = PhotoImage(file=f"img_{str(x)}.png")
                    lst.append(active_img)
                    
                    # 1ST ROW -----------------
                    if x == 0:
                        img_x = 0
                        img_y = 13
                    elif x == 1:
                        img_x = 11
                        img_y = 19
                    elif x == 2:
                        img_x = 22
                        img_y = 17
                    elif x == 3:
                        img_x = 33
                        img_y = 19
                    elif x == 4:
                        img_x = 46
                        img_y = 20
                    elif x == 5:
                        img_x = 60
                        img_y = 20
                    # 2ND ROW ----------------
                    elif x == 6:
                        img_x = 0
                        img_y = 39
                    elif x == 7:
                        img_x = 6
                        img_y = 37
                    elif x == 8:
                        img_x = 23
                        img_y = 39
                    elif x == 9:
                        img_x = 29
                        img_y = 38
                    elif x == 10:
                        img_x = 46
                        img_y = 42
                    elif x == 11:
                        img_x = 57
                        img_y = 35
                    # 3RD ROW ---------------
                    elif x == 12:
                        img_x = 0
                        img_y = 59
                    elif x == 13:
                        img_x = 6
                        img_y = 59
                    elif x == 14:
                        img_x = 22
                        img_y = 59
                    elif x == 15:
                        img_x = 33
                        img_y = 57
                    elif x == 16:
                        img_x = 47
                        img_y = 63
                    elif x == 17:
                        img_x = 54
                        img_y = 57
                    # 4TH ROW ------------------
                    elif x == 18:
                        img_x = 1
                        img_y = 79
                    elif x == 19:
                        img_x = 0
                        img_y = 85
                    elif x == 20:
                        img_x = 23
                        img_y = 85
                    elif x == 21:
                        img_x = 32
                        img_y = 84
                    elif x == 22:
                        img_x = 45
                        img_y = 84
                    elif x == 23:
                        img_x = 56
                        img_y = 81
                    # 5TH ROW -------------------
                    elif x == 24:
                        img_x = 6
                        img_y = 100   
                    elif x == 25:
                        img_x = 0
                        img_y = 107
                    elif x == 26:
                        img_x = 45
                        img_y = 101    
                    elif x == 27:
                        img_x = 60
                        img_y = 105 
                    # 6TH ROW ------------------
                    elif x == 28:
                        img_x = 0
                        img_y = 122
                    elif x == 29:
                        img_x = 47
                        img_y = 122
                    else:
                        img_x = 0
                        img_y = 120
                
                    canvas.create_image(img_x*5,img_y*5, anchor=NW, image=active_img)
                    item_dict["item_"+str(x)] = True

    day_complete()
    img = PhotoImage(file="button.png")  
    btn = Button(window, image=img, command=lambda:glass_finished(client), borderwidth=0, highlightthickness=0)
    #  command=lambda:glass_finished(mqtt_client),
    btn.imgref = img
    btn.place(x=100,y=610)
    
    if daily_count == 8:
        day_complete()

    return window


def main():
    client = connect_mqtt()

    client.loop_start()

    subscribe(client) # currently for debugging 
    window = create_window(client)

    window.mainloop()

    client.loop_stop()

if __name__ == '__main__':
    main()