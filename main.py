import tkinter as tk
from tkinter import ttk
from typing import Optional
from WeatherData import WeatherForecast, valid_city, getweather, getPictureFileFromDescription
from PIL import Image, ImageTk

window = tk.Tk()
window.title('Weather App')
window.geometry('300x300')
style = ttk.Style()
style.configure('My.TFrame', background='pink')
frame = ttk.Frame(window, style='My.TFrame')
frame.configure()

dict_ro = {'Location': 'Localitate', 'Choose language': 'Alege limba',
           'Temperature: ': 'Temperatura: ', 'Go': 'Cauta',
           'Weather App': 'Vremea', 'Today': 'Azi', 'Tomorrow': 'Maine',
           'light snow': 'ninsoare', 'clear sky': 'insorit', 'clear': 'insorit',
           'sunny': 'insorit', 'light rain': 'ploaie marunta', 'rain': 'ploaie',
           'moderate rain': 'ploaie moderata', 'heavy rain': 'ploaie torentiala',
           'thunderstorm': 'furtuna', 'overcast clouds': 'innorat', 'clouds': 'innorat',
           'few clouds': 'nori si soare', 'broken clouds': 'nori imprastiati',
           'scattered clouds': 'nori imprastiati',
           'The city is not in our city list.': "Orasul nu este in lista.",
           'No internet connection.': 'Nu e conexiune la internet'}


def translatetext(text) -> str:
    global use_ro
    global dict_ro
    if use_ro is True:
        if text not in dict_ro:
            print('Could not translate this.')
            return text
        else:
            return dict_ro[text]
    else:
        return text


def languageChangedCallback(event):
    global selected_language
    global use_ro
    global result_label_text
    if selected_language.get() == 'English':
        use_ro = False
    elif selected_language.get() == 'Romanian':
        use_ro = True
    languageLabel.configure(text=translatetext('Choose language'))
    labelLocation.configure(text=translatetext('Location'))
    button.configure(text=translatetext('Go'))
    labeltab1Temp.configure(text=translatetext('Temperature: '))
    labeltab2Temp.configure(text=translatetext('Temperature: '))
    window.title(translatetext('Weather App'))
    tabs.tab(0, text=translatetext('Today'))
    tabs.tab(1, text=translatetext('Tomorrow'))
    result_label.configure(text=translatetext(result_label_text))


use_ro = False
languageLabel = ttk.Label(frame, text='Choose language')
languageLabel.grid(row=5, column=1)
selected_language = tk.StringVar()

chooseLanguage = ttk.Combobox(frame, textvariable=selected_language, values=['English', 'Romanian'])
chooseLanguage.grid(row=6, column=1)
chooseLanguage.current(0)
chooseLanguage.bind("<<ComboboxSelected>>", languageChangedCallback)

tabs = ttk.Notebook(frame)
tab1 = ttk.Frame(tabs)
tab2 = ttk.Frame(tabs)
tab1.grid()
tab2.grid()
tabs.add(tab1, text='Today')
tabs.add(tab2, text='Tomorrow')
labeltab1time = ttk.Label(tab1)
labeltab1description = ttk.Label(tab1)
labeltab1temperature = ttk.Label(tab1)
labeltab1Temp = ttk.Label(tab1)
labeltab1Temp.configure(text=translatetext('Temperature: '))
labeltab1time.grid()
labeltab1description.grid()
labeltab1temperature.grid(row=3, column=1)
labeltab1Temp.grid(row=3, column=0)
labeltab2time = ttk.Label(tab2)
labeltab2description = ttk.Label(tab2)
labeltab2temperature = ttk.Label(tab2)
labeltab2Temp = ttk.Label(tab2)
labeltab2time.grid()
labeltab2description.grid()
labeltab2temperature.grid(row=3, column=1)
labeltab2Temp.grid(row=3, column=0)
labeltab2Temp.configure(text=translatetext('Temperature: '))
imgLabeltab = tk.Label(tab1)
imgLabeltab.grid()
imgLabeltab2 = tk.Label(tab2)
imgLabeltab2.grid(rowspan=1, columnspan=1)


def setPictureToTab(picturefile, labelTab):
    imgtab = ImageTk.PhotoImage(Image.open(picturefile).resize((50, 50)))
    labelTab.configure(image=imgtab)
    labelTab.image = imgtab


weatherdata: Optional[WeatherForecast] = None


def delete_labels():
    labels = [labeltab1time, labeltab1description, labeltab1Temp, labeltab1temperature, labeltab2time,
              labeltab2description, labeltab2Temp, labeltab2temperature]
    for label in labels:
        label.configure(text='')
    imgLabeltab.configure(image='')
    imgLabeltab2.configure(image='')


def enter_clicked(cityName):
    global weatherdata
    global result_label_text
    if valid_city(cityName):
        result_label_text = ''
        result_label.configure(text=result_label_text)
        weatherdata = getweather(cityName)
        if weatherdata is None:
            result_label_text = 'No internet connection.'
            result_label.configure(text=translatetext(result_label_text))
            delete_labels()
        else:
            weatherForecastToday = weatherdata.today
            labeltab1time.configure(text=weatherForecastToday.time)
            labeltab1description.configure(text=translatetext(weatherForecastToday.description))
            labeltab1Temp.configure(text=translatetext('Temperature: '))
            setPictureToTab(getPictureFileFromDescription(weatherForecastToday.description), imgLabeltab)
            weatherForecastTomorrow = weatherdata.tomorrow
            labeltab2time.configure(text=weatherForecastTomorrow.time)
            labeltab2description.configure(text=translatetext(weatherForecastTomorrow.description))
            labeltab2Temp.configure(text=translatetext('Temperature: '))
            setPictureToTab(getPictureFileFromDescription(weatherForecastTomorrow.description), imgLabeltab2)
            if use_kelvin:
                labeltab1temperature.configure(text=weatherForecastToday.temperature_kelvin)
                labeltab2temperature.configure(text=weatherForecastTomorrow.temperature_kelvin)
            else:
                labeltab1temperature.configure(
                    text=weatherForecastToday.temperature_celsius)
                labeltab2temperature.configure(
                    text=weatherForecastTomorrow.temperature_celsius)
    else:
        result_label_text = 'The city is not in our city list.'
        result_label.configure(text=translatetext(result_label_text))
        delete_labels()


def go_button_clicked():
    return enter_clicked(town.get())


result_label_text = ''
labelLocation = ttk.Label(frame, text='Location', width=10)
labelLocation.grid(row=1, column=0)

town = tk.StringVar()
entry = ttk.Entry(frame, width=20, textvariable=town)
entry.grid(row=1, column=1)
entry.focus()
entry.bind('<Return>', enter_clicked)

button = ttk.Button(frame, text='Go', width=10)
button.grid(row=1, column=2)
button.configure(command=go_button_clicked)

var = tk.IntVar()
var.set(1)
use_kelvin = True


def change_temperature_scale():
    global use_kelvin
    global weatherdata

    if weatherdata is None:
        return

    if var.get() == 1:
        use_kelvin = True
        labeltab1temperature.configure(text=weatherdata.today.temperature_kelvin)
        labeltab2temperature.configure(text=weatherdata.tomorrow.temperature_kelvin)
    else:
        use_kelvin = False
        labeltab1temperature.configure(text=weatherdata.today.temperature_celsius)
        labeltab2temperature.configure(text=weatherdata.tomorrow.temperature_celsius)


kelvin = ttk.Radiobutton(frame, variable=var, value=1, text='K', command=change_temperature_scale)
celsius = ttk.Radiobutton(frame, variable=var, value=2, text='C', command=change_temperature_scale)
kelvin.grid(row=3, column=0)
celsius.grid(row=3, column=1)

result_label = ttk.Label(frame)
result_label.grid(rowspan=12, columnspan=10)

tabs.grid(padx=10, pady=10, rowspan=10, columnspan=10)
frame.pack(expand=True, fill='both')
window.mainloop()
