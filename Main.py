import speech_recognition as sr
import re
import pyttsx3
import time as t
from gtts import gTTS
import urllib.request
import urllib.parse
import webbrowser
import datetime

r = sr.Recognizer()
engine = pyttsx3.init()


def turnoff(thing):
    print("Turn off {}".format(thing))
    engine.say("Turn off".format(thing))
    engine.runAndWait()


def listen(music):
    regex = r'(.*?)song'
    matches = re.search(regex, music).group(1)
    query_string = urllib.parse.urlencode({"search_query": matches})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    link = "http://www.youtube.com/watch?v=" + search_results[0]
    print("Understood, I am searching your song")
    engine.say("Understood, I am searching your song")
    engine.runAndWait()
    webbrowser.open(link)


def set_timer(timer):
    time = 0
    pattern_int = r'[0-9]+'
    result = re.findall(pattern_int, timer)
    if result.__len__() == 1:
        if 'minute' in timer:
            result.append('0')
        if 'hour' in timer:
            result.extend(('0', '0'))
    if result.__len__() == 1:
        time = int(result[0])
        engine.say("Understood, I am setting the timer for {} seconds.".format(result[0]))
        engine.runAndWait()
    elif result.__len__() == 2:
        time = int(result[0]) * 60 + int(result[1])
        engine.say("Understood, I am setting the timer for {0}minutes and {1} seconds.".format(result[0], result[1]))
        engine.runAndWait()
    else:
        time = int(result[0]) * 3600 + int(result[1]) * 60 + int(result[2])
        engine.say(
            "Understood, I am setting the timer for {0}hours {1}minutes and {2} seconds.".format(result[0], result[1],
                                                                                                 result[2]))
        engine.runAndWait()
    for i in range(time):
        print(str(time - i) + " seconds remaining \n")
        t.sleep(1)
    print("Finished")
    engine.say("Finished")
    engine.setProperty('rate', 140)
    engine.setProperty('volumn', 0.9)
    engine.runAndWait()


def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


def reg_order(audio):
    try:
        print("Order : {}".format(r.recognize_google(audio)));
        order_list = r.recognize_google(audio)
        pattern = r'[a-zA-Z0-9]+'
        pattern_int = r'[0-9]+'
        result = re.findall(pattern, order_list)
        result_int = re.findall(pattern_int, order_list)
        dict_order_list = {'song': listen, 'timer': set_timer, 'dim': turnoff}
        dict_key = ['song', 'timer', 'dim']
        order = intersection(result, dict_key)
        for word in order:
            func_called = dict_order_list[word]
            func_called(order_list)
    except:
        pass


if __name__ == '__main__':
    currentTime = datetime.datetime.now()
    currentTime.hour
    if currentTime.hour < 12:
        engine.say('Good morning Sir, What can I help you?')
        print('Good morning Sir, What can I help you?')
        engine.runAndWait()
    elif 12 <= currentTime.hour < 18:
        engine.say('Good afternoon Sir, What can I help you?')
        print('Good afternoon Sir, What can I help you?')
        engine.runAndWait()
    else:
        engine.say('Good evening Sir, What can I help you?')
        print('Good evening Sir, What can I help you?')
        engine.runAndWait()
    while True:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print("Listening....")
            audio = r.listen(source)
            print("Done")
        reg_order(audio)
        continue
