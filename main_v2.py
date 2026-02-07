# main.py
import keyboard


import Typer_v2.mapping
import Typer_v2.input


def main():
    print("Steno-style word cycler active.")
    print("Are you sure you want to quit?")
    print("Press ESC to quit.\n")

    keyboard.wait("esc")
    print("Exiting...")


if __name__ == "__main__":
    main()
