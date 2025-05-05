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
    window.geometry('265x395')
    window.resizable(False,False)
    window.configure(bg="white")

    photo = PhotoImage(file="background.png")
    canvas = Canvas(window, width=265, height=395)


    canvas.create_image(0,0, anchor=NW, image=photo)
    canvas.imgref = photo
    canvas.pack()

    img = PhotoImage(file="button.png")

    btn = Button(window, command=lambda:glass_finished(mqtt_client), image=img)
    btn.imgref = img
    btn.place(x=50,y=249)
    
    return window


def main():
    load_dotenv()
    client = connect_mqtt()

    client.loop_start()

    subscribe(client) # currently for debugging 

    window = create_window(client)

    window.mainloop()

    client.loop_stop()

if __name__ == '__main__':
    main()