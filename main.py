import tkinter as tk
from tkinter import ttk
from tkinter import Menu, StringVar, messagebox
from tkinter.constants import CENTER
from pycoingecko import CoinGeckoAPI
from PIL import Image, ImageTk
import pandas as pd
import re
import requests
from datetime import datetime
import matplotlib.pyplot as plt
import subprocess


win = tk.Tk()
win.title("Cryptocurrency Center")
win.geometry("640x480")
win.resizable(0, 0)
win.tk.call("source", "azure.tcl")
win.tk.call("set_theme", "dark")

cg = CoinGeckoAPI()


def get_price(crypto_name):
    try:
        x = cg.get_price(ids=crypto_name, vs_currencies='usd')
    except requests.exceptions.ConnectionError:
        messagebox.showerror("Warning", "No internet or connection error! Please restart your applications!")
        _quit()

    return str(x[crypto_name]['usd'])


def forgetAllScene():
    crypto_rates_frame.grid_forget()
    buttonLabel.grid_forget()
    firstLabel.grid_forget()
    crypto_exchanges_frame.grid_forget()
    crypto_info_frame.grid_forget()
    crypto_convert_frame.grid_forget()


def _msgBoxHelp():
    messagebox.showinfo('Help', "Application made with CoingeckoAPI.\nIf you need help, please contact us via e-mail.")


def _quit():
    win.quit()
    win.destroy()
    exit()


def dark_theme():
    win.tk.call("set_theme", "dark")


def light_theme():
    win.tk.call("set_theme", "light")


def onChange(event):
    logo = Image.open('images/bitcoin_logo.jpg')
    logo = ImageTk.PhotoImage(logo)
    logo_label = tk.Label(firstLabel, image=logo)
    logo_label.image = logo
    logo_bitcoin.grid(column=1, row=1, columnspan=3)
    logo_label.grid(column=1, row=1)
    firstLabel.grid(column=1, row=1, columnspan=3)


# Mainpage (firstLabel)
logo_bitcoin = tk.Canvas(win, width=600, height=400)
logo_bitcoin.grid(column=1, row=1, columnspan=3)
firstLabel = tk.Label(win, width=640, height=480)

logo = Image.open('images/bitcoin_logo.jpg')
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(firstLabel, image=logo)
logo_label.image = logo
logo_bitcoin.grid(column=1, row=1, columnspan=3)
logo_label.grid(column=1, row=1)

string_logo1 = tk.Label(firstLabel, text='Welcome to the cryptocurrency center.\n\n\n\n\n\n', font=('bold', 16))
string_logo1.grid(row=1, column=2)
string_logo2 = tk.Label(firstLabel, text='The app functionalities are included in the top menu and below.\n\n\n\n\n',
                        font=('bold', 11))
string_logo2.grid(row=1, column=2)
buttonLabel = tk.Label(firstLabel, text="")
buttonLabel.grid(row=1, column=2)
clicked = StringVar()
clicked.set("Menu")
drop = tk.OptionMenu(buttonLabel, clicked, "Cryptocurrency rates", "Cryptocurrency exchanges", "About cryptocurrencies",
                     "Converter", "Quit",
                     command=onChange).grid(row=1, column=2, sticky=tk.E)
firstLabel.grid(column=1, row=1, columnspan=3)


def selectHandler():
    if clicked.get() == "Quit":
        _quit()
    elif clicked.get() == "Cryptocurrency rates":
        cryptocurrency_rates()
    elif clicked.get() == "Cryptocurrency exchanges":
        cryptocurrency_exchanges()
    elif clicked.get() == "About cryptocurrencies":
        info_cryptocurrencies()


buttonSelect = tk.Button(buttonLabel, text="Select", command=selectHandler).grid(row=1, column=3, sticky=tk.W)


def cryptocurrency_rates():
    forgetAllScene()

    try:
        # d = requests.get("https://www.coingecko.com/en")
        # df = pd.read_html(d.text)[0]
        # df = df[["Coin", "Price", "1h", "24h", "7d"]]
        # df["Coin"] = df["Coin"].apply(lambda x: x.split(" ")[0])

        d = requests.get("https://8marketcap.com/cryptos/")
        print(d)
        df = pd.read_html(d.text)[0]
        df = df[["Name", "Symbol", "Price", "24h", "7d"]]

    except KeyError:
        messagebox.showwarning("Warning", "Server request error! Please reset your application!")
        _quit()
    except requests.exceptions.ConnectionError:
        messagebox.showerror("Warning", "No internet or connection error! Please restart your applications!")
        _quit()

    table = ttk.Treeview(crypto_rates_frame)

    logoframe = tk.Label(crypto_rates_frame, text='Cryptocurrency rates dashboard\n', font=('bold', 20))
    logoframe.grid(row=0, column=1)

    table["column"] = list(df.columns)
    table["show"] = "headings"

    for column in table["column"]:
        table.heading(column, text=column)
        table.column(column, width=100, anchor=CENTER)

    df_rows = df.to_numpy().tolist()
    for row in df_rows:
        table.insert("", "end", values=row)

    table.grid(row=1, column=1)
    crypto_rates_frame.grid(column=1, row=1, columnspan=3)


def cryptocurrency_exchanges():
    forgetAllScene()

    try:
        # d = requests.get("https://www.coingecko.com/en/exchanges")
        # df = pd.read_html(d.text)[0]
        # df = df[["Exchange", "Visits (SimilarWeb)", "# Coins", "# Pairs"]]
        # df["Exchange"] = df["Exchange"].apply(lambda x: x.split(" ")[0])
        # df["Visits (SimilarWeb)"] = df["Visits (SimilarWeb)"].apply(lambda x: str(x).replace(".0", ""))

        d = requests.get("https://cryptorank.io/exchanges")
        df = pd.read_html(d.text)[0]
        df = df[["Rank", "Name", "Pairs", "Market Share"]]


    except KeyError:
        messagebox.showwarning("Warning", "Server request error! Please reset your application!")
        print("")
        _quit()
    except requests.exceptions.ConnectionError:
        messagebox.showerror("Warning", "No internet or connection error! Please restart your applications!")
        _quit()

    table_exchanges = ttk.Treeview(crypto_exchanges_frame)

    logoframe = tk.Label(crypto_exchanges_frame, text='Cryptocurrency exchanges dashboard\n', font=('bold', 20))
    logoframe.grid(row=0, column=1)

    table_exchanges["column"] = list(df.columns)
    table_exchanges["show"] = "headings"

    for column in table_exchanges["column"]:
        table_exchanges.heading(column, text=column)
        table_exchanges.column(column, width=100, anchor=CENTER)

    df_rows = df.to_numpy().tolist()
    for row in df_rows:
        table_exchanges.insert("", "end", values=row)

    table_exchanges.grid(row=1, column=1)
    crypto_exchanges_frame.grid(column=1, row=1, columnspan=3)


def info_cryptocurrencies():
    forgetAllScene()

    tabControl = ttk.Notebook(crypto_info_frame, width=630, height=440)

    tab_btc = ttk.Frame(tabControl)
    tabControl.add(tab_btc, text="BTC")


    tab_eth = ttk.Frame(tabControl)
    tabControl.add(tab_eth, text="ETH")

    tab_bnb = ttk.Frame(tabControl)
    tabControl.add(tab_bnb, text="BNB")

    tab_usdt = ttk.Frame(tabControl)
    tabControl.add(tab_usdt, text="USDT")

    tab_sol = ttk.Frame(tabControl)
    tabControl.add(tab_sol, text="SOL")

    tab_usdc = ttk.Frame(tabControl)
    tabControl.add(tab_usdc, text="USDC")

    tab_ada = ttk.Frame(tabControl)
    tabControl.add(tab_ada, text="ADA")

    tab_doge = ttk.Frame(tabControl)
    tabControl.add(tab_doge, text="DOGE")

    tab_shib = ttk.Frame(tabControl)
    tabControl.add(tab_shib, text="SHIB")

    tab_ltc = ttk.Frame(tabControl)
    tabControl.add(tab_ltc, text="LTC")

    tabControl.grid(row=0, column=0)
    crypto_info_frame.grid()

    # Bitcoin history

    logo_btc = tk.Canvas(tab_btc, width=600, height=400)
    logo_btc.grid(column=1, row=1, columnspan=3)
    label_btc = tk.Label(tab_btc, width=640, height=480)

    logo_btc = Image.open('images/btc_history.jpg')
    logo_btc_resized = logo_btc.resize((200, 200), Image.ANTIALIAS)
    logo_btc = ImageTk.PhotoImage(logo_btc_resized)
    logo_btc_label = tk.Label(label_btc, image=logo_btc)
    logo_btc_label.image = logo_btc
    logo_btc_label.grid(column=1, row=1)
    label_btc.grid(row=0, column=0)

    string_name_btc = tk.Label(label_btc, text='          \n        Bitcoin (BTC)\n\n\n\n\n\n\n\n\n\n ', font=('bold', 16))
    string_name_btc.grid(row=1, column=2)
    string_wallets_btc = tk.Label(label_btc, text='            Wallets: Ledgar, Trezor, Bitcan\n\n\n\n\n\n\n\n', font=('bold', 11))
    string_wallets_btc.grid(row=1, column=2)
    string_description_btc = tk.Label(label_btc, text='          Creation date, creator: 2009, Satoshi Nakamoto\n\n\n\n', font=('bold', 11))
    string_description_btc.grid(row=1, column=2)
    string_actualrate_btc = tk.Label(label_btc, text='            Actual rate: ' + get_price('bitcoin') + ' USD', font=('bold', 11))
    string_actualrate_btc.grid(row=1, column=2)

    # Ethereum history

    logo_eth = tk.Canvas(tab_eth, width=600, height=400)
    logo_eth.grid(column=1, row=1, columnspan=3)
    label_eth = tk.Label(tab_eth, width=640, height=480)
    logo_eth = Image.open('images/eth_history.jpg')
    logo_eth_resized = logo_eth.resize((200, 200), Image.ANTIALIAS)
    logo_eth = ImageTk.PhotoImage(logo_eth_resized)
    logo_eth_label = tk.Label(label_eth, image=logo_eth)
    logo_eth_label.image = logo_eth
    logo_eth_label.grid(column=1, row=1)
    label_eth.grid(row=0, column=0)

    string_name_eth = tk.Label(label_eth, text='          \n        Ethereum (ETH)\n\n\n\n\n\n\n\n\n\n ', font=('bold', 16))
    string_name_eth.grid(row=1, column=2)
    string_wallets_eth = tk.Label(label_eth, text='            Wallets: Crypto.com, Metamask, MyEtherWallet \n\n\n\n\n\n\n\n', font=('bold', 11))
    string_wallets_eth.grid(row=1, column=2)
    string_description_eth = tk.Label(label_eth, text='          Creation date, creator: 2014, Vitalik Buterin\n\n\n\n', font=('bold', 11))
    string_description_eth.grid(row=1, column=2)
    string_actualrate_eth = tk.Label(label_eth, text='            Actual rate: ' + get_price('ethereum') + ' USD', font=('bold', 11))
    string_actualrate_eth.grid(row=1, column=2)

    # Binance coin history

    logo_bnb = tk.Canvas(tab_bnb, width=600, height=400)
    logo_bnb.grid(column=1, row=1, columnspan=3)
    label_bnb = tk.Label(tab_bnb, width=640, height=480)
    logo_bnb = Image.open('images/bnb_history.jpg')
    logo_bnb_resized = logo_bnb.resize((200, 200), Image.ANTIALIAS)
    logo_bnb = ImageTk.PhotoImage(logo_bnb_resized)
    logo_bnb_label = tk.Label(label_bnb, image=logo_bnb)
    logo_bnb_label.image = logo_bnb
    logo_bnb_label.grid(column=1, row=1)
    label_bnb.grid(row=0, column=0)

    string_name_bnb = tk.Label(label_bnb, text='          \n        Binance Coin (BNB)\n\n\n\n\n\n\n\n\n\n ', font=('bold', 16))
    string_name_bnb.grid(row=1, column=2)
    string_wallets_bnb = tk.Label(label_bnb, text='            Wallets: Ledgar \n\n\n\n\n\n\n\n', font=('bold', 11))
    string_wallets_bnb.grid(row=1, column=2)
    string_description_bnb = tk.Label(label_bnb, text='          Creation date, creator: 2017, Binance Exchange\n\n\n\n', font=('bold', 11))
    string_description_bnb.grid(row=1, column=2)
    string_actualrate_bnb = tk.Label(label_bnb, text='            Actual rate: ' + get_price('binancecoin') + ' USD', font=('bold', 11))
    string_actualrate_bnb.grid(row=1, column=2)

    # Tether history

    logo_usdt = tk.Canvas(tab_usdt, width=600, height=400)
    logo_usdt.grid(column=1, row=1, columnspan=3)
    label_usdt= tk.Label(tab_usdt, width=640, height=480)
    logo_usdt = Image.open('images/tether_history.jpg')
    logo_usdt_resized = logo_usdt.resize((200, 200), Image.ANTIALIAS)
    logo_usdt = ImageTk.PhotoImage(logo_usdt_resized)
    logo_usdt_label = tk.Label(label_usdt, image=logo_usdt)
    logo_usdt_label.image = logo_usdt
    logo_usdt_label.grid(column=1, row=1)
    label_usdt.grid(row=0, column=0)

    string_name_usdt = tk.Label(label_usdt, text='          \n        Tether (USDT)\n\n\n\n\n\n\n\n\n\n ', font=('bold', 16))
    string_name_usdt.grid(row=1, column=2)
    string_wallets_usdt = tk.Label(label_usdt, text='            Wallets: Ledgar, Bitcan, Crypto.com \n\n\n\n\n\n\n\n', font=('bold', 11))
    string_wallets_usdt.grid(row=1, column=2)
    string_description_usdt = tk.Label(label_usdt, text='          Creation date, creator: 2014, Craig Seller\n\n\n\n', font=('bold', 11))
    string_description_usdt.grid(row=1, column=2)
    string_actualrate_usdt = tk.Label(label_usdt, text='            Actual rate: ' + get_price('tether') + ' USD', font=('bold', 11))
    string_actualrate_usdt.grid(row=1, column=2)

    # Solana history

    logo_sol = tk.Canvas(tab_sol, width=600, height=400)
    logo_sol.grid(column=1, row=1, columnspan=3)
    label_sol = tk.Label(tab_sol, width=640, height=480)
    logo_sol = Image.open('images/sol_history.jpg')
    logo_sol_resized = logo_sol.resize((200, 200), Image.ANTIALIAS)
    logo_sol = ImageTk.PhotoImage(logo_sol_resized)
    logo_sol_label = tk.Label(label_sol, image=logo_sol)
    logo_sol_label.image = logo_sol
    logo_sol_label.grid(column=1, row=1)
    label_sol.grid(row=0, column=0)

    string_name_sol = tk.Label(label_sol, text='          \n        Solana (SOL)\n\n\n\n\n\n\n\n\n\n ', font=('bold', 16))
    string_name_sol.grid(row=1, column=2)
    string_wallets_sol = tk.Label(label_sol, text='            Wallets: Ledgar, Coin98 \n\n\n\n\n\n\n\n', font=('bold', 11))
    string_wallets_sol.grid(row=1, column=2)
    string_description_sol = tk.Label(label_sol, text='          Creation date, creator: 2017, Anatol Yakovenko\n\n\n\n', font=('bold', 11))
    string_description_sol.grid(row=1, column=2)
    string_actualrate_sol = tk.Label(label_sol, text='            Actual rate: ' + get_price('solana') + ' USD', font=('bold', 11))
    string_actualrate_sol.grid(row=1, column=2)

    # USD Coin history

    logo_usdc = tk.Canvas(tab_usdc, width=600, height=400)
    logo_usdc.grid(column=1, row=1, columnspan=3)
    label_usdc = tk.Label(tab_usdc, width=640, height=480)
    logo_usdc = Image.open('images/usdc_history.jpg')
    logo_usdc_resized = logo_usdc.resize((200, 200), Image.ANTIALIAS)
    logo_usdc = ImageTk.PhotoImage(logo_usdc_resized)
    logo_usdc_label = tk.Label(label_usdc, image=logo_usdc)
    logo_usdc_label.image = logo_usdc
    logo_usdc_label.grid(column=1, row=1)
    label_usdc.grid(row=0, column=0)

    string_name_usdc = tk.Label(label_usdc, text='          \n        USD Coin (USDC)\n\n\n\n\n\n\n\n\n\n ', font=('bold', 16))
    string_name_usdc.grid(row=1, column=2)
    string_wallets_usdc = tk.Label(label_usdc, text='            Wallets: Ledgar, Crypto.com \n\n\n\n\n\n\n\n', font=('bold', 11))
    string_wallets_usdc.grid(row=1, column=2)
    string_description_usdc = tk.Label(label_usdc, text='          Creation date, creator: 2018, Coinbase\n\n\n\n', font=('bold', 11))
    string_description_usdc.grid(row=1, column=2)
    string_actualrate_usdc = tk.Label(label_usdc, text='            Actual rate: ' + get_price('usd-coin') + ' USD', font=('bold', 11))
    string_actualrate_usdc.grid(row=1, column=2)

    # Cardano history

    logo_ada = tk.Canvas(tab_ada, width=600, height=400)
    logo_ada.grid(column=1, row=1, columnspan=3)
    label_ada = tk.Label(tab_ada, width=640, height=480)
    logo_ada = Image.open('images/ada_history.jpg')
    logo_ada_resized = logo_ada.resize((200, 200), Image.ANTIALIAS)
    logo_ada = ImageTk.PhotoImage(logo_ada_resized)
    logo_ada_label = tk.Label(label_ada, image=logo_ada)
    logo_ada_label.image = logo_ada
    logo_ada_label.grid(column=1, row=1)
    label_ada.grid(row=0, column=0)

    string_name_ada = tk.Label(label_ada, text='          \n        Cardano (ADA)\n\n\n\n\n\n\n\n\n\n ', font=('bold', 16))
    string_name_ada.grid(row=1, column=2)
    string_wallets_ada = tk.Label(label_ada, text='            Wallets: Ledgar, Trezor \n\n\n\n\n\n\n\n', font=('bold', 11))
    string_wallets_ada.grid(row=1, column=2)
    string_description_ada = tk.Label(label_ada, text='          Creation date, creator: 2017, Cardano\n\n\n\n', font=('bold', 11))
    string_description_ada.grid(row=1, column=2)
    string_actualrate_ada = tk.Label(label_ada, text='            Actual rate: ' + get_price('cardano') + ' USD', font=('bold', 11))
    string_actualrate_ada.grid(row=1, column=2)

    # Dogecoin history

    logo_doge = tk.Canvas(tab_doge, width=600, height=400)
    logo_doge.grid(column=1, row=1, columnspan=3)
    label_doge = tk.Label(tab_doge, width=640, height=480)
    logo_doge = Image.open('images/doge_history.jpg')
    logo_doge_resized = logo_doge.resize((200, 200), Image.ANTIALIAS)
    logo_doge = ImageTk.PhotoImage(logo_doge_resized)
    logo_doge_label = tk.Label(label_doge, image=logo_doge)
    logo_doge_label.image = logo_doge
    logo_doge_label.grid(column=1, row=1)
    label_doge.grid(row=0, column=0)

    string_name_doge = tk.Label(label_doge, text='          \n        Dogecoin (DOGE)\n\n\n\n\n\n\n\n\n\n ', font=('bold', 16))
    string_name_doge.grid(row=1, column=2)
    string_wallets_doge = tk.Label(label_doge, text='            Wallets: Ledgar, Trezor \n\n\n\n\n\n\n\n', font=('bold', 11))
    string_wallets_doge.grid(row=1, column=2)
    string_description_doge = tk.Label(label_doge, text='          Creation date, creator: 2013, Anonim\n\n\n\n', font=('bold', 11))
    string_description_doge.grid(row=1, column=2)
    string_actualrate_doge = tk.Label(label_doge, text='            Actual rate: ' + get_price('dogecoin') + ' USD', font=('bold', 11))
    string_actualrate_doge.grid(row=1, column=2)

    # Shiba Inu history

    logo_shib = tk.Canvas(tab_shib, width=600, height=400)
    logo_shib.grid(column=1, row=1, columnspan=3)
    label_shib = tk.Label(tab_shib, width=640, height=480)
    logo_shib = Image.open('images/shib_history.jpg')
    logo_shib_resized = logo_shib.resize((200, 200), Image.ANTIALIAS)
    logo_shib = ImageTk.PhotoImage(logo_shib_resized)
    logo_shib_label = tk.Label(label_shib, image=logo_shib)
    logo_shib_label.image = logo_shib
    logo_shib_label.grid(column=1, row=1)
    label_shib.grid(row=0, column=0)

    string_name_shib = tk.Label(label_shib, text='          \n        Shiba Inu (SHIB)\n\n\n\n\n\n\n\n\n\n ', font=('bold', 16))
    string_name_shib.grid(row=1, column=2)
    string_wallets_shib = tk.Label(label_shib, text='            Wallets: AtomicWallet, Exodus \n\n\n\n\n\n\n\n', font=('bold', 11))
    string_wallets_shib.grid(row=1, column=2)
    string_description_shib = tk.Label(label_shib, text='          Creation date, creator: 2020, Ryoshi\n\n\n\n', font=('bold', 11))
    string_description_shib.grid(row=1, column=2)
    string_actualrate_shib = tk.Label(label_shib, text='            Actual rate: ' + get_price('shiba-inu') + ' USD', font=('bold', 11))
    string_actualrate_shib.grid(row=1, column=2)

    # Litecoin history

    logo_ltc = tk.Canvas(tab_ltc, width=600, height=400)
    logo_ltc.grid(column=1, row=1, columnspan=3)
    label_ltc = tk.Label(tab_ltc, width=640, height=480)
    logo_ltc = Image.open('images/ltc_history.jpg')
    logo_ltc_resized = logo_ltc.resize((200, 200), Image.ANTIALIAS)
    logo_ltc = ImageTk.PhotoImage(logo_ltc_resized)
    logo_ltc_label = tk.Label(label_ltc, image=logo_ltc)
    logo_ltc_label.image = logo_ltc
    logo_ltc_label.grid(column=1, row=1)
    label_ltc.grid(row=0, column=0)

    string_name_ltc = tk.Label(label_ltc, text='          \n        Litecoin (LTC)\n\n\n\n\n\n\n\n\n\n ', font=('bold', 16))
    string_name_ltc.grid(row=1, column=2)
    string_wallets_ltc = tk.Label(label_ltc, text='            Wallets: Crypto.com, ViaWallet, Ledgar \n\n\n\n\n\n\n\n', font=('bold', 11))
    string_wallets_ltc.grid(row=1, column=2)
    string_description_ltc = tk.Label(label_ltc, text='          Creation date, creator: 2011, Charlie Lee\n\n\n\n', font=('bold', 11))
    string_description_ltc.grid(row=1, column=2)
    string_actualrate_ltc = tk.Label(label_ltc, text='            Actual rate: ' + get_price('litecoin') + ' USD', font=('bold', 11))
    string_actualrate_ltc.grid(row=1, column=2)

    crypto_info_frame.grid(column=1, row=1, columnspan=3)


def convert_crypto(walutaZ, walutaNa):
    forgetAllScene()

    try:
        x = cg.get_coin_by_id(walutaZ)
    except requests.exceptions.ConnectionError:
        messagebox.showerror("Warning", "No internet or connection error! Please restart your applications!")
        _quit()

    symbol = x["symbol"]
    usdRate = x["market_data"]["current_price"]["usd"]

    logo_convert = tk.Canvas(crypto_convert_frame, width=600, height=400)
    logo_convert.grid(column=1, row=1, columnspan=3)
    convertLabel = tk.Label(crypto_convert_frame, width=640, height=480)

    logoConvert = Image.open('images/convert_icon.jpg')
    logo_resized = logoConvert.resize((200, 200), Image.ANTIALIAS)
    logoConvert = ImageTk.PhotoImage(logo_resized)
    logoconvert_label = tk.Label(convertLabel, image=logoConvert)
    logoconvert_label.image = logoConvert
    logo_convert.grid(column=1, row=1, columnspan=3)
    logoconvert_label.grid(column=1, row=1)

    string_logoconvert1 = tk.Label(convertLabel, text=f' Cryptocurrencies converter ({walutaZ} -> {walutaNa}) \n\n\n\n\n\n\n', font=('bold', 14))
    string_logoconvert1.grid(row=1, column=2)
    string_logoconvert2 = tk.Label(convertLabel,
                            text=f'          Actual rate: 1 {symbol} = {usdRate} usd\n\n\n\n\n',
                            font=('bold', 11))
    string_logoconvert2.grid(row=1, column=2)
    string_logoconvert3 = tk.Label(convertLabel, text='  Enter a value:', font=('bold', 11))
    string_logoconvert3.grid(row=1, column=2, sticky=tk.W)

    valueConvert = tk.StringVar()
    nameEntered = ttk.Entry(convertLabel, width=22, textvariable=valueConvert)
    nameEntered.grid(row=1, column=2)

    convertButton = ttk.Button(convertLabel, text="Convert", command=lambda: onClickConvert(walutaZ, walutaNa, nameEntered.get()))
    convertButton.grid(row=1, column=2, sticky=tk.E)

    convertLabel.grid(column=1, row=1, columnspan=3)
    crypto_convert_frame.grid(column=1, row=1, columnspan=3)


def onClickConvert(walutaZ, walutaNa, value):
    num_format = re.compile("^\s*([0-9.]\d*\s*)+$")
    isnumber = re.match(num_format, value)

    try:
        x = cg.get_coin_by_id(walutaZ)
    except requests.exceptions.ConnectionError:
        messagebox.showerror("Warning", "No internet or connection error! Please restart your applications!")
        _quit()

    if not isnumber:
        messagebox.showerror("Warning", "Enter a numeric value!")
        return

    if walutaNa == "usd" or walutaNa == "eur" or walutaNa == "pln":
        rate = x["market_data"]["current_price"][walutaNa]
        mesageValue = rate * float(value)
        messagebox.showinfo("Convert", "You will receive: " + str(mesageValue) + f" ({walutaNa})")
    else:
        kursnausd = x["market_data"]["current_price"]["usd"]
        walutaNaUSD = kursnausd * float(value)

        try:
            d = cg.get_coin_by_id(walutaNa)
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Warning", "No internet or connection error! Please restart your applications!")
            _quit()

        symbolNa = d["symbol"]
        kurs = d["market_data"]["current_price"]["usd"]
        mesageValue = float(walutaNaUSD) / float(kurs)
        messagebox.showinfo("Convert", "You will receive: " + str(mesageValue) + f" ({symbolNa})")
        return


def btctousdconvert():
    convert_crypto("bitcoin", "usd")


def btctoeurconvert():
    convert_crypto("bitcoin", "eur")


def btctoplnconvert():
    convert_crypto("bitcoin", "pln")


def btctoethereumconvert():
    convert_crypto("bitcoin", "ethereum")


def btctolitecoinconvert():
    convert_crypto("bitcoin", "litecoin")


def btctodogecoinconvert():
    convert_crypto("bitcoin", "dogecoin")


def ethtousdconvert():
    convert_crypto("ethereum", "usd")


def ethtoeurconvert():
    convert_crypto("ethereum", "eur")


def ethtoplnconvert():
    convert_crypto("ethereum", "pln")


def ethtobtcconvert():
    convert_crypto("ethereum", "bitcoin")


def ethtoltcconvert():
    convert_crypto("ethereum", "litecoin")


def ethtodogecoinconvert():
    convert_crypto("ethereum", "dogecoin")


def ltctousdconvert():
    convert_crypto("litecoin", "usd")


def ltctoeurconvert():
    convert_crypto("litecoin", "eur")


def ltctoplnconvert():
    convert_crypto("litecoin", "pln")


def ltctobtcconvert():
    convert_crypto("litecoin", "bitcoin")


def ltctoethconvert():
    convert_crypto("litecoin", "ethereum")


def ltctodogecoinconvert():
    convert_crypto("litecoin", "dogecoin")


def dogecointousdconvert():
    convert_crypto("dogecoin", "usd")


def dogecointoeurconvert():
    convert_crypto("dogecoin", "eur")


def dogecointoplnconvert():
    convert_crypto("dogecoin", "pln")


def dogecointobtcconvert():
    convert_crypto("dogecoin", "bitcoin")


def dogecointoethconvert():
    convert_crypto("dogecoin", "ethereum")


def dogecointoltcconvert():
    convert_crypto("dogecoin", "litecoin")


def availableCryptocurrencies():
    try:
        url = f'https://api.coingecko.com/api/v3/coins'
        response = requests.get(url)
        data = response.json()
    except requests.exceptions.ConnectionError:
        messagebox.showerror("Warning", "No internet or connection error! Please restart your applications!")
        _quit()

    crypto_ids = []

    for asset in data:
        crypto_ids.append(asset['id'])

    return crypto_ids


def getChart(waluta, vs_currency='usd', days='max', interval='daily'):
    crypto_ids = availableCryptocurrencies()

    if waluta in crypto_ids:
        try:
            url = f"https://api.coingecko.com/api/v3/coins/{waluta}/market_chart"
            payload = {'vs_currency': vs_currency, 'days': days, 'interval': interval}
            response = requests.get(url, params=payload)
            data = response.json()
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Warning", "No internet or connection error! Please restart your applications!")
            _quit()

        timestamp_list, price_list = [], []

        for price in data['prices']:
            timestamp_list.append(datetime.fromtimestamp(price[0] / 1000))
            price_list.append(price[1])

        raw_data = {
            'Period of time': timestamp_list,
            'Price in $USD': price_list
        }

        df = pd.DataFrame(raw_data)
        return df
    else:
        print("Cryptocurrency does not exist!")


def chartBTCGenerate():
    wykres = getChart(waluta="bitcoin")
    wykres.plot(y='Price in $USD', x='Period of time', color='#4285F4')
    plt.title(f"Chart Bitcoin")
    plt.show()
    return


def chartETHGenerate():
    wykres = getChart(waluta="ethereum")
    wykres.plot(y='Price in $USD', x='Period of time', color='#4285F4')
    plt.title(f"Chart Ethereum")
    plt.show()
    return


def chartBNBGenerate():
    wykres = getChart(waluta="binancecoin")
    wykres.plot(y='Price in $USD', x='Period of time', color='#4285F4')
    plt.title(f"Chart Binance Coin")
    plt.show()
    return


def chartUSDTGenerate():
    wykres = getChart(waluta="tether")
    wykres.plot(y='Price in $USD', x='Period of time', color='#4285F4')
    plt.title(f"Chart Tether")
    plt.show()
    return


def chartUSDCGenerate():
    wykres = getChart(waluta="usd-coin")
    wykres.plot(y='Price in $USD', x='Period of time', color='#4285F4')
    plt.title(f"Chart USD-Coin")
    plt.show()
    return


def chartSOLGenerate():
    wykres = getChart(waluta="solana")
    wykres.plot(y='Price in $USD', x='Period of time', color='#4285F4')
    plt.title(f"Chart Solana")
    plt.show()
    return


def chartADAGenerate():
    wykres = getChart(waluta="cardano")
    wykres.plot(y='Price in $USD', x='Period of time', color='#4285F4')
    plt.title(f"Chart Cardano")
    plt.show()
    return


def chartDOGEGenerate():
    wykres = getChart(waluta="dogecoin")
    wykres.plot(y='Price in $USD', x='Period of time', color='#4285F4')
    plt.title(f"Chart Dogecoin")
    plt.show()
    return


def chartSHIBGenerate():
    wykres = getChart(waluta="shiba-inu")
    wykres.plot(y='Price in $USD', x='Period of time', color='#4285F4')
    plt.title(f"Chart Shiba-Inu")
    plt.show()
    return


def switch_tui_version():
    cmdline = "python main.py"
    subprocess.call("start cmd /K " + cmdline, shell=True, cwd="C:\\Users\\Dom\\PycharmProjects\\crypto_app_tui\\")
    _quit()


# Menu
menuBar = Menu(win)
win.config(menu=menuBar)

# App - menu
appMenu = Menu(menuBar, tearoff=0)
menuBar.add_cascade(label="App", menu=appMenu)
appMenu.add_command(label="Switch Terminal Version", command=switch_tui_version)
appMenu.add_command(label="Help", command=_msgBoxHelp)
appMenu.add_command(label="Quit", command=_quit)

# About - menu
aboutMenu = Menu(menuBar, tearoff=0)
menuBar.add_cascade(label="About", menu=aboutMenu)
aboutMenu.add_command(label="Cryptocurrencies", command=info_cryptocurrencies)

# Statistic - menu
kursyMenu = Menu(menuBar, tearoff=0)
menuBar.add_cascade(label="Statistics", menu=kursyMenu)
kursyMenu.add_command(label="Cryptocurrency rates", command=cryptocurrency_rates)
kursyMenu.add_command(label="Cryptocurrency exchanges", command=cryptocurrency_exchanges)

# Converter

convertMenu = Menu(menuBar, tearoff=0)
menuBar.add_cascade(label="Converter", menu=convertMenu)

btc_menu = Menu(convertMenu, tearoff=0)
convertMenu.add_cascade(label="Bitcoin", menu=btc_menu)
btc_menu.add_command(label="Bitcoin->USD", command=btctousdconvert)
btc_menu.add_command(label="Bitcoin->EUR", command=btctoeurconvert)
btc_menu.add_command(label="Bitcoin->PLN", command=btctoplnconvert)
btc_menu.add_command(label="Bitcoin->Ethereum", command=btctoethereumconvert)
btc_menu.add_command(label="Bitcoin->Litecoin", command=btctolitecoinconvert)
btc_menu.add_command(label="Bitcoin->Dogecoin", command=btctodogecoinconvert)

eth_menu = Menu(convertMenu, tearoff=0)
convertMenu.add_cascade(label="Ethereum", menu=eth_menu)
eth_menu.add_command(label="Ethereum->USD", command=ethtousdconvert)
eth_menu.add_command(label="Ethereum->EUR", command=ethtoeurconvert)
eth_menu.add_command(label="Ethereum->PLN", command=ethtoplnconvert)
eth_menu.add_command(label="Ethereum->Bitcoin", command=ethtobtcconvert)
eth_menu.add_command(label="Ethereum->Litecoin", command=ethtoltcconvert)
eth_menu.add_command(label="Ethereum->Dogecoin", command=ethtodogecoinconvert)


ltc_menu = Menu(convertMenu, tearoff=0)
convertMenu.add_cascade(label="Litecoin", menu=ltc_menu)
ltc_menu.add_command(label="Litecoin->USD", command=ltctousdconvert)
ltc_menu.add_command(label="Litecoin->EUR", command=ltctoeurconvert)
ltc_menu.add_command(label="Litecoin->PLN", command=ltctoplnconvert)
ltc_menu.add_command(label="Litecoin->Bitcoin", command=ltctobtcconvert)
ltc_menu.add_command(label="Litecoin->Ethereum", command=ltctoethconvert)
ltc_menu.add_command(label="Litecoin->Dogecoin", command=ltctodogecoinconvert)

doge_menu = Menu(convertMenu, tearoff=0)
convertMenu.add_cascade(label="Dogecoin", menu=doge_menu)
doge_menu.add_command(label="Dogecoin->USD", command=dogecointousdconvert)
doge_menu.add_command(label="Dogecoin->EUR", command=dogecointoeurconvert)
doge_menu.add_command(label="Dogecoin->PLN", command=dogecointoplnconvert)
doge_menu.add_command(label="Dogecoin->Bitcoin", command=dogecointobtcconvert)
doge_menu.add_command(label="Dogecoin->Ethereum", command=dogecointoethconvert)
doge_menu.add_command(label="Dogecoin->Litecoin", command=dogecointoltcconvert)

# Charts - wykresy

chartsMenu = Menu(menuBar, tearoff=0)
menuBar.add_cascade(label="Charts", menu=chartsMenu)
chartsMenu.add_command(label="Bitcoin chart", command=chartBTCGenerate)
chartsMenu.add_command(label="Ethereum chart", command=chartETHGenerate)
chartsMenu.add_command(label="Binance Coin chart", command=chartBNBGenerate)
chartsMenu.add_command(label="Tether chart", command=chartUSDTGenerate)
chartsMenu.add_command(label="Solana chart", command=chartSOLGenerate)
chartsMenu.add_command(label="USD Coin chart", command=chartUSDCGenerate)
chartsMenu.add_command(label="Cardano chart", command=chartADAGenerate)
chartsMenu.add_command(label="Dogecoin chart", command=chartDOGEGenerate)
chartsMenu.add_command(label="Shiba Inu chart", command=chartSHIBGenerate)

# Theme
themeMenu = Menu(menuBar, tearoff=0)
menuBar.add_cascade(label="Theme", menu=themeMenu)
themeMenu.add_command(label="Dark", command=dark_theme)
themeMenu.add_command(label="Light", command=light_theme)


crypto_convert_frame = tk.Label(win, width=640, height=480)
crypto_info_frame = tk.Label(win, width=640, height=480)
crypto_rates_frame = tk.Label(win, width=640, height=480)
crypto_exchanges_frame = tk.Label(win, width=640, height=480)

win.iconbitmap(r'images/btc-icon.ico')

win.mainloop()
