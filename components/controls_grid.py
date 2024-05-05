import flet as ft


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
        print("asdasd")

    def display(self):
        self.visible = True
        self.controls = []
        for grid_item in self.gallery.selected_control_group.grid_items:
            self.controls.append(
                ft.Container(
                    on_click=self.grid_item_clicked,
                    data=grid_item,
                    bgcolor=ft.colors.SECONDARY_CONTAINER,
                    border_radius=5,
                    padding=15,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.START,
                        vertical_alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.IconButton(ft.icons.ADD, tooltip="Add", icon_color=ft.colors.BLACK87),
                            ft.Text(
                                value=grid_item.name,
                                weight=ft.FontWeight.W_500,
                                size=14,
                            ),
                        ],
                    ),
                )
            )