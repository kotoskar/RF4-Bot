from cfg import *
import tkinter as tk


def main():
    root = tk.Tk()
    root.title("Settings")
    root.geometry("400x500")
    root.resizable(False, False)

    exit_hotkey_label = tk.Label(root, text="Exit hotkey")
    exit_hotkey_label.grid(row=0, column=0, padx=10, pady=10)
    exit_hotkey_entry = tk.Entry(root)
    exit_hotkey_entry.grid(row=0, column=1, padx=10, pady=10)
    exit_hotkey_entry.insert(0, EXIT_HOTKEY)

    telegram_id_label = tk.Label(root, text="Telegram ID")
    telegram_id_label.grid(row=1, column=0, padx=10, pady=10)
    telegram_id_entry = tk.Entry(root)
    telegram_id_entry.grid(row=1, column=1, padx=10, pady=10)
    telegram_id_entry.insert(0, TELEGRAM_ID)

    fish_filter_label = tk.Label(root, text="Fish filter")
    fish_filter_label.grid(row=2, column=0, padx=10, pady=10)
    fish_filter_var = tk.BooleanVar(value=FISH_FILTER)
    fish_filter_checkbox = tk.Checkbutton(root, variable=fish_filter_var)
    fish_filter_checkbox.grid(row=2, column=1, padx=10, pady=10)
    fish_filter_checkbox.select() if FISH_FILTER else fish_filter_checkbox.deselect()

    rise_label = tk.Label(root, text="Рыскание")
    rise_label.grid(row=3, column=0, padx=10, pady=10)

    time_rise_label = tk.Label(root, text="Время рывка")
    time_rise_label.grid(row=4, column=0, padx=10, pady=10)
    time_rise_entry = tk.Entry(root)
    time_rise_entry.grid(row=4, column=1, padx=10, pady=10)
    time_rise_entry.insert(0, TIME_RISE)

    tweeting_label = tk.Label(root, text="Твитчинг")
    tweeting_label.grid(row=5, column=0, padx=10, pady=10)

    time_between_tweeting_label = tk.Label(root, text="Время между рывками")
    time_between_tweeting_label.grid(row=6, column=0, padx=10, pady=10)
    time_between_tweeting_entry = tk.Entry(root)

    time_between_tweeting_entry.grid(row=6, column=1, padx=10, pady=10)
    time_between_tweeting_entry.insert(0, TIME_BETWEEN_TWEETING)

    time_tweeting_label = tk.Label(root, text="Время рывка")
    time_tweeting_label.grid(row=7, column=0, padx=10, pady=10)
    time_tweeting_entry = tk.Entry(root)
    time_tweeting_entry.grid(row=7, column=1, padx=10, pady=10)
    time_tweeting_entry.insert(0, TIME_TWEETING)

    jumping_label = tk.Label(root, text="Джиговая ступенька")
    jumping_label.grid(row=8, column=0, padx=10, pady=10)

    time_between_jumping_label = tk.Label(root, text="Время между рывками")
    time_between_jumping_label.grid(row=9, column=0, padx=10, pady=10)
    time_between_jumping_entry = tk.Entry(root)
    time_between_jumping_entry.grid(row=9, column=1, padx=10, pady=10)
    time_between_jumping_entry.insert(0, TIME_BETWEEN_JUMPING)

    time_jumping_label = tk.Label(root, text="Время рывка")
    time_jumping_label.grid(row=10, column=0, padx=10, pady=10)
    time_jumping_entry = tk.Entry(root)
    time_jumping_entry.grid(row=10, column=1, padx=10, pady=10)
    time_jumping_entry.insert(0, TIME_JUMPING)

    def save_settings():
        with open("cfg.py", "w") as f:
            f.write(f"EXIT_HOTKEY = '{exit_hotkey_entry.get()}'\n")
            f.write(f"TELEGRAM_ID = '{telegram_id_entry.get()}'\n")
            f.write(f"FISH_FILTER = {'True' if fish_filter_var.get() else 'False'}\n")
            f.write(f"TIME_RISE = {time_rise_entry.get()}\n")
            f.write(f"TIME_BETWEEN_TWEETING = {time_between_tweeting_entry.get()}\n")
            f.write(f"TIME_TWEETING = {time_tweeting_entry.get()}\n")
            f.write(f"TIME_BETWEEN_JUMPING = {time_between_jumping_entry.get()}\n")
            f.write(f"TIME_JUMPING = {time_jumping_entry.get()}\n")
        root.destroy()

    save_button = tk.Button(root, text="Save", command=save_settings)
    save_button.grid(row=11, column=0, columnspan=2, padx=10, pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
