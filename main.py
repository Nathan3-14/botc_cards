import json
import os
from rich.console import Console
import tomllib

def select_from(options: list[str]) -> str:
    return options[select_index_from(options)]

def select_index_from(options: list[str]) -> int:
    current_option_index = 0
    while True:
        for index, option in enumerate(options):
            is_selected = index == current_option_index
            console.print("".join([
                "[green4 bold]\\[#] " if is_selected else "[ ] ",
                option,
                "[/green4 bold]" if is_selected else "",
            ]), highlight=False)
        action = input()
        match action:
            case "w":
                current_option_index -= 1
                if current_option_index < 0:
                    current_option_index = len(options) - 1
            case "s":
                current_option_index += 1
                if current_option_index >= len(options):
                    current_option_index = 0
            case "e":
                break

    return current_option_index

character_types = json.load(open("character_types.json", "r"))
character_colours = tomllib.load(open("config.toml", "rb"))["character_colours"]
console = Console()

class App:
    def __init__(self, scripts_path: str) -> None:
        self.scripts_path = scripts_path
        self.available_scripts = os.listdir(scripts_path)
        self.selected_script_index = 0
        self.selected_script = self.available_scripts[self.selected_script_index]
    
    def select_script(self) -> None:
        print("Selecting")
        self.selected_script_index = select_index_from(self.available_scripts)
        self.selected_script = self.available_scripts[self.selected_script_index]
    
    def wake(self) -> None:
        print("Waking")
        options = [
            "You are",
            "This Player is",
            "These Characters are not in play",
            "These Characters are in play",
            "This is the Demon",
            "These are your minions",
            "This ability has targeted you",
            "You have this ability",
            "-"
        ]
        characters = []
        for character in json.load(open(f"{self.scripts_path}/{self.selected_script}", "r")):
            if type(character) == dict:
                if character["id"] == "_meta":
                    continue
                characters.append(character["id"])
            else:
                characters.append(character)
        
        messages = [select_from(options)]
        while True:
            match select_from(["character", "exit"]):
                case "character":
                    message_character = select_from([*characters, "Done"])
                    if message_character != "Done":
                        messages.append("".join([
                            f"[{character_colours[character_types[message_character]]} bold]",
                            message_character,
                            f"[/{character_colours[character_types[message_character]]} bold]",
                        ]))
                case "exit":
                    break
        console.print(" ".join(messages))

if __name__ == "__main__":
    test = App("./scripts")
    test.select_script()
    test.wake()
    
        