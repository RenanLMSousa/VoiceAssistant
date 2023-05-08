import speech_recognition
import pyttsx3

"""
Handles the voice to text conversion using the system default sound input and the google API
Takes a very short time to calibrate in each phrase, making it deal with ambient noise in a satisfying way

TODO: Add another method that can handle in real time transcription and is less internet dependent,
not only that, should be more precise

"""
class SpeechTranscriber:

    #isHearing
    def __init__(self):

        self.recognizer = speech_recognition.Recognizer()
        pass



    def detect_speech(self):
        try:
            with speech_recognition.Microphone() as mic:
                self.recognizer.adjust_for_ambient_noise(mic, duration = 1)
                audio = self.recognizer.listen(mic)

                text = self.recognizer.recognize_google(audio,language="pt-BR")
                text = text.lower()


                print(f"Recognized {text}")
                return text

        except speech_recognition.UnknownValueError:
            
            self.recognizer = speech_recognition.Recognizer()
            return None

        