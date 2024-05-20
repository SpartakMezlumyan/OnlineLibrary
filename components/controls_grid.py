import flet as ft
from db.queries import fetch_books
from getcode import generate_code


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

    def display(self):
        self.visible = True

        book_dialog = ft.AlertDialog(title=ft.Text(''), content=ft.Text(''), on_dismiss=lambda e: print("Dialog dismissed!"))
        code_dialog = ft.AlertDialog(title=ft.Text(''), on_dismiss=lambda e: print("Dialog dismissed!"))

        def close_banner(e):
            self.page.banner.open = False
            self.page.update()


        def open_dlg(e, book):
            self.page.dialog = book_dialog
            book_dialog.title.value = f"{book.author.full_name()} - {book.title}"
            book_dialog.content.value = book.description
            book_dialog.open = True
            self.page.update()

        def receive_code(e):
            self.page.dialog = code_dialog
            code_dialog.title.value = generate_code()
            code_dialog.open = True
            self.page.update()

        def show_banner_click(e, book):
            self.page.banner = ft.Banner(
                bgcolor=ft.colors.BLACK,
                leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER, size=40),
                content=ft.Text(
                    f"To receive a code for the {book.title} book or information about it, click the submit button"
                ),
                actions=[
                    ft.TextButton("Book Info", on_click=lambda e: open_dlg(e, book)),
                    ft.TextButton("Receive a code", on_click=receive_code),
                    ft.TextButton("Cancel", on_click=close_banner),
                ],
            )
            self.page.banner.open = True
            self.page.update()

        self.controls = []

        for book in fetch_books():
            self.controls.append(
                ft.Container(
                    # on_click=self.grid_item_clicked,
                    bgcolor=ft.colors.SECONDARY_CONTAINER,
                    border_radius=5,
                    width=250,
                    height=100,
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                alignment=ft.MainAxisAlignment.START,
                                controls=[
                                    ft.IconButton(
                                        ft.icons.INFO,
                                        tooltip="Information",
                                        icon_color=ft.colors.BLACK87,
                                        on_click=lambda e, b=book: show_banner_click(e, b),
                                        # data=book,
                                    ),
                                    ft.Text(
                                        value=book.title,
                                        weight=ft.FontWeight.W_500,
                                        size=14,
                                    ),
                                ],
                            ),
                        ],
                    ),
                )
            )