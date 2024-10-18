

import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from random import randint, choice

kivy.require('2.0.0')

VALID_LICENSE_PLATES = ["ABC123", "XYZ789", "JKL456", "DILI2002"]
ALL_LICENSE_PLATES = VALID_LICENSE_PLATES + ["FAKE001", "INVALID9"]
AI_MEMORY = {}


class GarageDoor(BoxLayout):
    door_status = StringProperty("Closed")
    scanned_license_plate = StringProperty("")

    def __init__(self, **kwargs):
        super(GarageDoor, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10

        self.add_widget(Label(text="Smart Garage Door Opener", font_size='24sp', color=[0, 0, 1, 1]))

        self.status_label = Label(text="Door Status: " + self.door_status, font_size='20sp', color=[0, 0, 0, 1])
        self.add_widget(self.status_label)

        self.toggle_button = Button(text="Open Door", font_size='20sp', on_press=self.toggle_door, disabled=True,
                                    background_color=[0.2, 0.8, 0.2, 1])
        self.add_widget(self.toggle_button)

        self.license_input = TextInput(hint_text="Enter License Plate", multiline=False, font_size='18sp',
                                       background_color=[1, 1, 1, 1])
        self.add_widget(self.license_input)

        self.scan_button = Button(text="Scan License Plate", font_size='18sp', on_press=self.scan_license_plate,
                                  background_color=[0.4, 0.4, 0.9, 1])
        self.add_widget(self.scan_button)

        self.camera_button = Button(text="Camera Scan", font_size='18sp', on_press=self.camera_scan,
                                    background_color=[1, 0.5, 0, 1])
        self.add_widget(self.camera_button)

        self.alert_button = Button(text="Simulate Unexpected Activity", font_size='18sp',
                                   on_press=self.simulate_unexpected_activity, background_color=[0.9, 0.1, 0.1, 1])
        self.add_widget(self.alert_button)

        Clock.schedule_once(self.security_alert, 15)

    def toggle_door(self, instance):
        if self.door_status == "Closed":
            self.door_status = "Open"
            self.toggle_button.text = "Close Door"
        else:
            self.door_status = "Closed"
            self.toggle_button.text = "Open Door"
        self.update_status()

    def update_status(self):
        self.status_label.text = "Door Status: " + self.door_status

    def scan_license_plate(self, instance):
        license_plate = self.license_input.text.strip().upper()

        if license_plate in VALID_LICENSE_PLATES:
            self.scanned_license_plate = license_plate
            self.toggle_button.disabled = False
            self.learn_license_plate(license_plate)
            self.show_popup("License Plate Scanned", f"Valid License Plate: {license_plate}")
        else:
            self.scanned_license_plate = ""
            self.toggle_button.disabled = True
            self.learn_license_plate(license_plate)
            self.show_popup("License Plate Scanned", "Invalid License Plate!")

    def camera_scan(self, instance):
        scanned_plate = choice(ALL_LICENSE_PLATES)

        if scanned_plate in VALID_LICENSE_PLATES:
            self.scanned_license_plate = scanned_plate
            self.toggle_button.disabled = False
            self.learn_license_plate(scanned_plate)
            self.show_popup("Camera Scan", f"Detected Valid License Plate: {scanned_plate}")
        else:
            self.scanned_license_plate = ""
            self.toggle_button.disabled = True
            self.learn_license_plate(scanned_plate)
            self.show_popup("Camera Scan", f"Detected Invalid License Plate: {scanned_plate}")

    def learn_license_plate(self, license_plate):
        if license_plate in AI_MEMORY:
            AI_MEMORY[license_plate] += 1
        else:
            AI_MEMORY[license_plate] = 1
        print(f"AI Memory: {AI_MEMORY}")

    def show_popup(self, title, message):
        popup = Popup(title=title,
                      content=Label(text=message),
                      size_hint=(None, None), size=(300, 200))
        popup.open()

    def simulate_unexpected_activity(self, instance):
        popup = Popup(title='Security Alert!',
                      content=Label(text='Unexpected door activity detected!'),
                      size_hint=(None, None), size=(300, 200))
        popup.open()

    def security_alert(self, dt):
        if randint(0, 1) == 1:
            self.simulate_unexpected_activity(None)
        Clock.schedule_once(self.security_alert, 15)


class GarageApp(App):
    def build(self):
        return GarageDoor()


if __name__ == '__main__':
    GarageApp().run()