import tkinter as tk
from tkinter import *
import requests
from bs4 import BeautifulSoup as bs

class CurrencyConverter():
    def __init__(self, url):
        self.data = requests.get(url).json()
        self.currencies = self.data['rates']

m = tk.Tk()
m.title('Currency Converter')
m.geometry("600x400")  # Ekran boyutunu değiştirin
m.eval('tk::PlaceWindow . center')

# Arka plan
bg = tk.PhotoImage(file="bg.png")
label1 = tk.Label(m, image=bg)
label1.place(x=-100, y=-300)

# Ana çerçeve
main_frame = Frame(m)
main_frame.pack(expand=True)

Label(main_frame, text='Source Currency  :').grid(row=0, column=0, sticky='w')
Label(main_frame, text='Target Currency  :').grid(row=1, column=0, sticky='w')
Label(main_frame, text='Amount  :').grid(row=2, column=0, sticky='w')
Label(main_frame, text='Result  :').grid(row=8, column=0, sticky='w')

source_currency_entry = StringVar(m)
target_currency_entry = StringVar(m)

# Para birimi dropdown
url = 'https://api.exchangerate-api.com/v4/latest/USD'
currency_converter = CurrencyConverter(url)
currencies = currency_converter.currencies

popular_currencies = ['USD', 'EUR', 'TRY', 'GBP', 'JPY', 'CNY', 'CAD', 'AUD', 'CHF', 'SEK', 'NZD']
all_currencies = list(currencies.keys())
for currency in popular_currencies:
    if currency in all_currencies:
        all_currencies.remove(currency)
all_currencies = popular_currencies + all_currencies

source_currency_options = OptionMenu(main_frame, source_currency_entry, *all_currencies)
source_currency_entry.set("USD")
source_currency_options.config(bg="#2ECC71")
source_currency_options.grid(row=0, column=1)

target_currency_options = OptionMenu(main_frame, target_currency_entry, *all_currencies)
target_currency_entry.set("TRY")
target_currency_options.config(bg="#2ECC71")
target_currency_options.grid(row=1, column=1)

amount_entry = Entry(main_frame)
amount_entry.config(bg="#DFDFDF")
amount_entry.focus()
amount_entry.grid(row=2, column=1)

def clear():
    amount_entry.delete(0, END)
    result_label.config(text="")

def convert():
    source_currency = source_currency_entry.get()
    target_currency = target_currency_entry.get()
    amount = float(amount_entry.get())

    response = requests.get(f"https://www.x-rates.com/calculator/?from={source_currency}&to={target_currency}&amount=1")
    soup = bs(response.text, "html.parser")

    text1 = soup.find(class_="ccOutputTrail").previous_sibling
    text2 = soup.find(class_="ccOutputTrail").get_text(strip=True)
    rate = "{}{}".format(text1, text2)
    result = amount * float(rate)

    result_label.config(text=result)

result_label = Label(main_frame,font='Helvetica 10 bold', bg="#9FF71F")
result_label.grid(row=8, column=1)

button = tk.Button(main_frame, text='Convert', command=convert)
button.config(bg="#3498DB")
button.grid(row=3, column=1)

button2 = tk.Button(main_frame, text='Clear', command=clear)
button2.config(bg="#F4D03F")
button2.grid(row=4, column=1)

exit_button = tk.Button(main_frame, text='Exit', width=8, command=m.destroy, bg="#E74C3C")
exit_button.grid(row=5, column=1)

# Ana çerçeveyi sola hizala
main_frame.place(relx=0.5, rely=0.5, anchor='center')

m.mainloop()
