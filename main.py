import pandas as pd
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from datetime import datetime
import os  # إضافة استيراد os


class InputCollector(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"

        self.input_area = TextInput(hint_text='PASTE HERE', size_hint_y=None, height=200)
        self.add_widget(self.input_area)

        buttons_layout = BoxLayout(size_hint_y=None, height=50)

        generate_button = Button(text="GENERATE", on_press=self.generate_data)
        buttons_layout.add_widget(generate_button)

        delete_button = Button(text="DELETE", on_press=self.delete_text)
        buttons_layout.add_widget(delete_button)

        self.add_widget(buttons_layout)

        self.message_label = Label(text="")
        self.add_widget(self.message_label)

    def generate_data(self, instance):
        input_text = self.input_area.text.replace('PASTE HERE', '').strip()
        input_values = input_text.split('\n')
        input_values = [value.strip() for value in input_values if value.strip()]

        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = {
            "Variable": [f"Variable{i + 1}" for i in range(len(input_values))],
            "Value": input_values,
            "Date": [current_date] * len(input_values)
        }
        df = pd.DataFrame(data)

        output_file = "input_values_with_date.csv"

        # التحقق من وجود الملف لتحديد ما إذا كنا بحاجة إلى كتابة الرأس أم لا
        if os.path.exists(output_file):
            header = False  # لا تكتب الرأس إذا كان الملف موجودًا بالفعل
        else:
            header = True  # اكتب الرأس إذا كان الملف جديدًا

        df.to_csv(output_file, mode='a', index=False, header=header, encoding='utf-8')

        self.message_label.text = f"Input values saved to {output_file}"

    def delete_text(self, instance):
        self.input_area.text = ""


class MyApp(App):
    def build(self):
        return InputCollector()


if __name__ == "__main__":
    MyApp().run()
