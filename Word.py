import speech_recognition as sr
import pyttsx3
import re
from openai import OpenAI
import keyboard
import time
import random
import requests
from pydub import AudioSegment
from pydub.playback import play

transcript = ""
engine = pyttsx3.init()
word = ""
end_character = "p" # the character that will end the program
cheat_character = "7" # the character that will skip the punishment if the word is not recognized correctly
def word_definition():
    global word
    global engine
    word= ""
    word_definition = ""
    api_url = 'https://api.api-ninjas.com/v1/randomword'
    response = requests.get(api_url, headers={'X-Api-Key': 'UfRiEbyPPCYoFjQ7Iy+1EA==1QBM1NkHKQk9lEoO'})
    if response.status_code == requests.codes.ok:
        word = response.text
        print(response.text)
    else:
        print("Error:", response.status_code, response.text)
    print(f"Word: {word}")
    # get the word definition from the AI
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key="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",
    )
    completion = client.chat.completions.create(
    
        model="deepseek/deepseek-prover-v2:free",
        
        messages=
        [
          {
            "role": "user",
            "content": ("Please define this word " + str(word) + " in a short paragraph, you can use any words, don't use the word in a sentence. DEFINE ONLY " + str(word) +", don't use any special characters or special ways of displaying.")
            }
        ]
    )
    
    try:
        word_definition = completion.choices[0].message.content
        print(completion.choices[0].message.content)
    except Exception as e:
        print("Error accessing response:", e)
        print("Full response:", completion)
    # Have it tts the ai response
    engine.say(word_definition)
    engine.runAndWait()
    # word = re.search(r'\*\*(.*?)\*\*', completion.choices[0].message.content, re.IGNORECASE).group(1)
    print(f"Word: {word}")
    return word_definition

def audio_from_mic():
    global transcript
    transcript = ""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        past_time = time.time()
        delta_time = 60
        recognizer.adjust_for_ambient_noise(source)
        while(time.time() - past_time <= delta_time):
            if keyboard.is_pressed(end_character):
                print("Exiting audio recording.")
                return
            try:
                audio = recognizer.listen(source)
                transcript = transcript + " " + recognizer.recognize_google(audio)
                print("You said:", transcript)
            except sr.UnknownValueError:
                print("Sorry, I did not understand that.")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
        print("Final transcript:", transcript.strip())
        return transcript
def bad_thing():
    past_time = time.time()
    delta_time = 60
    possible_keys = ['w', 'a', 's', 'd', 'i', 'space', 'j', 'f','k','q','e'] # change this to whatever keys you want the program to press randomly, default is controls for blazeblue entrophy effect
    keyboard.press('alt + f4')  # Example of a bad thing, you can change this to whatever you want SUGGESTED BY COPILOT NOT ME BTW!
    play(AudioSegment.from_mp3("Vine boom.mp3"))  

    # while(time.time() - past_time <= delta_time):
    #     if keyboard.is_pressed(end_character):
    #         print("Exiting bad thing loop.")
    #         return
    #     if keyboard.is_pressed(cheat_character):
    #         engine.say("Skipping punishment. L")
    #         engine.runAndWait()
    #         return
    #     keyboard.press_and_release(random.choice(possible_keys))
    #     time.sleep(0.2)  # Adjust the delay as needed to control the frequency of key presses

def WordCheck():
    global engine
    global word
    global transcript
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key="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",
    )
    completion = client.chat.completions.create(
    
        model="deepseek/deepseek-prover-v2:free",
        
        messages=
        [
          {
            "role": "user",
            "content": (f"Check if the word '{word}' is used correctly in the following, try to be a little lenient if the word is spelled wrong or if it's pronounced similarly. HOWEVER, be critical, but fair if the usage of the word, if its used incorrectly yell at the user. Please only say if it's correct or incorrect once, and do not say both. Here is the transcript of someone speaking: {transcript}. If it is used correctly, respond with 'Correct'. If it is not used correctly, respond with 'Incorrect' keep it short, less than 2 sentences!")
            }
        ]
    )
    try:
        check = (completion.choices[0].message.content).lower()
        print(f"AI Response: {check}")
        # print(completion.choices[0].message.content)
        engine.say(completion.choices[0].message.content)
        engine.runAndWait()

    except Exception as e:
        print("Error accessing response:", e)
        print("Full response:", completion)
    if ("incorrect" in check) and word:
        print("The word was not used correctly.")
        engine.say("FAILURE")
        engine.runAndWait()
        bad_thing()
    else:
        print("The word was used correctly.")
        engine.say("SUCCESS")
        engine.runAndWait()
        return True


def main():
    word_definition()
    engine.say("Time Start!")
    engine.runAndWait()
    # listen to my microphone for a minute and transcribe the audio
    audio_from_mic()
    # AI checks if the word is used correctly in the transcription
    WordCheck()
    # if not used correctly, it will do something negative to you (like inverse controls or input random controls)

while keyboard.read_key() != end_character:
    main()
    time.sleep(120)
# sometimes the voice program will just not understand the word in this case I have made a cheat key to skip the punishment