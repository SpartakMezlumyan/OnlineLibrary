import flet as ft
import sqlite3

def mains(page: ft.Page):
    page.title = "SchoolLibrary"
    page.theme_mode = 'dark'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_width = 400
    page.window_height = 350

    x = True

    def auth_user(e):
        db_path = '/home/spartak/DataGripProjects/UsersDataBase/identifier.sqlite'
        db = sqlite3.connect(db_path)
        cur = db.cursor()
        cur.execute(f"SELECT * FROM users WHERE email = '{user_login.value}' AND'{user_pass.value}'")
        if cur.fetchone() != None:
            user_login.value = ''
            user_pass.value = ''
            btn_auth.text = 'Added'

            if len(page.navigation_bar.destinations) == 2:
                page.navigation_bar.destinations.append(ft.NavigationDestination(
                    icon=ft.icons.BOOK,
                    label='Cabinet',
                    selected_icon=ft.icons.BOOKMARK
                ))
            page.update()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Непровильно написона данные"))
            page.snack_bar.open = True
            page.update()

        db.commit()
        db.close()

        user_login.value = ''
        user_pass.value = ''
        btn_auth.text = 'Added'
        page.update()

    def validate(e):
        if all([user_login.value, user_pass.value]):
            btn_auth.disabled = False
        else:
            btn_auth.disabled = True

        page.update()

    user_login = ft.TextField(label='Login', width=270, on_change=validate)
    user_pass = ft.TextField(label='Password', width=270, password=True, on_change=validate)
    btn_auth = ft.OutlinedButton(text='Add', width=270, on_click=auth_user)

    panel_registration = ft.Row(
        [
            ft.Column(
                [
                    ft.Text("Registration"),
                    user_login,
                    user_pass,
                    btn_auth
                ]
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

    panel_logining = ft.Row(
        [
            ft.Column(
                [
                    ft.Text("Sing In"),
                    user_login,
                    user_pass,
                    btn_auth
                ]
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

    panel_cabinet = ft.Row(
        [
            ft.Column(
                [
                    ft.Text("Cabinet"),
                ]
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )
    def navigate(e):
        index = page.navigation_bar.selected_index
        page.clean()

        if index == 0: page.add(panel_registration)
        elif index == 1: page.add(panel_logining)
        elif index == 2: page.add(panel_cabinet)

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.VERIFIED_USER, label="Registration"),
            ft.NavigationDestination(icon=ft.icons.VERIFIED_USER_OUTLINED, label="Sing In")
        ], on_change=navigate
    )

    page.add(panel_registration)

ft.app(target=mains)