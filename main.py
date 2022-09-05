##importing relevant libraries##
import datetime
import random
import string
import webbrowser as wb
import pyautogui
import yagmail
import pyttsx3
import speech_recognition as sr
import pywhatkit
import pyjokes
import wikipedia
from secret import sender_email, pswd
from time import sleep
import requests, json
from newsapi import NewsApiClient
import clipboard
import os
import time
import psutil

##end
listener = sr.Recognizer()  ## Initalizing speech recognition
engine = pyttsx3.init()  ## Initalizing python text to speech library
voices = engine.getProperty('voices')  ## Getting voices to set the property to male
engine.setProperty('voice', voices[0].id)


## Function to take command from user through mic. It will be used everywhere
def take_command():
    try:
        with sr.Microphone() as source:
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            return command
    except Exception as e:
        print(e)


##end
##this function will allow to say anything that user wants
def talk(audio):
    engine.say(audio)
    engine.runAndWait()


##end

##Function to get time using datetime package
def get_time():
    time = datetime.datetime.now().strftime('%H:%M:%S')
    return time


##end
##Function to get date using datetime package
def get_date():
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    return date


##end

##the Ai Assitant will wish good morning, everning, afternoon or night on executing the package using this function
def greetings():
    hours = datetime.datetime.now().hour
    if hours >= 6 and hours < 12:
        talk("good morning sir")
    elif hours >= 12 and hours <= 18:
        talk("good evening sir")
    elif hours > 18 and hours <= 24:
        talk("good afternoon sir")
    else:
        talk("good night sir")


##end
## At execution, the assistant will give its intro using this function
def greet():
    greetings()
    greet = "this is jarvis, current time is " + get_time() + ", and date is " + get_date() + ", how may I help you today? "
    talk(greet)
    print(greet)


##end
##This function will open youtube videos from user's command
def play_on_yt(command):
    talk('opening' + command)
    pywhatkit.playonyt(command)


##end
##This function will search meaning of a word from wikipedia using user's command
def get_meaning(command):
    info = wikipedia.summary(command, 1)
    print(info)
    talk(info)


# end
##This functon will send email on user's command using yagmail
def send_email():
    try:
        with sr.Microphone() as source:
            yag = yagmail.SMTP(sender_email, pswd)
            talk("Please type in the receiver email address")
            email = input("Enter email address here : ")
            talk("Please tell the subject")
            voice = listener.listen(source)
            subj = listener.recognize_google(voice)
            subj = subj.lower()
            talk("Please tell the body")
            voice = listener.listen(source)
            body = listener.recognize_google(voice)
            body = body.lower()
            yag.send(to=email, subject=subj, contents=body)
            talk("Email sent")
    except Exception as e:
        print(e)


## This function will send whatsapp message on user's command from the contacts in the list below
def send_whatsapp_message():
    number_list = {
        'Bunty': '+92xxxxxxxxxx'
    }
    try:
        with sr.Microphone() as source:
            talk("Please tell the name of the person")  ## from the list defined above
            voice = listener.listen(source)
            name = listener.recognize_google(voice)
            print(number_list[name])
            talk("please tell the message")  ## type message on user's command
            mesg = listener.listen(source)
            message = listener.recognize_google(mesg)
            print(message)
            pywhatkit.sendwhatmsg(number_list[name], message, datetime.datetime.now().hour,
                                  datetime.datetime.now().minute + 1)  ## send message 1m later the message is typed
            sleep(10)
            pyautogui.press('enter')  ## automatically sent message without pressing enter
            print("messAGE SENT")


    except Exception as e:
        print(e)


##end
##this function will search anything on google on user's command by using web browser library
def search_on_google():
    try:
        with sr.Microphone() as source:
            talk("What do you want to search?")
            voice = listener.listen(source)
            search = listener.recognize_google(voice)
            search = search.lower()
            wb.open("https://www.google.com/search?q=" + search)  ## search user's command
            talk("opening " + search)
    except Exception as e:
        print(e)


##end
##This function will tell weather using open weather Api
def get_weather():
    api_key = '7b8d8c17173194e8acf54de575524f67'
    base_url = 'http://api.openweathermap.org/data/2.5/weather?'
    try:
        with sr.Microphone() as source:
            talk("please tell city name")
            voice = listener.listen(source)
            city = listener.recognize_google(voice)
            city = city.lower()
            final_url = base_url + "q=" + city + "&units=imperial&appid=" + api_key  ##fetching data through Api
            print(final_url)
            res = requests.get(final_url)
            data = res.json()
            weather = data["weather"][0]["main"]
            temp = data["main"]["temp"]
            desp = data["weather"][0]["description"]
            talk("Weather is " + str(weather))
            print("Weather is " + str(weather))
            temp = round((temp - 32) * 5 / 9)  ## converting temp to celcius
            talk("Temperature is " + str(temp) + "degree celcius")
            print("Temperature is " + str(temp) + "degree celcius")
            talk("Description of weather is " + str(desp))
            print("Description of weather is " + str(desp))

    except Exception as e:
        print(e)


##end
##this function will tell news in any topic user want using news API
def get_news():
    news = NewsApiClient(api_key='ca1862099aae46b0bad7a78248f3ef98')
    talk("what topic do you want to search for?")
    try:
        with sr.Microphone() as source:
            voice = listener.listen(source)
            topic = listener.recognize_google(voice)
            topic = topic.lower()
            talk("fetching news for" + topic)
            sleep(2)
            data = news.get_top_headlines(q=topic,
                                          language='en',
                                          page_size=5)
            news_data = data["articles"]
            for x, y in enumerate(news_data):
                print(f'{x}{y["description"]}')
                talk(f'{x}{y["description"]}')
    except Exception as e:
        print(e)


##end
##This function will tell lastly copied thing in your clipboard
def get_text_from_clipboard():
    text = clipboard.paste()
    talk("Reading text from clipboard")
    sleep(2)
    print(text)
    talk(text)


##end
##This function will give worldwide covid report using covid API
def get_covid_update():
    r = requests.get('https://coronavirus-19-api.herokuapp.com/all')
    data = r.json()
    print("ok")
    covid_data = f'Confirmed Cases: {data["cases"]} \n Deaths : {data["deaths"]} \nRecovery : {data["recovered"]}'
    print(covid_data)
    talk(covid_data)


##end
##This function will open spotify on user's command
def open_spotify():
    code_path = 'C:\\Users\\aazhm\\AppData\\Roaming\\Microsoft\Windows\\Start Menu\Programs\\Spotify.lnk'
    talk("opening spotify")
    os.startfile(code_path)


##end
##This function will take screenshot of the screen on user's command
def screenshot():
    name_image = 'C:\\Users\\aazhm\\PycharmProjects\\AI_Jarvis\\screenshot\\' + str(time.time()) + '.png'
    talk("taking Screenshot")
    img = pyautogui.screenshot(name_image)
    img.show()


##end

##this function will store reminders and tell them when asked by user
def reminders():
    talk("What do you want me to do?")
    reminder = take_command()  ## here the Assitant will ask whether you want to create a reminder on read the previous one
    if 'create a reminder' in reminder:
        talk("what do you want me to remember?")
        data = take_command()
        remember = open('data.txt', 'w')  ## all the reminders are stored in data.txt file
        remember.write(data + '\n')
        remember.close()
        talk("You have asked to me remember that: " + data)
        print("You have asked to me remember that: " + data)
    elif 'tell me reminders' in reminder:
        remember = open('data.txt', 'r')
        for lines in remember:
            talk("You asked me to remember that " + lines)
            print("You asked me to remember that " + lines)
        remember.close()


##end
## This function will generate a ramdom pass on user's command
def password_generator():
    s1 = string.ascii_uppercase
    s2 = string.ascii_lowercase
    s3 = string.digits
    s4 = string.punctuation
    s = []
    s.extend(list(s1))
    s.extend(list(s2))
    s.extend(list(s3))
    s.extend(list(s4))
    random.shuffle(s)
    pass_len = 8
    new_password = ("".join(s[0:pass_len]))
    talk('Your new password is ' + new_password)
    print(new_password)


##end
## This function will flip a coin for toss and tell randomly whether head occurs or tails.
def flip_coin():
    talk("Flipping the coin")
    coin = ['head', 'tail']
    toss = []
    toss.extend(coin)
    random.shuffle(toss)
    result = ("".join(toss[0]))
    talk("the side of the coin is " + result)
    print("the side of the coin is " + result)


##end
## This function will randomly roll a dice and give output
def roll_dice():
    talk("rolling the dice")
    dice = random.randint(1, 6)
    talk("the number is : " + str(dice))
    print("the number is : " + str(dice))


##end
## tells the cpu being consumed
def cpu_usage():
    usage = psutil.cpu_percent()
    talk("cpu usage is :" + str(usage))
    print("cpu usage is :" + str(usage))


##end
##tells the battery percentage of computer
def battery_percentage():
    battery = psutil.sensors_battery()
    battery_per = battery.percent
    talk("battery percentage is :" + str(battery_per) + "%")
    print("battery percentage is :" + str(battery_per) + "%")


##end

##MAIN FUNCTION##
greet()  ## greet at first
while True:  ## loop will continue until user command with Thank you
    print("Listening")
    command = take_command()
    if 'jarvis' in command:  ## on jarvis the voice command will be activated
        command = command.replace('jarvis', '')  ## Replacing jarvis with empty string so only relevant part goes down
        if 'play' in command:
            command = command.replace('play',
                                      '')  ## Replacing now play with empty so that only the video name that's to be searched goes in the command.
            play_on_yt(command)
        elif 'who is' in command:
            command = command.replace('who is', '')  ## Same explanation as above
            get_meaning(command)
        elif 'tell me a' in command:
            talk(pyjokes.get_joke())
        elif 'send email' in command:
            send_email()
        elif 'send message' in command:
            send_whatsapp_message()
        elif 'open google' in command:
            search_on_google()
        elif 'tell weather' in command:
            get_weather()
        elif 'tell me some news' in command:
            get_news()
        elif 'read the copied text' in command:
            get_text_from_clipboard()
        elif 'give covid updates' in command:
            get_covid_update()
        elif 'open spotify' in command:
            open_spotify()
        elif 'take screenshot' in command:
            screenshot()
        elif 'open reminders' in command:
            reminders()
        elif 'generate password' in command:
            password_generator()
        elif 'flip' in command:
            flip_coin()
        elif 'dice' in command:
            roll_dice()
        elif 'cpu' in command:
            cpu_usage()
        elif 'battery' in command:
            battery_percentage()
        elif 'thank you' in command:  ## Program will stop if the user says thank you
            talk("you are welcome")
            break
