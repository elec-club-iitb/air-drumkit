import kivy
kivy.require('1.0.8')

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.core.audio import SoundLoader
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from kivy.clock import Clock

import serial


class AudioButton(Button):

    filename = StringProperty(None)
    sound = ObjectProperty(None, allownone=True)
    volume = NumericProperty(1.0)

    def on_press(self):
        if self.sound is None:
            self.sound = SoundLoader.load(self.filename)
        # stop the sound if it's currently playing
        if self.sound.status != 'stop':
            self.sound.stop()
        self.sound.volume = self.volume
        self.sound.play()

        self.state = 'down'
        Clock.schedule_once(self.reset_state, 300)

    def reset_state(self):
        self.state = 'up'

    def release_audio(self):
        if self.sound:
            self.sound.stop()
            self.sound.unload()
            self.sound = None

    def set_volume(self, volume):
        self.volume = volume
        if self.sound:
            self.sound.volume = volume


class AudioBackground(BoxLayout):
    pass


class AudioApp(App):

    def build(self):
        self.sound_buttons = []
        sounds = ['wavs/OH10.wav', 'wavs/CB.wav', 'wavs/CY0000.wav',
                  'wavs/MA.wav', 'wavs/SD0000.wav', 'wavs/SD0010.wav']

        root = AudioBackground(spacing=5)
        for i in range(6):
            btn = AudioButton(
                text='Audio ' + str(i+1), filename=sounds[i],
                size_hint=(None, None), halign='center',
                size=(128, 128), text_size=(118, None))
            root.ids.sl.add_widget(btn)
            self.sound_buttons.append(btn)

        self.serial = serial.Serial('/dev/ttyACM0')
        self.serial.timeout = 0.1

        Clock.schedule_once(self.read_from_serial)

        return root

    def release_audio(self):
        for audiobutton in self.root.ids.sl.children:
            audiobutton.release_audio()

    def set_volume(self, value):
        for audiobutton in self.root.ids.sl.children:
            audiobutton.set_volume(value)

    def read_from_serial(self, dt):
        c = self.serial.read()
        if c:
            print(c)
            i = ord(c) - 48
            if i < 6:
                self.sound_buttons[i].on_press()
        Clock.schedule_once(self.read_from_serial)

if __name__ == '__main__':
    AudioApp().run()
