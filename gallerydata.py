import importlib.util
import os
import sys
from os.path import isfile, join
from pathlib import Path

import flet as ft


class GridItem:
    def __init__(self, id):
        self.id = id
        self.name = None
        self.examples = []
        self.description = None


class ExampleItem:
    def __init__(self):
        self.name = None
        self.file_name = None
        self.order = None
        self.example = None
        # self.source_code = None


class ControlGroup:
    def __init__(self, name, label, icon, selected_icon, index):
        self.name = name
        self.label = label
        self.icon = icon
        self.selected_icon = selected_icon
        self.grid_items = []
        self.index = index

    # def find_grid_item(self, name):
    #     for grid_item in self.grid_items:
    #         if grid_item.name == name:
    #             return grid_item


class GalleryData:
    def __init__(self):
        self.control_groups = [
            ControlGroup(
                name="layout",
                label="Cabinet",
                icon=ft.icons.ACCOUNT_CIRCLE,
                selected_icon=ft.icons.ACCOUNT_CIRCLE,
                index=0,
            ),
            ControlGroup(
                name="navigation",
                label="Books",
                icon=ft.icons.BOOK,
                selected_icon=ft.icons.BOOK,
                index=1,
            ),
            # ControlGroup(
            #     name="displays",
            #     label="Writers",
            #     icon=ft.icons.MAN,
            #     selected_icon=ft.icons.MAN,
            #     index=2,
            # ),
            # ControlGroup(
            #     name="dialogs",
            #     label="Dialogs",
            #     icon=ft.icons.MESSAGE_SHARP,
            #     selected_icon=ft.icons.MESSAGE_SHARP,
            #     index=5,
            # ),
        ]
        self.import_modules()
        self.selected_control_group = self.control_groups[0]

    def get_control_group(self, control_group_name):
        for control_group in self.control_groups:
            if control_group.name == control_group_name:
                return control_group

    def get_control(self, control_group_name, control_name):
        control_group = self.get_control_group(control_group_name)
        for grid_item in control_group.grid_items:
            if grid_item.id == control_name:
                return grid_item

    def list_control_dirs(self, dir):
        file_path = os.path.join(str(Path(__file__).parent), "examples", dir)
        try:
            control_dirs = [
                f
                for f in os.listdir(file_path)
                if os.path.isdir(os.path.join(file_path, f)) and f not in ["index.py", "images", "__pycache__", ".venv", ".git"]
            ]
            return control_dirs
        except FileNotFoundError:
            print(f"Directory '{file_path}' not found.")
            return []

    def list_example_files(self, control_group_dir, control_dir):
        file_path = os.path.join(
            str(Path(__file__).parent), "examples", control_group_dir, control_dir
        )
        try:
            example_files = [f for f in os.listdir(file_path) if not f.startswith("_")]
            return example_files
        except FileNotFoundError:
            print(f"Directory '{file_path}' not found.")
            return []

    def import_modules(self):
        for control_group_dir in self.control_groups:
            for control_dir in self.list_control_dirs(control_group_dir.name):
                grid_item = GridItem(control_dir)

                for file in self.list_example_files(
                    control_group_dir.name, control_dir
                ):
                    file_name = os.path.join(control_group_dir.name, control_dir, file)
                    module_name = file_name.replace("/", ".").replace(".py", "")

                    if module_name in sys.modules:
                        print(f"{module_name!r} already in sys.modules")
                    else:
                        file_path = os.path.join(
                            str(Path(__file__).parent), "examples", file_name
                        )

                        try:
                            spec = importlib.util.spec_from_file_location(
                                module_name, file_path
                            )
                            module = importlib.util.module_from_spec(spec)
                            sys.modules[module_name] = module
                            spec.loader.exec_module(module)
                            print(f"{module_name!r} has been imported")
                            if file == "index.py":
                                grid_item.name = module.name
                                grid_item.description = module.description
                            else:
                                example_item = ExampleItem()
                                example_item.example = module.example

                                example_item.file_name = (
                                    module_name.replace(".", "/") + ".py"
                                )
                                example_item.name = module.name
                                example_item.order = file[
                                    :2
                                ]
                                grid_item.examples.append(example_item)
                        except FileNotFoundError:
                            print(f"File '{file_path}' not found.")
                            continue
                        except Exception as e:
                            print(f"Error importing module '{module_name}': {e}")
                            continue
                grid_item.examples.sort(key=lambda x: x.order)
                control_group_dir.grid_items.append(grid_item)
            control_group_dir.grid_items.sort(key=lambda x: x.name)
