from PyQt6.QtWidgets import QMainWindow, QApplication, QTextEdit, QLineEdit, QPushButton
from backend import Chatbot
from backend import recognize_speech_from_mic
from audio_files import play, voice
import sys, threading
import speech_recognition as sr

class ChatbotWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #Starts backend chatbot
        self.chatbot = Chatbot()

        self.setMinimumSize(700, 500)

        # Adds chat area widget
        self.chat_area = QTextEdit(self)
        self.chat_area.setGeometry(10, 10, 480, 320)
        self.chat_area.setReadOnly(True)

        # Adds the input field widget
        self.input_field = QLineEdit(self)
        self.input_field.setGeometry(10, 340, 480, 40)
        self.input_field.returnPressed.connect(self.send_message)

        # Adds the submit button
        self.button = QPushButton("Send", self)
        self.button.setGeometry(500, 340, 100, 40)
        self.button.clicked.connect(self.send_message)

        # Adds the listen button
        self.button2 = QPushButton("Listen", self)
        self.button2.setGeometry(200, 380, 100, 60)
        self.button2.clicked.connect(self.send_listen_message)

        self.show()

    def send_message(self):
        user_input = self.input_field.text().strip()
        self.chat_area.append(f"<p style=color'color:#333333'>Me: {user_input}</p>")
        self.input_field.clear()

        # Allows for user input to be sent to interface before AI response is receieved

        thread = threading.Thread(target=self.get_bot_response, args=(user_input, ))
        thread.start()

    def send_listen_message(self):
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()
        mic_pickup = recognize_speech_from_mic(recognizer, microphone)
        listen_input = mic_pickup["transcription"]
        #user_input = self.input_field.text().strip()
        self.chat_area.append(f"<p style=color'color:#333333'>Me: {listen_input}</p>")
        self.input_field.clear()
        self.get_bot_response(listen_input)


    def get_bot_response(self, user_input):
        response = self.chatbot.get_response(user_input)
        self.chat_area.append(f"<p style='color:#333333; background-color: #E9E9E9'>Bot: {response} </p>")
        play(voice.generate_audio_bytes(response))

app = QApplication(sys.argv)
main_window = ChatbotWindow()
sys.exit(app.exec())
