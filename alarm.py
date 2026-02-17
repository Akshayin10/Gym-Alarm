from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from datetime import datetime

class AlarmLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=15, padding=30, **kwargs)

        self.title = Label(
            text=' Gym Alarm ',
            font_size=32,
            size_hint=(1, 0.2),
            color=(0, 1, 0.6, 1)
        )
        self.add_widget(self.title)

        self.hour_input = TextInput(
            hint_text='Hour (0-23)',
            input_filter='int',
            multiline=False,
            font_size=24,
            size_hint=(1, 0.15)
        )
        self.add_widget(self.hour_input)

        self.minute_input = TextInput(
            hint_text='Minute (0-59)',
            input_filter='int',
            multiline=False,
            font_size=24,
            size_hint=(1, 0.15)
        )
        self.add_widget(self.minute_input)

        self.set_button = Button(
            text='Set Alarm',
            font_size=24,
            background_color=(0, 1, 0.6, 1),
            size_hint=(1, 0.2)
        )
        self.set_button.bind(on_press=self.set_alarm)
        self.add_widget(self.set_button)

        self.status = Label(
            text='',
            font_size=20,
            size_hint=(1, 0.3)
        )
        self.add_widget(self.status)

        self.alarm_set = False
        self.alarm_hour = None
        self.alarm_minute = None

        self.sound = SoundLoader.load('alarm.mp3')
        Clock.schedule_interval(self.check_alarm, 1)

    def set_alarm(self, instance):
        try:
            hour = int(self.hour_input.text)
            minute = int(self.minute_input.text)

            if not (0 <= hour < 24 and 0 <= minute < 60):
                raise ValueError

            self.alarm_hour = hour
            self.alarm_minute = minute
            self.alarm_set = True
            self.status.text = f'⏰ Alarm set for {hour:02}:{minute:02}'

        except ValueError:
            self.status.text = '❌ Invalid time format. Use 24-hour format.'

    def check_alarm(self, dt):
        if self.alarm_set:
            now = datetime.now()
            if now.hour == self.alarm_hour and now.minute == self.alarm_minute:
                self.status.text = "🚨 Time to Work Out! 💪"
                if self.sound:
                    self.sound.play()
                self.alarm_set = False

class GymAlarmApp(App):
    def build(self):
        return AlarmLayout()

if __name__ == '__main__':
    GymAlarmApp().run()