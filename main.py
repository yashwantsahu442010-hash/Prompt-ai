import os
import threading
import requests

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label

try:
    from plyer import filechooser
except Exception:
    filechooser = None

# IMPORTANT: After deploying backend/app.py, replace this URL with your live HTTPS URL.
BACKEND_URL = "https://YOUR-BACKEND-URL.onrender.com/generate"

KV = """
<PromptScreen>:
    orientation: "vertical"
    padding: "18dp"
    spacing: "12dp"

    Label:
        text: "[b]StudyAI — AI Prompt Generator[/b]"
        markup: True
        font_size: "23sp"
        size_hint_y: None
        height: "48dp"
        color: 0.12, 0.20, 0.35, 1

    Label:
        text: "Photo ya audio chunein aur AI se prompt banwayein."
        font_size: "15sp"
        size_hint_y: None
        height: "38dp"
        color: 0.25, 0.28, 0.32, 1

    Button:
        text: "📷  Photo select karein"
        size_hint_y: None
        height: "50dp"
        on_release: root.pick_file("image")

    Button:
        text: "🎙  Audio select karein"
        size_hint_y: None
        height: "50dp"
        on_release: root.pick_file("audio")

    Label:
        text: root.selected_text
        size_hint_y: None
        height: "42dp"
        text_size: self.width, None
        halign: "left"
        valign: "middle"
        color: 0.18, 0.35, 0.22, 1

    Button:
        text: "Prompt generate karein"
        size_hint_y: None
        height: "52dp"
        disabled: not root.file_path or root.busy
        on_release: root.generate_prompt()

    Label:
        text: root.status_text
        size_hint_y: None
        height: "36dp"
        text_size: self.width, None
        halign: "left"
        valign: "middle"
        color: 0.25, 0.28, 0.32, 1

    Label:
        text: "[b]Generated prompt[/b]"
        markup: True
        size_hint_y: None
        height: "28dp"
        halign: "left"
        color: 0.12, 0.20, 0.35, 1

    TextInput:
        id: output_box
        text: root.prompt_text
        hint_text: "Aapka prompt yahan dikhega..."
        multiline: True
        readonly: False
        size_hint_y: 1

    Button:
        text: "Prompt copy karein"
        size_hint_y: None
        height: "48dp"
        disabled: not root.prompt_text
        on_release: root.copy_prompt()
"""

class PromptScreen(BoxLayout):
    file_path = StringProperty("")
    selected_text = StringProperty("Abhi koi file select nahi ki gayi.")
    status_text = StringProperty("Ready")
    prompt_text = StringProperty("")
    busy = BooleanProperty(False)
    file_kind = ""

    def pick_file(self, kind):
        if filechooser is None:
            self.show_message("File picker available nahi hai. App ko Android par chalayein.")
            return
        self.file_kind = kind
        try:
            if kind == "image":
                filechooser.open_file(
                    on_selection=lambda selection: self.on_file_selected(selection),
                    filters=["*.png", "*.jpg", "*.jpeg", "*.webp"]
                )
            else:
                filechooser.open_file(
                    on_selection=lambda selection: self.on_file_selected(selection),
                    filters=["*.mp3", "*.m4a", "*.wav", "*.ogg", "*.webm", "*.mp4"]
                )
        except Exception as exc:
            self.show_message("File picker kholne mein dikkat: " + str(exc))

    def on_file_selected(self, selection):
        if not selection:
            return
        path = selection[0]
        if not os.path.isfile(path):
            self.show_message("Selected file nahi mili.")
            return
        self.file_path = path
        self.selected_text = "Selected: " + os.path.basename(path)
        self.status_text = "File ready hai."

    def generate_prompt(self):
        if not self.file_path:
            self.show_message("Pehle photo ya audio select karein.")
            return
        if "YOUR-BACKEND-URL" in BACKEND_URL:
            self.show_message(
                "Pehle main.py mein BACKEND_URL ko apne deployed backend ke HTTPS URL se replace karein."
            )
            return
        self.busy = True
        self.status_text = "AI prompt bana raha hai... thoda intezar karein."
        threading.Thread(target=self._send_file, daemon=True).start()

    def _send_file(self):
        try:
            with open(self.file_path, "rb") as file_obj:
                response = requests.post(
                    BACKEND_URL,
                    files={"file": (os.path.basename(self.file_path), file_obj)},
                    data={"kind": self.file_kind},
                    timeout=180
                )
            if response.status_code != 200:
                try:
                    message = response.json().get("error", "Server error")
                except Exception:
                    message = "Server error: " + str(response.status_code)
                raise RuntimeError(message)
            data = response.json()
            prompt = data.get("prompt", "").strip()
            if not prompt:
                raise RuntimeError("Server ne khaali prompt bheja.")
            Clock.schedule_once(lambda _dt: self._show_result(prompt), 0)
        except Exception as exc:
            message = str(exc)
            Clock.schedule_once(lambda _dt: self._show_error(message), 0)

    def _show_result(self, prompt):
        self.prompt_text = prompt
        self.ids.output_box.text = prompt
        self.status_text = "Prompt taiyar hai. Aap ise edit ya copy kar sakte hain."
        self.busy = False

    def _show_error(self, message):
        self.status_text = "Prompt nahi ban saka."
        self.busy = False
        self.show_message(
            "Error: " + message + "\n\nInternet aur backend URL check karein."
        )

    def copy_prompt(self):
        text = self.ids.output_box.text.strip()
        if not text:
            return
        try:
            from kivy.core.clipboard import Clipboard
            Clipboard.copy(text)
            self.status_text = "Prompt clipboard par copy ho gaya."
        except Exception:
            self.show_message("Copy nahi hua. Text box mein prompt select karke copy karein.")

    def show_message(self, message):
        popup = Popup(
            title="StudyAI",
            content=Label(text=message, halign="center", valign="middle"),
            size_hint=(0.88, 0.42)
        )
        popup.open()


class StudyAIApp(App):
    def build(self):
        Builder.load_string(KV)
        return PromptScreen()


if __name__ == "__main__":
    StudyAIApp().run()
