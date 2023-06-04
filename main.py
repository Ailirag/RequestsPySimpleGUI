import PySimpleGUI as sg
import requests
import time


use_custom_titlebar = True if sg.running_trinket() else False

def make_window(theme=None):

    NAME_SIZE = 23

    def name(name):
        dots = NAME_SIZE-len(name)-2
        return sg.Text(name + ' ' + '•'*dots, size=(NAME_SIZE,1), justification='r',pad=(0,0), font='Courier 10')

    sg.theme(theme)

    layout = [
                [name('Type request'), sg.Radio('GET', 'Type_request', k='GET'), sg.Radio('POST', 'Type_request', k='POST')],
                [name('User'), sg.Input(s=50, k='User')],
                [name('Password'), sg.Input(s=50, k='Password', password_char='*')],
                [name('URL'), sg.Input(s=50, k='URL')],
                [name('Arguments (?key=val)'), sg.Multiline(s=(50, 5), k='Arguments')],
                [name('Headers (key:value)'), sg.Multiline(s=(50,5), k='Headers')],
                [name('Body'), sg.Multiline(s=(50, 5), k='Output_body')],
                [name('Response code'), sg.StatusBar('', k='Response_code')],
                [name('Response body'), sg.Multiline(s=(50, 5), k='Response_body')],
                [name('Program status'), sg.StatusBar('', s=(45), k='Current_status')],
                [sg.Button('Send request', s=(69,2), k='Send_request')]]

    window = sg.Window('PyRequester', layout, finalize=True,
                       # keep_on_top=True,
                       use_custom_titlebar=use_custom_titlebar)


    return window


window = make_window()
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break

    if event == 'Send_request':

        if not values['GET'] and not values['POST']:
            window['Current_status'].update('Please select the type of request.')

        else:

            params = {'Arguments': dict(), 'Headers': dict()}

            arguments = values['Arguments']
            headers = values['Headers']

            for key in params.keys():
                if len(values[key]):
                    strings = values[key].split('\n')
                    for data in strings:
                        key_value = data.split(':')

                        params[key][key_value[0]] = key_value[1]

            start_time = time.time()

            if len(values['User']):
                variator = requests.Session()
                variator.auth = (values['User'], values['Password'])
            else:
                variator = requests

            if values['GET'] == True:

                r = variator.get(url=values['URL'], headers=params['Headers'], params=params['Arguments'])

            else:

                r = variator.post(url=values['URL'], headers=params['Headers'], params=params['Arguments'], data= values['Output_body'])

            end_time = time.time()

            if r.status_code != 200:
                status_code = f'{r.status_code} {r.reason}'
            else:
                status_code = r.status_code

            window['Response_code'].update(status_code)
            window['Response_body'].update(r.text)
            window['Current_status'].update(f'Completed for {round((end_time - start_time), 3)} seconds.')

window.close()