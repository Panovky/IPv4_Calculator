from tkinter import *
from tkinter import ttk
from tkinter import font
import re


def findNetMask():
    normalView = []
    prefixView = combobox.get()
    prefixView = int(prefixView[1:])
    for i in range(4):
        if prefixView >= 8:
            normalView.append('255')
            prefixView -= 8
        else:
            normalView.append(str(256 - pow(2, 8 - prefixView)))
            prefixView = 0
    normalView = '.'.join(normalView)
    return normalView


def findNetAddress():
    netAddress = [0]*4
    ipAddress = entry.get()
    ipAddress = list(map(int, ipAddress.split('.')))
    mask = findNetMask()
    mask = list(map(int, mask.split('.')))
    sub = 128
    for i in range(4):
        if mask[i] == 255 or mask[i] == ipAddress[i]:
            netAddress[i] = ipAddress[i]
        elif mask[i] == 0 or ipAddress[i] == 0:
            netAddress[i] = 0
        else:
            while mask[i] != 0 and ipAddress[i] != 0:
                if ipAddress[i] >= sub:
                    ipAddress[i] -= sub
                    netAddress[i] += sub
                mask[i] -= sub
                sub //= 2
    netAddress = '.'.join(map(str, netAddress))
    return netAddress


def findBroadcastAddress():
    netAddress = findNetAddress()
    netAddress = list(map(int, netAddress.split('.')))
    mask = combobox.get()
    zeroes = 32 - int(mask[1:])
    broadcastAddress = [0] * 4
    for i in range(3, -1, -1):
        if zeroes >= 8:
            broadcastAddress[i] = 255
            zeroes -= 8
        elif zeroes > 0:
            broadcastAddress[i] = netAddress[i] + pow(2, zeroes) -1
            zeroes = 0
        else:
            broadcastAddress[i] = netAddress[i]
    broadcastAddress = '.'.join(map(str, broadcastAddress))
    return broadcastAddress


def findAllNumberOfHosts():
    prefixView = combobox.get()
    prefixView = int(prefixView[1:])
    allHosts = pow(2, 32 - prefixView)
    return allHosts


def executeCalculations():
    label3.configure(text=f'Маска в нормальном виде: {findNetMask()}')
    label4.configure(text=f'Адрес сети: {findNetAddress()}')
    label5.configure(text=f'Широковещательный адрес: {findBroadcastAddress()}')
    label6.configure(text=f'Общее количество хостов: {findAllNumberOfHosts()}')
    label7.configure(text=f'Количество рабочих хостов: {findAllNumberOfHosts() - 2}')


def isValid():
    text = entry.get()
    result = re.match(r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$', text)
    check = True
    if not bool(result):
        check = False
    else:
        for part in (map(int, text.split('.'))):
            if part > 255:
                check = False
                break
    if check:
        labelError.configure(text='')
        executeCalculations()
    else:
        clear()
        labelError.configure(text='Неккоректный IP-адрес.')


def clear():
    entry.delete(0, END)
    combobox.current(0)
    labelError.configure(text='')
    label3.configure(text='')
    label4.configure(text='')
    label5.configure(text='')
    label6.configure(text='')
    label7.configure(text='')


window = Tk()
window.title('Калькулятор IPv4-адресации')
window.configure(bg='#2B2727')
width = window.winfo_screenwidth() // 2
height = window.winfo_screenheight() // 2
window.geometry(f'700x300+{width - 350}+{height - 150}')

Font = font.Font(size=13, weight='bold')

frameInput = Frame(window, bg='#2B2727')
frameOutput = Frame(window, bg='#2B2727')

label1 = Label(frameInput, text='IPv4 адрес:', font=Font, bg='#2B2727', fg='#23EF2D')
label2 = Label(frameInput, text='маска:', font=Font, bg='#2B2727', fg='#23EF2D')

entry = Entry(frameInput, width=14, font=Font)
combobox = ttk.Combobox(frameInput, width=3, font=Font, values=['/' + str(i) for i in range(33)])

window.option_add('*TCombobox*Listbox*Font', Font)
window.option_add('*TCombobox*Listbox*selectBackground', '#23EF2D')
window.option_add('*TCombobox*Listbox*selectForeground', 'black')
combobox.current(0)

button1 = Button(frameInput, width=10, text='Рассчитать', font=Font, bg='#23EF2D')
button1.config(command=isValid)
button2 = Button(frameInput, width=10, text='Очистить', font=Font, bg='#23EF2D')
button2.config(command=clear)


labelError = Label(frameOutput, text='', font=Font, bg='#2B2727', fg='red')
label3 = Label(frameOutput, text='', font=Font, bg='#2B2727', fg='#23EF2D')
label4 = Label(frameOutput, text='', font=Font, bg='#2B2727', fg='#23EF2D')
label5 = Label(frameOutput, text='', font=Font, bg='#2B2727', fg='#23EF2D')
label6 = Label(frameOutput, text='', font=Font, bg='#2B2727', fg='#23EF2D')
label7 = Label(frameOutput, text='', font=Font, bg='#2B2727', fg='#23EF2D')

frameInput.pack(fill=X, padx=30, pady=20)
frameOutput.pack(fill=X, padx=30)

label1.pack(side=LEFT)
entry.pack(side=LEFT, padx=10, ipady=3)
label2.pack(side=LEFT, padx=10)
combobox.pack(side=LEFT, ipady=3)
button1.pack(side=LEFT, padx=30)
button2.pack(side=LEFT)

labelError.pack(anchor='nw')
label3.pack(anchor='nw', ipady=5)
label4.pack(anchor='nw', ipady=5)
label5.pack(anchor='nw', ipady=5)
label6.pack(anchor='nw', ipady=5)
label7.pack(anchor='nw', ipady=5)

window.mainloop()

