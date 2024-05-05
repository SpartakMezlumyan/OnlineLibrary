import flet as ft
from flet import *
from math import pi
import time
import csv

def check_credentials(username, password):
    with open('users.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if row[0] == username and row[1] == password:
                return True
        return False


class AnimatedBox(UserControl):
    def __init__(self, border_color, bg_color, rotate_angle):
        self.border_color = border_color
        self.bg_color = bg_color
        self.rotate_angle = rotate_angle
        super().__init__()

    def build(self):
        return Container(
            width=48,
            height=48,
            border=border.all(2.5, self.border_color),
            bgcolor=self.bg_color,
            border_radius=2,
            rotate=transform.Rotate(self.rotate_angle, alignment.center),
            animate_rotation=animation.Animation(700, "easeInOut"),
        )


class SignInButton(UserControl):
    def __init__(self, btn_name, username_input, password_input):
        self.btn_name = btn_name
        self.username_input = username_input
        self.password_input = password_input
        super().__init__()

    def build(self):
        return Container(
            content=ElevatedButton(
                content=Text(
                    self.btn_name,
                    size=13,
                    weight="bold",
                ),
                style=ButtonStyle(
                    shape={
                        "": RoundedRectangleBorder(radius=8),
                    },
                    color={
                        "": "black",
                    },
                    bgcolor={"": "#7df6dd"},
                ),
                height=42,
                width=320,
                on_click=self.sign_in_handler,
            ),
        )

    def sign_in_handler(self, e):
        if check_credentials(self.username_input, self.password_input):
            print("Вход выполнен успешно")
        else:
            error_message = Text("Неверное имя пользователя или пароль", size=12, color="red")
            self.controls.append(error_message)
            self.update()


class UserInputField(UserControl):
    def __init__(
            self,
            icon_name,
            text_hint,
            hide: bool,
            function_emails: bool,
            function_check: bool,
    ):
        self.icon_name = icon_name
        self.text_hint = text_hint
        self.hide = hide
        self.function_emails = function_emails
        self.function_check = function_check
        super().__init__()

    def return_email_prefix(self, e):
        email = self.controls[0].content.controls[1].value
        if e.control.data in email:
            pass
        else:
            self.controls[0].content.controls[1].value += e.control.data
            self.controls[0].content.controls[2].offset = transform.Offset(0.5, 0)
            self.controls[0].content.controls[2].opacity = 0
            self.update()

    def off_focus_input_check(self):
        return Container(
            opacity=0,
            offset=transform.Offset(0, 0),
            animate=200,
            border_radius=6,
            width=18,
            height=18,
            alignment=alignment.center,
            content=Checkbox(
                fill_color="#7df6dd",
                check_color="black",
                disabled=True,
            ),
        )

    def build(self):
        return Container(
            width=320,
            height=40,
            border=border.only(
                bottom=border.BorderSide(0.5, "white54"),
            ),
            border_radius=6,
            content=Row(
                spacing=20,
                vertical_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    Icon(
                        name=self.icon_name,
                        size=14,
                        opacity=0.85,
                    ),
                    TextField(
                        border_color="transparent",
                        bgcolor="transparent",
                        height=20,
                        width=200,
                        text_size=12,
                        content_padding=3,
                        cursor_color="white",
                        cursor_width=1,
                        color="white",
                        hint_text=self.text_hint,
                        hint_style=TextStyle(
                            size=11,
                        ),
                        password=self.hide,
                    ),
                    self.off_focus_input_check(),
                ],
            ),
        )


def mainlog(page: Page):
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.padding = padding.only(right=50)
    page.bgcolor = "#212328"

    username_input = ""
    password_input = ""

    page.add(
        Card(
            width=408,
            height=612,
            elevation=15,
            content=Container(
                bgcolor="#23262a",
                border_radius=6,
                content=Column(
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    controls=[
                        Divider(height=40, color="transparent"),
                        Stack(
                            controls=[
                                AnimatedBox("#e9665a", None, 0),
                                AnimatedBox("#7df6dd", "#23262a", pi / 4),
                            ]
                        ),
                        Divider(height=20, color="transparent"),
                        Column(
                            alignment=MainAxisAlignment.CENTER,
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                            spacing=5,
                            controls=[
                                Text("Sign In Youre Personal Library", size=22, weight="bold"),
                                Text(
                                    "School Online Library",
                                    size=13,
                                    weight="bold",
                                ),
                            ],
                        ),
                        Divider(height=30, color="transparent"),
                        UserInputField(
                            icons.PERSON_ROUNDED,
                            "Email",
                            False,
                            True,
                            True,
                        ),
                        Divider(height=1, color="transparent"),
                        UserInputField(
                            icons.LOCK_OUTLINE_ROUNDED,
                            "Password",
                            True,
                            False,
                            True,
                        ),
                        Divider(height=1, color="transparent"),
                        SignInButton("Sign In", username_input, password_input),  # Кнопка входа
                        Divider(height=35, color="transparent"),
                    ],
                ),
            ),
        )
    )
    page.update()

ft.app(target=mainlog)
