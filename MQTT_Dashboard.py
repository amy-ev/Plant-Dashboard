import os
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import datetime as dt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
from paho.mqtt import client as mqtt_client
from tkinter import *
from dotenv import load_dotenv

broker = os.getenv("MQTT_BROKER")
port = int(os.getenv("PORT"))
daily_topic = os.getenv("DAILY_TOPIC")
monthly_topic = os.getenv("MONTHLY_TOPIC")
motion_topic = os.getenv("MOTION_TOPIC")

client_id = f'{os.getenv("CLIENT_ID")}-{random.randint(0,1000)}'
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
device_id = os.getenv("DEVICE_ID")

with open("daily_count.txt","r") as d_file:
    daily_count = int(d_file.read())
d_file.close

with open("monthly_count.txt", "r") as m_file:
    monthly_count = int(m_file.read())
m_file.close()

motion_data = 0
lst = []
water_frames = []
img_x = 0
img_y = 0

# MQTT PROTOCOLS -------------------------------------------------------
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

def subscribe(client: mqtt_client,update_ui, day_complete):

    def on_message(client, userdata, msg):
        global daily_count
        global monthly_count
        global motion_data
        
        if msg.topic != motion_topic:

            valid_message = False

            allowed_msgs = list(range(0,32)) # needs to read up to 31 to allow for the reset to happen
            allowed_msgs =[str(i) for i in allowed_msgs]

            # check the recieved message against each value
            for i in allowed_msgs:
                if msg.payload.decode() == i:
                    valid_message = True
                    break
                else:
                    valid_message = False

            # if the message is allowed determine what to do with it
            if valid_message:
                print(f"recieved '{msg.payload.decode()}' from '{msg.topic}' topic")
                if msg.topic == daily_topic:
                        # to avoid an error with the animation frames
                        if int(msg.payload.decode()) < 9:
                            with open("daily_count.txt", "w") as d_file: 
                                # update the txt file to hold the count between reruns of the script
                                d_file.write(msg.payload.decode())
                                daily_count = int(msg.payload.decode())
                            d_file.close()
                            update_ui(daily_count)
                # does not need an additional check
                if msg.topic == monthly_topic:
                    with open("monthly_count.txt", "w") as m_file:
                        m_file.write(msg.payload.decode())
                        monthly_count = int(msg.payload.decode())
                    m_file.close()
                    day_complete()
        else:
            print(f'recieved {msg.payload.decode()} from {msg.topic} topic')
            motion_data = int(msg.payload.decode())
                
    client.subscribe(daily_topic)
    client.subscribe(monthly_topic)
    client.subscribe(motion_topic)
    client.on_message = on_message


def publish(client,topic,msg, retain):
    result = client.publish(topic,msg, retain=True)
    status = result[0]
    if status == 0:
        print(f"send '{msg}' to topic '{topic}'")
    else:
        print("failed")

    if topic == daily_topic:
        with open("daily_count.txt","w") as d_file:
            d_file.write(str(msg))
        d_file.close()

    if topic == monthly_topic:
        with open("monthly_count.txt","w") as m_file:
            m_file.write(str(msg))
        m_file.close()

# ---------------------------------------------------------------------

def inc_daily():
    global daily_count
    daily_count+=1

def inc_monthly():
    global monthly_count
    monthly_count+=1

# UI CREATION ----------------------------------------------------------
def create_window(client):
    global daily_count

    window = Tk()
    window.title("MQTT Dashboard")
    window.geometry('325x700')
    window.resizable(False,False)

    # background image
    canvas = Canvas(window, width=325, height=700, borderwidth=0, highlightthickness=0)
    background_img = PhotoImage(file="background.png")
    canvas.create_image(0,0, anchor=NW, image=background_img)

    frame_img = PhotoImage(file=f"F{daily_count}.png")
    water_frames.append(frame_img)
    canvas.create_image(22*5,99*5, anchor=NW, image=frame_img)

    #reset button for testing
    reset_img = PhotoImage(file="reset_button.png")
    reset_btn = Button(window, image = reset_img,command=lambda:day_end(), borderwidth=0, highlightthickness=0)
    reset_btn.imgref = reset_img
    reset_btn.place(x=55*5,y=131*5)

    # garbage collection
    canvas.imgref = background_img

    # update the water bottles animation frame
    def update_ui(daily_count):
        frame_img = PhotoImage(file=f"F{daily_count}.png")
        water_frames.append(frame_img)
        canvas.create_image(22*5,99*5, anchor=NW, image=frame_img)

    # recreate what would be performed at midnight
    def day_end():
        global daily_count
        daily_count = 0
        publish(client, daily_topic, daily_count, True)

    # carry out with every button click
    def glass_finished(client):
        global daily_count
        global monthly_count

        if daily_count <= 8:
            publish(client, daily_topic, daily_count, True)

            if daily_count == 8:
                inc_monthly()
                publish(client, monthly_topic, monthly_count, True)

    # carried out if all 8 glasses were finished in a day
    def day_complete():
        global monthly_count
        active_img = PhotoImage()
        canvas.create_image(0,0,image=active_img)

        # store each of the x,y coords of the shelf items

        pos_dict = {"img0":(0,13),"img1":(11,19),"img2":(22,17),"img3":(32,19),"img4":(46,20),"img5":(60,20),
            "img6":(0,39),"img7":(6,37),"img8":(23,39),"img9":(29,38),"img10":(46,42),"img11":(57,35),
            "img12":(0,59),"img13":(6,59),"img14":(22,59),"img15":(33,57),"img16":(47,63),"img17":(54,57),
            "img18":(1,79),"img19":(0,85),"img20":(23,85),"img21":(32,84),"img22":(45,84),"img23":(56,81),
            "img24":(6,100),"img25":(0,107),"img26":(45,101),"img27":(60,105),
            "img28":(0,122),"img29":(47,122)}

        if monthly_count < 31: # at 31 to allow a roll over for reset
             for x in range(monthly_count):
                active_img = PhotoImage(file=f"img_{x}.png")
                lst.append(active_img)

                values = pos_dict.get(f"img{x}", [])
                img_x = values[0]
                img_y = values[1]
            
                canvas.create_image(img_x*5,img_y*5, anchor=NW, image=active_img)
        else:
            # reset the count
            monthly_count = 0
            publish(client,monthly_topic, monthly_count, True)

    # button creation
    img = PhotoImage(file="button.png")  
    btn = Button(window, image=img, command=lambda:[inc_daily(), glass_finished(client)], borderwidth=0, highlightthickness=0)

    btn.imgref = img 
    btn.place(x=100,y=610)
    graph = createGraph()

    canvas.pack()
    return window, update_ui, day_complete, graph

# --------------------------------------------------------------------------------
def createGraph():
    graph_window = Toplevel()
    graph_window.title('graph')
    graph_window.geometry('600x600+800+0')

    fig = Figure(figsize=(9,9),dpi=100)

    plot1 = fig.add_subplot(111)
    xs = []
    ys = []
    
    def animate(i, xs, ys):
        global motion_data

        xs.append(dt.datetime.now().strftime('%H:%M:%S'))
        ys.append(motion_data)

        xs = xs[-10:]
        ys = ys[-10:]

        plot1.clear()
        plot1.plot(xs,ys)

        plt.setp(plot1.get_xticklabels(), rotation=45)
        #plt.title('Motion Sensor Data')
        #plt.ylabel('Range')


    canvas = FigureCanvasTkAgg(fig, master=graph_window)
    ani = animation.FuncAnimation(fig,animate, fargs=(xs,ys),interval=1000, cache_frame_data=False)
    plt.show()
    canvas.draw()
    canvas.get_tk_widget().pack()

    return graph_window

def main():
    client = connect_mqtt()
    client.loop_start()

    window, update_ui, day_complete, graph = create_window(client)
    subscribe(client, update_ui, day_complete) 
    window.mainloop()
    
    client.loop_stop()

if __name__ == '__main__':
    main()