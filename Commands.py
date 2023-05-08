from enum import Enum
import pyttsx3
import pyautogui
import openai

"""
Function:
Handles command detection and execution
If a command is detected inside a phrase it will be removed from the phrase and executed
Multiple commands can be used in a single phrase

OBS: This class has no connection to the input system, it only deals with the string content already in memory 

"""

"""
The following functions execute the commands

"""
def cmdStartStoreSpeech(text):
        CommandsExecution.isStoringText = True
def cmdStopStoreSpeech(text):
        CommandsExecution.isStoringText = False
def cmdWriteStoredSpeech(text):
        print(CommandsExecution.storedText)
def cmdFreeStoredSpeech(text):
        CommandsExecution.storedText = ""
        print("Gravação limpa")
def cmdReadMemoryText(text):
     engine = pyttsx3.init()
     engine.say(CommandsExecution.storedText)
     engine.runAndWait()
     engine.stop()    

def cmdToggleWriteAsSpeak(text):
    pyautogui.typewrite(CommandsExecution.storedText)

def cmdFixWrittingText(args):
    API_KEY = open("API_KEY" ,"r").read()
    openai.api_key = API_KEY
    response = openai.ChatCompletion.create(

        model = "gpt-3.5-turbo",
        messages = [
            {"role" : "system", "content" : "Você é irá receber frases e arrumar os erros de escrita"},
            {"role" : "user", "content" : CommandsExecution.storedText}
        ]
    )
    CommandsExecution.storedText= response["choices"][0]["message"]["content"]

def cmdGenerateAIText(text):
    CommandsExecution.storedText=""

    API_KEY = open("API_KEY" ,"r").read()
    openai.api_key = API_KEY
    response = openai.ChatCompletion.create(

        model = "gpt-3.5-turbo",
        messages = [
            {"role" : "system", "content" : "Você irá criar um texto conforme solicidado"},
            {"role" : "user", "content" : text}
        ]
    )
    CommandsExecution.storedText= response["choices"][0]["message"]["content"]
    print(CommandsExecution.storedText)


def cmdAlterText(text):
    API_KEY = open("API_KEY" ,"r").read()
    openai.api_key = API_KEY
    response = openai.ChatCompletion.create(

        model = "gpt-3.5-turbo",
        messages = [
            {"role" : "system", "content" : "Você ira fazer o seguinte:" + text},
            {"role" : "user", "content" : CommandsExecution.storedText}
        ]
    )
    CommandsExecution.storedText= response["choices"][0]["message"]["content"]
    print(CommandsExecution.storedText)


"""
Each Key is a command and has its description and execution function
"""

CommandsTable = {
     
    "COMEÇAR A GRAVAR": {
        "description": "Store Speech inside memory",
        "command": cmdStartStoreSpeech
    },
    "LIMPAR GRAVAÇÃO": {
        "description": "Store Speech inside memory",
        "command": cmdFreeStoredSpeech
    },
    "PARAR DE GRAVAR": {
        "description": "Store Speech inside memory",
        "command": cmdStopStoreSpeech
    },
    "IMPRIMIR NO TERMINAL": {
        "description": "Write the stored speech",
        "command": cmdWriteStoredSpeech
    },
    "ESCREVER TEXTO SALVO": {
        "description": "Store Speech and write on selected box",
        "command": cmdToggleWriteAsSpeak
    },
    "LER TEXTO SALVO": {
        "description": "Read stored text",
        "command": cmdReadMemoryText
    },
    "ARRUMAR ORTOGRAFIA": {
        "description": "Read stored text",
        "command": cmdFixWrittingText
    },
    "CRIE UM TEXTO QUE": {
        "description": "Read stored text",
        "command": cmdGenerateAIText
    },
    "CRIE UM FILTRO QUE": {
        "description": "Read stored text",
        "command": cmdAlterText
    },
}




class CommandsExecution:
    """
    Handles the commands text input and execution
    
    """

    storedText = ""
    isStoringText = False
    isActive = True


    """Method that will receive a string and execute the commands"""
    @staticmethod
    def SpeechActions(inputString):
        CommandsExecution.store_text(inputString)
        commandsList = CommandsExecution.find_commands(inputString)
        for command in commandsList:
            CommandsExecution.storedText = CommandsExecution.storedText.lower().replace(command.lower(),'')
        for command in commandsList:
            CommandsExecution.execute_command(command,inputString)
        CommandsExecution.storedText.strip()

    """Stores the text in the current text buffer"""
    @staticmethod
    def store_text(inputString):
          if(CommandsExecution.isStoringText):
            CommandsExecution.storedText +=" "+ inputString


    """Identifies the commands within the new inserted phrase"""
    @staticmethod
    def find_commands(inputString):
        storeCommands = []
        for command in CommandsTable:
                if inputString.upper().find(command) >=0:
                    storeCommands.append(command)
        return storeCommands

    """Executes all the commands within the phrase"""
    @staticmethod
    def execute_command(command , text):
        if command in CommandsTable:
            f = CommandsTable[command]['command']
            f(text)
            pass
        else:
            # Mensagem de erro caso o comando não seja reconhecido
            print("Comando inválido")
