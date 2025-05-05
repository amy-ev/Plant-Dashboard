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
monthly_count = 2
item_dict = {"item_0": False, "item_1": False, "item_2": False, "item_4": False,
              "item_5": False, "item_6": False, "item_7": False, "item_8": False, 
              "item_9": False, "item_10": False, "item_11": False, "item_12": False,               
              "item_13": False, "item_14": False, "item_15": False, "item_16": False, 
              "item_17": False, "item_18": False, "item_19": False, "item_20": False,
              "item_21": False, "item_22": False, "item_23": False, "item_24": False, 
              "item_25": False, "item_26": False, "item_27": False, "item_28": False,
              "item_29": False, "item_30": False, "item_31": False}
lst = []
img_x = 0
img_y = 0

def connect_mqtt():

    def on_connect(client, userdata, flags, rc, properties):
        if rc==0:
            print("successfully connected to MQTT broker")
        else:
            print("failed to connect")
    client = mqtt_client.Client(client_id=client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)
    #client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client: mqtt_client):

    def on_message(client, userdata, msg):
        print(f"recieved '{msg.payload.decode()}' from '{msg.topic}' topic")
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

def glass_finished(client):
    global daily_count
    daily_count+=1
    if daily_count <= 8: # only send a message while daily count is less than 8
        publish(client,daily_count)

def create_window(mqtt_client):
    window = Tk()
    window.title("MQTT Dashboard")
    window.geometry('325x700')
    window.resizable(False,False)
    window.configure(bg="white")
    
    photo = PhotoImage(file="shelf.png")
    canvas = Canvas(window, width=325, height=700, borderwidth=0, highlightthickness=0)

    canvas.create_image(0,0, anchor=NW, image=photo)
    canvas.imgref = photo
    canvas.pack()

    # canvas1 = Canvas(canvas, width=20, height=20, background="black", borderwidth=0, highlightthickness=0)
    # canvas.create_window(20,20, anchor="nw", window=canvas1)

    img = PhotoImage(file="button.png")   

    def day_complete():
        global monthly_count
        img_0 = PhotoImage(file="img_0.png")
        img_1 = PhotoImage(file="img_1.png")
        img_2 = PhotoImage(file="img_2.png")
        # img_3 = PhotoImage(file="img_3.png")
        # img_4 = PhotoImage(file="img_4.png")
        # img_5 = PhotoImage(file="img_5.png")
        # img_6 = PhotoImage(file="img_6.png")
        # img_7 = PhotoImage(file="img_7.png")
        # img_8 = PhotoImage(file="img_8.png")
        # img_9 = PhotoImage(file="img_9.png")
        # img_10 = PhotoImage(file="img_10.png")
        # img_11 = PhotoImage(file="img_11.png")
        # img_12 = PhotoImage(file="img_12.png")
        # img_13 = PhotoImage(file="img_13.png")
        # img_14 = PhotoImage(file="img_14.png")
        # img_15 = PhotoImage(file="img_15.png")
        # img_16 = PhotoImage(file="img_16.png")
        # img_17 = PhotoImage(file="img_17.png")
        # img_18 = PhotoImage(file="img_18.png")
        # img_19 = PhotoImage(file="img_19.png")
        # img_20 = PhotoImage(file="img_20.png")
        # img_21 = PhotoImage(file="img_21.png")
        # img_22 = PhotoImage(file="img_22.png")
        # img_23 = PhotoImage(file="img_23.png")
        # img_24 = PhotoImage(file="img_24.png")
        # img_25 = PhotoImage(file="img_25.png")
        # img_26 = PhotoImage(file="img_26.png")
        # img_27 = PhotoImage(file="img_27.png")
        # img_28 = PhotoImage(file="img_28.png")
        # img_29 = PhotoImage(file="img_29.png")
        # img_30 = PhotoImage(file="img_30.png")
        # img_31 = PhotoImage(file="img_31.png")


        item_0 = canvas.create_image(0,0, anchor=NW,image=img_0)
        item_1 = canvas.create_image(0,0, anchor=NW, image=img_1)
        item_2 = canvas.create_image(0,0, anchor=NW, image=img_2)
        # item_3 = canvas.create_image(0,0, anchor=NW,image=img_3)
        # item_4 = canvas.create_image(0,0, anchor=NW, image=img_4)
        # item_5 = canvas.create_image(0,0, anchor=NW, image=img_5)
        # item_6 = canvas.create_image(0,0, anchor=NW,image=img_6)
        # item_7 = canvas.create_image(0,0, anchor=NW,image=img_7)
        # item_8 = canvas.create_image(0,0, anchor=NW,image=img_8)
        # item_9 = canvas.create_image(0,0, anchor=NW,image=img_9)
        # item_10 = canvas.create_image(0,0, anchor=NW,image=img_10)
        # item_11 = canvas.create_image(0,0, anchor=NW,image=img_11)
        # item_12 = canvas.create_image(0,0, anchor=NW,image=img_12)
        # item_13 = canvas.create_image(0,0, anchor=NW,image=img_13)
        # item_14 = canvas.create_image(0,0, anchor=NW,image=img_14)
        # item_15 = canvas.create_image(0,0, anchor=NW,image=img_15)
        # item_16 = canvas.create_image(0,0, anchor=NW,image=img_16)
        # item_17 = canvas.create_image(0,0, anchor=NW,image=img_17)
        # item_18 = canvas.create_image(0,0, anchor=NW,image=img_18)
        # item_19 = canvas.create_image(0,0, anchor=NW,image=img_19)
        # item_20 = canvas.create_image(0,0, anchor=NW,image=img_20)
        # item_21 = canvas.create_image(0,0, anchor=NW,image=img_21)
        # item_22 = canvas.create_image(0,0, anchor=NW,image=img_22)
        # item_23 = canvas.create_image(0,0, anchor=NW,image=img_23)
        # item_24 = canvas.create_image(0,0, anchor=NW,image=img_24)
        # item_25 = canvas.create_image(0,0, anchor=NW,image=img_25)
        # item_26 = canvas.create_image(0,0, anchor=NW,image=img_26)
        # item_27 = canvas.create_image(0,0, anchor=NW,image=img_27)
        # item_28 = canvas.create_image(0,0, anchor=NW,image=img_28)
        # item_29 = canvas.create_image(0,0, anchor=NW,image=img_29)
        # item_30 = canvas.create_image(0,0, anchor=NW,image=img_30)
        # item_31 = canvas.create_image(0,0, anchor=NW,image=img_31)

        
        img_dict = list(range(3))
  

        #print(item_dict.get("item_"+str(x)))
        for day in range(monthly_count):
            x = random.randint(0,2)
            if (item_dict.get("item_"+str(x)) == False):

                active_img = PhotoImage(file=f"img_{str(x)}.png")
                lst.append(active_img)
                
                if x == 0:
                    img_x = 5
                    img_y = 13*5
                elif x == 1:
                    img_x = 110
                    img_y = 12*5
                else:
                    img_x = 160
                    img_y = 12*5    
            
                canvas.create_image(img_x,img_y, anchor=NW, image=active_img)
                item_dict["item_"+str(x)] = True
            else:
                x = random.randint(0,2)
                
    btn = Button(window, command=lambda:glass_finished(mqtt_client), image=img, borderwidth=0, highlightthickness=0)
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