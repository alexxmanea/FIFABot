import datetime
import random
import threading
import time
from tkinter import *
from typing import Any

from pynput.keyboard import Key, Controller

app = Tk()
app_is_running = False
snipes_list = ["None", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
keyboard = Controller()
sleep_between_press_and_release_key = 0.25
stop_app_running = False
default_running_time = [14, 17]
print_time_interval_second = 120
row = 0
configurable_views_list = []
pause_time_minutes = [8, 11]

SEARCH_AND_BUY_KEY = "n"
BUY_KEY = "b"
SEND_TO_TRANSFER_KEY = "t"
SEND_TO_CLUB_KEY = "c"
LIST_KEY = "a"
BACK_KEY = Key.backspace
DOWN_PRICE_BUY = "3"
UP_PRICE_BUY = "4"
DOWN_PRICE_BID = "5"
UP_PRICE_BID = "6"
RESET_KEY = "r"


def window_configuration():
    app.title('FIFA Bot')
    app.geometry('800x950')
    app.configure(background='white')


def get_row():
    global row
    row = row + 1
    return row


def create_actions_group():
    global radio_group_option
    radio_group_option = IntVar()
    radio_group_option.set(1)

    Label(app, text="Actions", font=('Verdana', 15, 'bold'), background='white').grid(row=get_row(), column=0, sticky=W,
                                                                                      padx=30, pady=(20, 0))
    radio1 = Radiobutton(app, text="Buy and Send to My Club", variable=radio_group_option, value=1,
                         font=('Verdana', 14), background='white', command=set_radio_button_text_color)
    radio1.grid(row=get_row(), column=0, sticky=W, padx=30)
    # configurable_views_list.append(radio1)

    radio2 = Radiobutton(app, text="Buy and Send to Transfer List", variable=radio_group_option, value=2,
                         font=('Verdana', 14), background='white', command=set_radio_button_text_color)
    radio2.grid(row=get_row(), column=0, sticky=W, padx=30)
    # configurable_views_list.append(radio2)

    radio3 = Radiobutton(app, text="Buy and List on Transfer Market", variable=radio_group_option, value=3,
                         font=('Verdana', 14), background='white', command=set_radio_button_text_color)
    radio3.grid(row=get_row(), column=0, sticky=W, padx=30)
    # configurable_views_list.append(radio3)

    global radio_buttons
    radio_buttons = [radio1, radio2, radio3]

    set_radio_button_text_color()


def set_radio_button_text_color():
    for i, item in enumerate(radio_buttons):
        item.config(fg='black')
    radio_buttons[radio_group_option.get() - 1].config(fg='red')


def create_snipes_menu():
    get_row()
    Label(app, text="Loaded Snipe Filter", font=('Verdana', 15, 'bold'), background='white').grid(row=get_row(),
                                                                                                  column=0, sticky=W,
                                                                                                  padx=30, pady=(20, 0))

    global snipes_menu_value
    snipes_menu_value = StringVar(app)
    snipes_menu_value.set("None")

    option_menu = OptionMenu(app, snipes_menu_value, *snipes_list)
    option_menu.configure(width=10, height=1, font=('Verdana', 12))
    option_menu.grid(row=get_row(), column=0, sticky=W, padx=30, pady=10)
    configurable_views_list.append(option_menu)

    return snipes_menu_value


def create_time_textboxes():
    Label(app, text="Run time", font=('Verdana', 15, 'bold'), background='white').grid(row=get_row(), column=0,
                                                                                       sticky=W, padx=(30, 0),
                                                                                       pady=(20, 0))

    Label(app, text="Minimum minutes to run:", font=('Verdana', 12), background='white').grid(row=get_row(), column=0,
                                                                                              sticky=W, padx=(30, 0),
                                                                                              pady=(10, 0))

    global time_textbox_minimum
    time_textbox_minimum = Entry(app)
    time_textbox_minimum.configure(font=('Verdana', 12), background='white', width=30)
    time_textbox_minimum.grid(row=get_row(), column=0, sticky=W, padx=(30, 0), pady=(0, 10))
    configurable_views_list.append(time_textbox_minimum)

    Label(app, text="Maximum minutes to run:", font=('Verdana', 12), background='white').grid(row=get_row(), column=0,
                                                                                              sticky=W, padx=(30, 0),
                                                                                              pady=(10, 0))

    global time_textbox_maximum
    time_textbox_maximum = Entry(app)
    time_textbox_maximum.configure(font=('Verdana', 12), background='white', width=30)
    time_textbox_maximum.grid(row=get_row(), column=0, sticky=W, padx=(30, 0))
    configurable_views_list.append(time_textbox_maximum)


def create_pause_checkbox():
    global pause_checkbox_value
    pause_checkbox_value = IntVar()
    pause_checkbox = Checkbutton(app, text="Pause between runs", variable=pause_checkbox_value, onvalue=1, offvalue=0,
                                 width=20, bg='white')
    pause_checkbox.configure(font=('Verdana', 15), background='white')
    pause_checkbox.grid(row=get_row(), column=0, sticky=W, pady=(20, 0))
    pause_checkbox.select()
    configurable_views_list.append(pause_checkbox)


def create_speed_textbox():
    Label(app, text="Run speed (default = 1x)", font=('Verdana', 15, 'bold'), background='white').grid(row=get_row(),
                                                                                                       column=0,
                                                                                                       sticky=W,
                                                                                                       padx=(30, 0),
                                                                                                       pady=(20, 0))

    global speed_textbox
    speed_textbox = Entry(app)
    speed_textbox.configure(font=('Verdana', 12), background='white', width=30)
    speed_textbox.grid(row=get_row(), column=0, sticky=W, padx=(30, 0), pady=10)
    configurable_views_list.append(speed_textbox)


def create_log_listbox():
    listbox_frame = Frame(app, relief='sunken', bg="white")
    listbox_frame.grid(row=get_row(), column=0, sticky=W, padx=(30, 0), pady=(0, 10))

    label = Label(listbox_frame, text="Running Log", font=('Verdana', 15, 'bold'), background='white', pady=5)
    label.pack(anchor=W)

    global listbox
    listbox = Listbox(listbox_frame, width=90, font=('Verdana', 10))
    listbox.pack(side=LEFT, fill='both')

    scrollbar = Scrollbar(listbox_frame)
    scrollbar.pack(side=RIGHT, fill='both')

    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    global clear_log_button
    clear_log_button = Button(app, text="Clear Log", font=('Verdana', 12), command=clear_log)
    clear_log_button.grid(row=get_row(), column=0, sticky=W, padx=(30, 0), pady=(0, 10))
    clear_log_button.configure(width=13, height=1, pady=5)


def post_log_message(message):
    now = datetime.datetime.now()
    hour = str('%02d' % now.hour)
    minute = str('%02d' % now.minute)
    second = str('%02d' % now.second)
    timestamp = "  [" + hour + ":" + minute + ":" + second + "]: "
    to_print = timestamp + str(message)

    if message == "":
        listbox.delete(0, END)
        to_print = to_print + "Log Cleared."

    listbox.insert(END, to_print)
    listbox.see(END)


def clear_log():
    post_log_message("")


def create_run_button():
    global run_button

    run_button = Button(app, font=('Verdana', 12, 'bold'), command=push_run_button)
    run_button.grid(row=get_row(), column=0, sticky=SE, pady=(0, 10))
    run_button_change_text()
    run_button.configure(width=13, height=2)


def push_run_button():
    global app_is_running
    global stop_app_running

    run_button.config(state=DISABLED)

    if app_is_running:
        stop_app_running = True
    else:
        configurable_views_state(False)
        stop_app_running = False
        thread = threading.Thread(target=run_app, args=(lambda: stop_app_running,))
        thread.start()

    app_is_running = not app_is_running
    run_button_change_text()


def run_button_change_text():
    if app_is_running:
        run_button_string = "Stop"
    else:
        run_button_string = "Start"
    run_button.config(text=run_button_string)


def run_app(stop):
    while True:
        if stop():
            break

        post_log_message("Starting in 5 seconds...")
        time.sleep(5)
        run_button.config(state=NORMAL)

        if snipes_menu_value.get() != "None":
            press_and_release_key(RESET_KEY, None)
            post_log_message("Loading Sniping fliter " + snipes_menu_value.get() + "...")
            shift_press_and_release_key(snipes_menu_value.get())

        starting_time_millis = current_time_millis()
        elapsed_time_millis = 0

        minimum_time = default_running_time[0]
        maximum_time = default_running_time[1]
        if len(time_textbox_minimum.get()) > 0 and len(
                time_textbox_maximum.get()) > 0 and time_textbox_minimum.get().isnumeric() and time_textbox_maximum.get().isnumeric() and int(
            time_textbox_minimum.get()) < int(time_textbox_maximum.get()):
            minimum_time = int(time_textbox_minimum.get())
            maximum_time = int(time_textbox_maximum.get())
        run_for_seconds = random.randint(minimum_time * 60 + 1, maximum_time * 60 + 1)
        last_printed_time_millis = starting_time_millis

        post_log_message(
            "Will run for: " + seconds_to_time(run_for_seconds) + ", at " + str(get_running_speed()) + "x speed.")

        bid_or_buy_change = True
        buy_change = True
        bid_change = True
        while elapsed_time_millis < run_for_seconds * 1000:
            if stop():
                break

            if bid_or_buy_change:
                if bid_change:
                    press_and_release_key(UP_PRICE_BID, refresh_market_sleep)
                else:
                    press_and_release_key(DOWN_PRICE_BID, refresh_market_sleep)
                    press_and_release_key(DOWN_PRICE_BID, refresh_market_sleep)
                    press_and_release_key(DOWN_PRICE_BID, refresh_market_sleep)
                    bid_or_buy_change = not bid_or_buy_change
                bid_change = not bid_change
            else:
                if buy_change:
                    press_and_release_key(UP_PRICE_BUY, refresh_market_sleep)
                else:
                    press_and_release_key(DOWN_PRICE_BUY, refresh_market_sleep)
                    press_and_release_key(DOWN_PRICE_BUY, refresh_market_sleep)
                    press_and_release_key(DOWN_PRICE_BUY, refresh_market_sleep)
                    bid_or_buy_change = not bid_or_buy_change
                buy_change = not buy_change

            sleep_before_search()
            press_and_release_key(SEARCH_AND_BUY_KEY, sleep_after_search)

            scenario = radio_group_option.get()

            if scenario == 1:
                press_and_release_key(SEND_TO_CLUB_KEY, None)
                press_and_release_key(SEND_TO_CLUB_KEY, sleep_after_done_with_item)
                press_and_release_key(SEND_TO_TRANSFER_KEY, None)
                press_and_release_key(SEND_TO_TRANSFER_KEY, sleep_after_done_with_item)
            if scenario == 2:
                press_and_release_key(SEND_TO_TRANSFER_KEY, None)
                press_and_release_key(SEND_TO_TRANSFER_KEY, sleep_after_done_with_item)
            if scenario == 3:
                sleep_before_list()
                press_and_release_key(LIST_KEY, None)
                press_and_release_key(LIST_KEY, None)
                press_and_release_key(LIST_KEY, sleep_after_done_with_item)

            press_and_release_key(BACK_KEY, sleep_before_start_again)

            elapsed_time_millis = current_time_millis() - starting_time_millis

            if current_time_millis() - last_printed_time_millis > print_time_interval_second * 1000:
                post_log_message("Running for: " + seconds_to_time(elapsed_time_millis / 1000))
                last_printed_time_millis = current_time_millis()

        if stop():
            break

        if pause_checkbox_value.get() == 1:
            pause_time_millis = random.randint(pause_time_minutes[0] * 60 + 1, pause_time_minutes[1] * 60 + 1) * 1000
            pause_time_string = seconds_to_time(pause_time_millis / 1000)
            post_log_message("Paused for: " + pause_time_string + "...")

            paused_at_moment_millis = current_time_millis()
            elapsed_time_pause = 0

            while elapsed_time_pause < pause_time_millis:
                if stop():
                    break
                elapsed_time_pause = current_time_millis() - paused_at_moment_millis

    post_log_message("Stopped.")
    run_button.config(state=NORMAL)
    configurable_views_state(True)


def get_running_speed():
    if len(speed_textbox.get()) > 0 and is_float(speed_textbox.get()) and 1 <= float(speed_textbox.get()) <= 5:
        return float(speed_textbox.get())
    return 1


def refresh_market_sleep():
    time.sleep(random.randint(100, 200) / 1000 / float(get_running_speed()))


def sleep_before_search():
    time.sleep(random.randint(400, 600) / 1000 / float(get_running_speed()))


def sleep_after_search():
    time.sleep(random.randint(900, 1100) / 1000)


def sleep_after_done_with_item():
    time.sleep(random.randint(400, 600) / 1000 / float(get_running_speed()))


def sleep_before_list():
    time.sleep(random.randint(2400, 2600) / 1000 / float(get_running_speed()))


def sleep_before_start_again():
    time.sleep(random.randint(900, 1100) / 1000 / float(get_running_speed()))


def press_and_release_key(key, sleep_function):
    keyboard.press(key)
    time.sleep(sleep_between_press_and_release_key)
    keyboard.release(key)

    if sleep_function is not None:
        sleep_function()


def shift_press_and_release_key(key):
    with keyboard.pressed(Key.shift):
        keyboard.press(key)
        time.sleep(sleep_between_press_and_release_key)
        keyboard.release(key)
    keyboard.release(Key.shift)


def current_time_millis():
    return round(time.time() * 1000)


def seconds_to_time(seconds):
    return "[" + str('%02d' % (seconds / 3600)) + ":" + str('%02d' % ((seconds % 3600) / 60)) + ":" + str(
        '%02d' % (seconds % 60)) + "]"


def configurable_views_state(value):
    state = NORMAL
    if not value:
        state = DISABLED

    for view in configurable_views_list:
        view.configure(state=state)


def is_float(element: Any) -> bool:
    try:
        float(element)
        return True
    except ValueError:
        return False


if __name__ == '__main__':
    window_configuration()
    create_actions_group()
    create_snipes_menu()
    create_time_textboxes()
    create_pause_checkbox()
    create_speed_textbox()
    create_log_listbox()
    create_run_button()
    app.mainloop()
