import speech_recognition
import pyttsx3



import openai

from SpeechComprehension import SpeechTranscriber
from Commands import CommandsExecution


def main():


    Sc = SpeechTranscriber()
    while True:
        text = Sc.detect_speech()
        if(text != None):
            #No error
            CommandsExecution.SpeechActions(text)
        else:
            continue
main()