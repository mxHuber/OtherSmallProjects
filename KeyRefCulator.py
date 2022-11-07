import tkinter as tk

# variables

window = tk.Tk(className="KeyRefCulator")

keyPriceEntry = tk.Entry()
firstPriceEntry = tk.Entry()
secondPriceEntry = tk.Entry()
decimalToKeyRefEntry = tk.Entry()
keyHalfEntry = tk.Entry()
refHalfEntry = tk.Entry()

keyPriceInputLabel = tk.Label(text="What is the current price of keys in ref?")
firstPriceInputLabel = tk.Label(text="What is the price of the first item?")
secondPriceInputLabel = tk.Label(text="What is the price of the second item?")
differenceInputLabel = tk.Label(text="Difference in item prices")
decimalToKeyRefLabel = tk.Label(text="Convert decimal price to key/ref price")
keyRefToDecimalLabel = tk.Label(text="Convert key/ref price to decimal price")

keyPriceValue = 0
firstPriceValue = 0
secondPriceValue = 0
differenceValue = 0
decimalValue = 0
keyHalfValue = 0
refHalfValue = 0
keyRefConverted = 0


# Functions
def display_all_args(*args):
    counter = 0
    for x in args:
        x.grid(row=counter)
        counter += 1


# Get all widgets, code from StackOverflow
def all_children(window_to_use):
    _list = window_to_use.winfo_children()

    for item in _list:
        if item.winfo_children():
            _list.extend(item.winfo_children())

    return _list


# Clear every widget from the screen and also reset the entry's
def clear_all(window_to_use):
    # Clearing the widgets off the screen
    widget_list = all_children(window_to_use)
    for item in widget_list:
        item.grid_forget()


def enter_key_price():
    if keyPriceEntry.get() != "":
        global keyPriceValue
        keyPriceValue = float(keyPriceEntry.get())
        clear_all(window)
        keyPriceInputLabel.grid(row=1, column=1)
        keyPriceEntry.grid(row=2, column=1)
        keyPriceInputButton.grid(row=2, column=3)
        keyRefToDecimalLabel.grid(row=3, column=1)
        keyHalfEntry.grid(row=4, column=1)
        refHalfEntry.grid(row=4, column=2)
        convertToDecimalButton.grid(row=4, column=3)
        decimalToKeyRefLabel.grid(row=5, column=1)
        decimalToKeyRefEntry.grid(row=6, column=1)
        convertToKeyRefButton.grid(row=6, column=3)
        differenceInputLabel.grid(row=7, column=1)
        firstPriceEntry.grid(row=8, column=1)
        secondPriceEntry.grid(row=8, column=2)
        getDifferenceButton.grid(row=8, column=3)


def calculate_difference():
    if firstPriceEntry.get() != "" and secondPriceEntry != "":
        global firstPriceValue
        global secondPriceValue
        global differenceValue

        firstPriceValue = float(firstPriceEntry.get())
        secondPriceValue = float(secondPriceEntry.get())
        differenceValue = min(firstPriceValue, secondPriceValue)/max(firstPriceValue, secondPriceValue)
        tk.Label(text=str("%.3f" % differenceValue) + " difference").grid(row=8, column=4)


def convert_to_decimal():
    if keyHalfEntry.get() != "" and refHalfEntry.get() != "":
        global keyPriceValue
        global keyHalfValue
        global refHalfValue
        global keyRefConverted

        keyHalfValue = float(keyHalfEntry.get())
        refHalfValue = float(refHalfEntry.get())
        keyRefConverted = keyHalfValue + (refHalfValue/keyPriceValue)
        tk.Label(text=str("%.2f" % keyRefConverted + " keys")).grid(row=4, column=4)


def convert_to_key_ref():
    if decimalToKeyRefEntry.get() != "":
        global decimalValue
        decimalValue = float(decimalToKeyRefEntry.get())
        just_key_value = int(decimalValue)
        just_ref_value = decimalValue - just_key_value
        tk.Label(text=(str(just_key_value) + " keys " + str("%.2f" % (just_ref_value * keyPriceValue)) + " ref"))\
            .grid(row=6, column=4)


def display_key_price():
    if keyPriceValue != 0:
        keyPriceInputLabel.grid(row=1, column=1)


# Buttons
keyPriceInputButton = tk.Button(
    text="confirm",
    width=18,
    height=4,
    bg="orange",
    fg="black",
    command=lambda: enter_key_price()
)

convertToDecimalButton = tk.Button(
    text="convert",
    width=18,
    height=4,
    bg="orange",
    fg="black",
    command=lambda: convert_to_decimal()
)

convertToKeyRefButton = tk.Button(
    text="convert",
    width=18,
    height=4,
    bg="orange",
    fg="black",
    command=lambda: convert_to_key_ref()
)

getDifferenceButton = tk.Button(
    text="calculate",
    width=18,
    height=4,
    bg="orange",
    fg="black",
    command=lambda: calculate_difference()
)


# Application
class App:
    keyPriceInputLabel.grid(row=1)
    keyPriceEntry.grid(row=2, column=1)
    keyPriceInputButton.grid(row=2, column=2)

    window.mainloop()
