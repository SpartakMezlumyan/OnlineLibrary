import flet as ft

def main(page: ft.Page):
    page.title = "Registration Form"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    def register_user(e):
        # Here you can add the logic for registering the user
        print("User registered")

    page.add(
        ft.Column(
            [
                ft.Text("Registration Form"),
                ft.TextField(label="Username"),
                ft.TextField(label="Email"),
                ft.TextField(label="Password", password=True),
                ft.ElevatedButton(text="Register", on_click=register_user),
            ]
        )
    )

ft.app(target=main)