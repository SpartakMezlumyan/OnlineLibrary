import flet as ft


class ExamplesView(ft.Column):
    def __init__(self, gallery):
        super().__init__()
        self.gallery = gallery
        self.visible = False
        self.expand = True
        self.control_name_text = ft.Text(style=ft.TextThemeStyle.HEADLINE_MEDIUM)
        self.control_description = ft.Text(style=ft.TextThemeStyle.BODY_MEDIUM)
        self.examples = ft.Column(expand=True, spacing=10, scroll=ft.ScrollMode.AUTO)
        self.controls = [
            self.control_name_text,
            self.control_description,
            self.examples,
        ]

    def display(self, grid_item):
        self.visible = True
        self.examples.controls = []
        self.control_name_text.value = grid_item.name
        self.control_description.value = grid_item.description

        for example in grid_item.examples:
            self.examples.controls.append(
                ft.Column(
                    controls=[
                        ft.Container(
                            content=example.example(),
                            clip_behavior=ft.ClipBehavior.NONE,
                        ),
                    ],
                )
            )