from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_symbols = [random.choice(symbols) for _ in range(random.randint(2, 4))]
    password_numbers = [random.choice(numbers) for _ in range(random.randint(2, 4))]

    password_list = password_letters + password_numbers + password_symbols
    random.shuffle(password_list)

    password_new = "".join(password_list)

    p_entry.delete(0, END)
    p_entry.insert(0, password_new)
    pyperclip.copy(password_new)

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = w_entry.get()
    email = e_entry.get()
    password = p_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty")
    else:
        try:
            with open("data.json", mode="r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", mode="w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            with open("data.json", mode="w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            w_entry.delete(0, END)
            p_entry.delete(0, END)


# ---------------------------- FIND PASSWORD ----------------------------#
def find_password():
    searched_website = w_entry.get()
    try:
        with open("data.json", mode="r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Oops", message="No data file found")
    else:
        if searched_website in data:
            searched_email = data[searched_website]["email"]
            searched_password = data[searched_website]["password"]
            messagebox.showinfo(title="Credentials", message=f"For {searched_website} website:\n"
                                                             f"email: {searched_email}\n"
                                                             f"password: {searched_password}")
        else:
            messagebox.showinfo(title="Oops", message="No data found for searched website.")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(pady=50, padx=50)

canvas = Canvas(width=200, height=200, highlightthickness=0)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)


# Labels
w_label = Label(text="Website:")
w_label.grid(column=0, row=1)

e_label = Label(text="Email/Username:")
e_label.grid(column=0, row=2)

p_label = Label(text="Password:")
p_label.grid(column=0, row=3)


# Entry
w_entry = Entry(width=24)
w_entry.grid(column=1, row=1)
w_entry.focus()

e_entry = Entry(width=42)
e_entry.grid(column=1, row=2, columnspan=2)
e_entry.insert(0, "username@email.com")

p_entry = Entry(width=24)
p_entry.grid(column=1, row=3)


# Buttons
search_button = Button(text="Search", width=14, command=find_password)
search_button.grid(column=2, row=1)

add_button = Button(text="Add", width=36, command=save)
add_button.grid(column=1, row=4, columnspan=2)

g_button = Button(text="Generate Password", command=generate_password)
g_button.grid(column=2, row=3)

window.mainloop()
