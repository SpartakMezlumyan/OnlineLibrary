import flet as ft
import sqlite3
from getcode import *

conn = sqlite3.connect('/home/spartak/OnlineLibrary/SchoolLibraryBotDatabase/identifier.sqlite')
cur = conn.cursor()

cur.execute("SELECT * FROM books")
rows = cur.fetchall()

if rows:
    row = rows[0]
    for row in rows:
        title_text = f"{row[1]} {row[2]} --- {row[3]},\n {row[4]}"
        title = ft.Text(title_text)
else:
    print(False)


cur.close()
conn.close()

received_code = ft.Text(code)

class ControlsGrid(ft.GridView):
    def __init__(self, gallery):
        super().__init__()
        self.expand = 1
        self.runs_count = 5
        self.max_extent = 250
        self.child_aspect_ratio = 3.0
        self.spacing = 10
        self.run_spacing = 10
        self.gallery = gallery

    def grid_item_clicked(self, e):
        pass

    def display(self):
        self.visible = True

        def close_banner(e):
            self.page.banner.open = False
            self.page.update()

        def open_dlg(e):
            self.page.dialog = dlg
            dlg.open = True
            self.page.update()

        def receive_code(e):
            self.page.dialog = dlgr
            dlgr.open = True
            self.page.update()

        self.page.banner = ft.Banner(
            bgcolor=ft.colors.BLACK,
            leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER, size=40),
            content=ft.Text(
                "To receive a code for the book or information about it, click the submit button"
            ),
            actions=[
                ft.TextButton("Book Info", on_click=open_dlg),
                ft.TextButton("Receive a code", on_click=receive_code),
                ft.TextButton("Cancel", on_click=close_banner),
            ],
        )

        def show_banner_click(e):
            self.page.banner.open = True
            self.page.update()

        # self.page.add(ft.ElevatedButton("Show Banner", on_click=show_banner_click))

        dlg = ft.AlertDialog(title=title, on_dismiss=lambda e: print("Dialog dismissed!"))
        dlgr = ft.AlertDialog(title=received_code, on_dismiss=lambda e: print("Dialog dismissed!"))

        self.controls = []
        for row in rows:
            title_book = row[3]
            self.controls.append(
                ft.Container(
                    on_click=self.grid_item_clicked,
                    bgcolor=ft.colors.SECONDARY_CONTAINER,
                    border_radius=5,
                    width=250,
                    height=100,
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                alignment=ft.MainAxisAlignment.START,
                                controls=[
                                    ft.IconButton(ft.icons.INFO, tooltip="Information", icon_color=ft.colors.BLACK87,
                                                  on_click=show_banner_click),
                                    ft.Text(
                                        value=title_book,
                                        weight=ft.FontWeight.W_500,
                                        size=14,
                                    ),
                                ],
                            ),
                        ],
                    ),
                )
            )

