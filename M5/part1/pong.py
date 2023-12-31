'''
Original code can be found here: https://github.com/VissaMoutafis/Pong
By VissaMoutafis

Modified for M4 at UCLA ECE M119
By Warren Pagsuguiron
'''

import turtle  # very basic gui design module
import time
import os
import paho.mqtt.client as mqtt
import numpy as np

data_out_1, data_out_2 = None, None

class mqtt_publisher1():
    # 0. define callbacks - functions that run when events happen.
    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, flags, rc):
        print("Connection returned result: " + str(rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe('ECEM119_1')
        # The callback of the client when it disconnects.

    def on_disconnect(client, userdata, rc):
        if rc != 0:
            print('Unexpected Disconnect')
        else:
            print('Expected Disconnect')
        # The default message callback.
        # (won't be used if only publishing, but can still exist)

    def on_message(client, userdata, message):
        message = str(message.payload)[2:-1]
        # print('Received message: ', message)
        data = message.split(';')

        player_data = data.pop(0)
        mode, pre_player = player_data.split(',')
        player = int(pre_player)
        
        mappings = {'Acceleration': {}, 'Gyroscope': {}}
        for d in data:
            degree, axis, value = d.split(',')
            mappings[degree][axis] = float(value)
        
        print(player, data)
        if (player == 1):
            global data_out_1
            data_out_1 = mappings
        if (player == 2):
            global data_out_2
            data_out_2 = mappings
                
    # 1. create a client instance.
    client = mqtt.Client()
    # add additional client options (security, certifications, etc.)
    # many default options should be good to start off.
    # add callbacks to client.
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    # 2. connect to a broker using one of the connect*() functions.
    client.connect_async("test.mosquitto.org")
    # client.connect_async('mqtt.eclipseprojects.io')

    # 3. call one of the loop*() functions to maintain network traffic flow with the broker.
    client.loop_start()

    # 4. use subscribe() to subscribe to a topic and receive messages.
    # 5. use publish() to publish messages to the broker.
    # payload must be a string, bytearray, int, float or None.
    #client.publish("ECEM119", curr, qos=1)

    # 6. use disconnect() to disconnect from the broker.
    # client.loop_stop()
    # client.disconnect()

class mqtt_publisher2():
    # 0. define callbacks - functions that run when events happen.
    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, flags, rc):
        print("Connection returned result: " + str(rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe('ECEM119_2')
        # The callback of the client when it disconnects.

    def on_disconnect(client, userdata, rc):
        if rc != 0:
            print('Unexpected Disconnect')
        else:
            print('Expected Disconnect')
        # The default message callback.
        # (won't be used if only publishing, but can still exist)

    def on_message(client, userdata, message):
        message = str(message.payload)[2:-1]
        # print('Received message: ', message)
        data = message.split(';')

        player_data = data.pop(0)
        mode, pre_player = player_data.split(',')
        player = int(pre_player)
        
        mappings = {'Acceleration': {}, 'Gyroscope': {}}
        for d in data:
            degree, axis, value = d.split(',')
            mappings[degree][axis] = float(value)
        
        print(player, data)
        if (player == 1):
            global data_out_1
            data_out_1 = mappings
        if (player == 2):
            global data_out_2
            data_out_2 = mappings
                
    # 1. create a client instance.
    client = mqtt.Client()
    # add additional client options (security, certifications, etc.)
    # many default options should be good to start off.
    # add callbacks to client.
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    # 2. connect to a broker using one of the connect*() functions.
    # client.connect_async("test.mosquitto.org")
    client.connect_async('mqtt.eclipseprojects.io')

    # 3. call one of the loop*() functions to maintain network traffic flow with the broker.
    client.loop_start()

    # 4. use subscribe() to subscribe to a topic and receive messages.
    # 5. use publish() to publish messages to the broker.
    # payload must be a string, bytearray, int, float or None.
    #client.publish("ECEM119", curr, qos=1)

    # 6. use disconnect() to disconnect from the broker.
    # client.loop_stop()
    # client.disconnect()


#Window
wn = turtle.Screen()  # we need a screen
wn.title("Pong")
wn.bgcolor("black")
wn.setup(width=700, height=500)
wn.tracer(0)

#Choose Multiplayer or Single player
message = turtle.Turtle()
message.speed(0)
message.color("white")
message.penup()
message.hideturtle()
message.write("No Data Input!", False, align='center',
              font=('Arial', 15, 'normal'))
answers = {"Singleplayer": 1, "Multiplayer": 2}
answer = wn.textinput(
    "pick a mode: ", f"Type one of the following: {answers}")

version = ""
if(answer == "1"):
    version = "singleplayer"
    print("Entering singleplayer... AI Bot getting ready for first round...")
else:
    version = "2"
    print("Entering multiplayer")
message.clear()

#Pen
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 210)

#Paddle A
a_score = 0
paddle_a = turtle.Turtle()
paddle_a.speed(0)
paddle_a.shape("square")
paddle_a.color("white")
paddle_a.shapesize(stretch_wid=9, stretch_len=1)
paddle_a.penup()
paddle_a.goto(-350, 0)
paddle_a.hideturtle()

#Paddle B
b_score = 0
paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape("square")
paddle_b.color("white")
paddle_b.shapesize(stretch_wid=9, stretch_len=1)
paddle_b.penup()
paddle_b.goto(345, 0)
paddle_b.hideturtle()

#Ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("circle")
ball.color("white")
ball.penup()
ball.goto(0, 0)
max_dx = 6
max_dy = 6
ball.dx = 1
ball.dy = 1

#Function for moving a up


def paddle_a_up():
    if(paddle_a.ycor() < 205):
        y = paddle_a.ycor()  # get the y coordinates
        y += 40
        paddle_a.sety(y)  # move the paddle 40px up

#Function for movin a down


def paddle_a_down():
    if(paddle_a.ycor() > -205):
        y = paddle_a.ycor()
        y -= 40
        paddle_a.sety(y)


# paddle b is player
# def paddle_b_up():
#     if(paddle_b.ycor() < 205):
#         y = paddle_b.ycor()  # get the y coordinates
#         y += 40
#         paddle_b.sety(y)  # move the paddle 40px up

# #Function for movin a down
# def paddle_b_down():
#     if(paddle_b.ycor() > -205):
#         y = paddle_b.ycor()
#         y -= 40
#         paddle_b.sety(y)

def move_player_1():
    acc_y = data_out_1['Acceleration']['y']
    
    # normalize
    y = paddle_b.ycor()

    if acc_y > 0 and paddle_b.ycor() < 205:
        acc_y = min(1, acc_y)
        

    if acc_y < 0 and paddle_b.ycor() > -205:
        acc_y = max(-1, acc_y)

    paddle_b.sety(acc_y * 204)
    print(acc_y * 204)

def move_player_2():
    acc_y = data_out_2['Acceleration']['y']
    
    # normalize
    y = paddle_a.ycor()

    if acc_y > 0 and paddle_a.ycor() < 205:
        acc_y = min(1, acc_y)
        

    if acc_y < 0 and paddle_a.ycor() > -205:
        acc_y = max(-1, acc_y)

    paddle_a.sety(acc_y * 204)
    print(acc_y * 204)

aiPaddle = paddle_a
ai_down = paddle_a_down
ai_up = paddle_a_up

#AI BOT for singleplayer mode
def ai_paddle_move():
    _y = ball.ycor()
    y = aiPaddle.ycor()

    #if the paddle is higher that the ball and the ball is moving downwards then go down
    if y > _y and ball.dy < 0:
        ai_down()
    elif y < _y and ball.dy > 0:
        ai_up()


#Keyboard listening
wn.listen()
if version == "multiplayer":
    wn.onkeypress(paddle_a_up, "w")
    wn.onkeypress(paddle_a_down, "s")

# wn.onkeypress(paddle_b_up, "Up")
# wn.onkeypress(paddle_b_down, "Down")


def updateScore():
    scoreBoard = "Score: A = " + str(a_score) + " - B = " + str(b_score)
    pen.clear()
    pen.write(scoreBoard, align="center", font=("Courier", 20, "bold"))


#Main Loop
mqtt_client_1 = mqtt_publisher1()
mqtt_client_2 = mqtt_publisher2()
paddle_a.showturtle()
paddle_b.showturtle()

while True:
    if (version != 'singleplayer'):
        while data_out_2 is None:
            print('No input found for player 2')
    while data_out_1 is None:
            print('No input found for player 1')
    wn.update()
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)
    move_player_1()
    if(version == "singleplayer"):
        ai_paddle_move()
    else:
        move_player_2()
    updateScore()

    #border checking
    if ball.ycor() > 250:
        ball.sety(250)
        ball.dy *= -1
        os.system("aplay bounce.wav&")

    if ball.ycor() < -250:
        ball.sety(-250)
        ball.dy *= -1
        os.system("aplay bounce.wav&")

    if ball.xcor() > 350:
        ball.goto(0, 0)
        ball.dx = -2  # re-initialize the speed
        a_score += 1

    if ball.xcor() < -350:
        ball.goto(0, 0)
        ball.dx = 2  # re-initialize the speed
        b_score += 1

    #Paddle and ball collisions
    if (ball.xcor() > 340 and ball.xcor() < 350):
        if ball.ycor() < paddle_b.ycor() + 100 and ball.ycor() > paddle_b.ycor() - 100:
            ball.setx(335)
            ball.dx *= -1
            os.system("aplay bounce.wav&")

    if (ball.xcor() < -340 and ball.xcor() > -350):
        if ball.ycor() < paddle_a.ycor() + 100 and ball.ycor() > paddle_a.ycor() - 100:
            ball.setx(-335)
            ball.dx *= -1
            os.system("aplay bounce.wav&")
