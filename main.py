import customtkinter as tk
import threading
import time
from functionality.speech_recog import SpeechRecog
import queue

class App():
    def __init__(self):
        self.gui = tk.CTk()
        self.gui.title("Custom Tkinter")
        self.gui.geometry("300x200")
        self.prompt_label = tk.CTkLabel(self.gui, text="Press the button and say something...", pady=35)
        self.prompt_label.pack()
        self.start_button = tk.CTkButton(self.gui, text="Start", command=self.start)
        self.start_button.pack()
        self.output_label = tk.CTkLabel(self.gui, text="Readout here...", pady=35)
        self.output_label.pack()
        self.thread = None
        
        self.state_queue = queue.Queue()
        
        self.speech_recog = SpeechRecog(self.state_queue)

    def start(self):
        if self.thread is None:
            self.thread = threading.Thread(target=self.run_action)
            self.thread.start()
            self.check_queue()

    def check_queue(self):
        try:
            state = self.state_queue.get_nowait()  # Non-blocking check of the queue
            self.output_label.configure(text=state)  # Update the label with the new state
            print(f'GUI: Reflecting state change to {state}')
        except queue.Empty:
            pass  # No new state, do nothing

        if self.thread is not None and self.thread.is_alive():
            self.gui.after(100, self.check_queue)

    def run_action(self):
        self.output_label.configure(text=self.speech_recog.state)
        text = self.speech_recog.listen_for_speech()
        self.thread = None
        time.sleep(0.11) # sleep longer than the next tick of the "check_queue" function
        self.output_label.configure(text=text)


if __name__ == "__main__":
    app = App()
    app.gui.mainloop()