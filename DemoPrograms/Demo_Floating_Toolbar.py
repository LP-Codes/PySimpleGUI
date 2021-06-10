import PySimpleGUI as sg
import os
import io
from PIL import Image, ImageDraw, ImageTk, ImageFont
import base64
import subprocess
import sys

button_names = ('close', 'cookbook', 'cpu', 'github', 'pysimplegui', 'run', 'storage', 'timer')

ROOT_PATH = './' if sys.platform == 'linux' else 'C:\\Python\\PycharmProjects\\GooeyGUI\\'

house64='iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAAsSAAALEgHS3X78AAAHPklEQVRYhbVXbUxb1xl+zjn30/a9/gBsbBwCBhPAUD4W2pClSZM0TemkdZPaSf0RTfszTZv2o1qzqmqiaL82salSqzZptVVqqmRV1dEssERKxJKxLAWajEYkAcxXyoBg4xgcY8AY23c/+EgwNiTRdqTz557zPOd5n/Oe95wLPGFzOp24fPp0yeTJk4cbjxzJelIe9qTA5uPHt7mHho6HOzsP1RQUWODxnO/o6Pj/C3A6naT5/ffLC9raWqZbW2v8t29GEz7/d3dXVuY56us7W69cmX1EHqaqKn1sAWffe6+ipK/vROjChaq+WNj/r2wWN44FEvAHamtcLhtfW3uuo7NT24xHVVUKPIYDzrw80vzuu1WuixdbQufPV3SJC747VcxUWC1ZvtFoRPX6tMX+wR27PJ6CLbt3d3zV1WWy2+0HZVn2APAkEgmPKIqeeDzeAwDhcFgLh8MaeVQB//j445qSrq4TU2fO1HlF+L07BGN5hVmXnWXG4PA4+q/OTVb1RwSjwSRZGxqaLm3deq7z+vU/B4NBjIyMwOfzQVEU+Hw+AgD19fUCAGwqwJmXR08dO1brampqjly7Zuu26/3j35GNNdutOqvVAV4QEA6H0D8wgr7u6OS29oCgSxCj7eWXvyB7snLjCDwLAiSTSe3YB20/avv3aNPD/NxmAk4dPbq9pLX1w3BHh23IrPMH6lW1vMyks+XmQxBEAIDRlI2iIoATJqw9kaS/sDt4P3b27A90d2yJql83EMIzxGILcYGniVT+jAKcDgc99dZbT7tOnGgO9/dn9RZb/f5nzeo2t1lPIGM6GAUlUbBlDxl4WA1GcAcEW2+27LddGiXz7cPqrd9fROXPDkC2GMAYv8q/sgUZBZw6fLi+5PPPj0d6e7NHnNm+qX1Wtdht0muLAj7rVhB0fR81VgLc/AKXTK/ioIuHe/5LFG6NgeMmbTdn4r6szrvM195vIAkN24+8AkYfLNfe3h5bEp4aud3Omo8e3eVubPzrgtdb4PU4fYHvbVFLn3LobblOxKJJdMyWwPXiL/F8XQV6brQjWv8r1D9VBvdsJ7Jy9JBlCXorMYyJmsBGZjA74ENo0IeEq7T5Srf3FrBBHWh5++09ZZ9+eiI2MpL/baHdH/yhS813Z+lzrHmQJD1mQrNIjvXBEf4G/NAFZEXvYCfrRtn9v0MI3oZozYUo6cDxFIZsEWOLiLDAQnR+2Cd7bPkm8759Z77u6oqtqwNOu51refPNvaWNjWcWx8edAzUu3/QrJWphuV2fk+OEJCsglGFuZhYtoTJ0lh2BuXwvvvrPLD6SfwHOtReFiUEYFApKOciyAlEUoOZJwj2zMq0N309GbvWU1VosTxcfOPB1y+XLgXA4rK0K+Nsbbzxfefr0B/GJCceoy+EPveZRHEUWgyXLAUlWQAkDIQxzMzO4Iz+Dssrt2FkkYnzgNsxFz+ClIh7ucBsgLM2jlFtyggKKhTP4CD+FiYg26x1wlypKhfm555qv3bgRZc7cXP7c668frHznnb/EJybsQ3Vuf/hQteIssRnMFgcknRGEstWemI0gSXR4oWARXHQEJVNXUesQ4Ex8C8PkNSQU0+pcSjmIsgJe4GByykooxzgd9wYQ6ekrrTEa64v377/OXqiutv387t0/LHq928bcW3wzP9mu5BRY9EazDZLOuBr5SudFEYViAPpIP5RwP7IMGrIXvJAjXkDgoEnGNfMp5SCIOhCahDFHNAQ5YSoxGsLcwFDRnoaGEDcej09M7NrVNDo+VBR8tcJcVmzT6/QWyDpT2uPJ61RAp0IDoAFIpowTkHX1lTEeJrMTjPlRup/Y2+ZjI4XDscG7VmszAYAd5eXGaHCi7seH6n7TsK9ip6LawPO6tAI+OfklAvem0o4BwEsv7oHH404zoiESnsS9YAD+hfzjv/vtJ38cDoZ6OQDo6Om5D6D1NY3+lOMFUMaDPlS1Hm6Dff2IT42D0vVjszEgUFedEct4AYwTUOyqvnm1b+AGkFIJCWVLi9Olnq7xjEAQCWiaayyhLXOkxWqgjANlHAh5AF4jgFIGxjhQxoNkiIJjFJLIAWStAgJgUUsuJV8GLGU82EYCVqhWsjddY5RCFrjU9UEIEI1vhNWWEjQ1oHSLEMqBMCG9AEZhkLl1W0AAROPxzFhNA8j6xMkgYGMHjBIPgaWQEWBuESCEpsdq2hrrNxGQ2QGOMQgcA5ey/j99KtR44H/hwOY5oOpEiPxash1kAdMzfEYHNE0D8KhbwLiNTwFPwLO1L+98I0FykS47sB5LNDziFhAsO5DpKFHIAoOQ8pIgBJB4BkJpWqz2OElIM0QBLOWAQeIgpiAJAFlkICSTA4+RhNjAAUYpZJGDlLIFhBBIPIOWoRI+hgNk+T7P8F4lFJIkQxHXk0nCIuYJTYsl0ECWk5DQB8/zTf8LUluScAguUG0mvv73bz6exuOHJKwUwg8/+lNk5et/AVSZbsni/k4yAAAAAElFTkSuQmCC'

cpu64='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'

timer64='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'

close64 = 'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAEQ0lEQVR42r2XW2wbRRSG/1177TgkdkyoS4shaaWogVIKRAXUVn4BgRBEIRBSkSK1lAakPhTxABJSK6BEtAoXCUHEWwWi4oEXUAVvRUASSBuJliAh5QJp6hrspoGQi69r73LO7Npu6kvsBGek0ezOrvf79szsmbG0D2iwAN8DaMQaFA0YHQFaLwCX6TQuHQAuNtjR2PawD05LZeFzKeC7b/txPoLxU8Aj1BVkAf1wqw/uejeU9RsASaqYQGp+Dv8EAvjgdD9OAg9S14gQOPKED1XNWyv7+lT0VArxiVH0fCUEOqjr3JoKcImN/pYW2EOnQyUJTESBJkdpgGkV8Cj/owDDdx59A8Mf92FT+GpR+KSlBrt6ehE6+hL0pLp6AYbvfusE5FontFgUZ989UVAiDU+X0OsvQ0/EVy4g4MeOQ3a6Mn38wKHet3MkrofzZJMsFlzpeRVaeLF8ASPsb8Javy7nDXRVxdA7x7FpIZQXnrlP0yDJMoKvHVpZBKq23Qv3M8/nzQt6PIah93qhRxaLwvPNhbLmgGP7Drg694mHlVqKwcsWEBItD8DVvleM6WrhRQXUwBSsnpthvclDY++BZLdnflS9YxecrZ2QFGVZePDIYcq5yWuGK47k39NIzlCdDkHxNuYXiJzrz/xIrr4BFpdbfAFyTS1CSi1uf7IDrqeeheyoLihxubsD2sI8UuEFaItUKfen5mahRcLZl7nft7xAvjIQs+GFP2cLCmjRCL5p3oDN6nzR56xIYDl4ORJlCwyqDnT7Z5aFL5G4w4vN8dnVCwymatA9daVkeCkSJQv8qDtxcDKYF86AwKEuSDYbvB+doq/DlnMPJ6uvmzfmSJQk0E9D+OLVcEG4f38bwgNnxLmz9Wl4+z6HZLXm3JuYHMfE7i0ri8Ck3Y3Hx4L0lvYl8Et7H0Xk7NJ7Xe1d8H74GX2/2YyZmv8XY3euo4SUXJkAFyvtEbdc+CsDn2r3Ifrrz3nHvW7Pftzy/kmxdhSCly2Qlmj66Xf88dB2qP6LRme+jauuo67rIDyvHMN4i1esmvlK6QIUTrEISbKxDnDlPkk2BK6VIDhXXaddP6Vk0H6A9wSUn0WKFn2lCgiYbDEmFVXJYjWOuU1LcHudgAASSLS0FnD4dV4TksYxNEOqsMDwgAAxELToSFZFfGaiVWzGNV6MWM4Uyc5OE8wQCr2AqwmxIuoJowX3k5CjZSd6vvxhqcBj921Fc2g8C2Mwzf5sax7zNZZjSdkcCg6/EEgacAYzlLZvRk1kW7rm39iELwZHsgLPATN311rqb7trG+65dT2FXTEg4o1NoDinZKOYQ8ICFo4ADwMJpEwBDrnKIU+YMqZQ0pAbC4QwODwCf0Rd/BQ4IATagM46oI+CeiNPPVS40EDF6M/pJ78Ap+n0PL8Cp7sGs9asgQSFDLxBmKJ6STKBVSbcZsa10gKcJHi/Hv0PWqbBbaFH/AEAAAAASUVORK5CYII='


def ExecuteCommandSubprocess(command, *args, wait=False):
    # try:
        if sys.platform == 'linux':
                arg_string = ''.join(' ' + str(arg) for arg in args)
                sp = subprocess.Popen(['python3' + arg_string, ], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
                expanded_args = []
                for a in args:
                    expanded_args += a
                sp = subprocess.Popen([command, expanded_args], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if wait:
            out, err = sp.communicate()
            if out:
                print(out.decode("utf-8"))
            if err:
                print(err.decode("utf-8"))
    # except: pass


def get_image_bytes(image64):
        image_file = io.BytesIO(base64.b64decode(image64))
        img = Image.open(image_file)
        bio = io.BytesIO()
        img.save(bio, format='PNG')
        return bio.getvalue()

def ShowMeTheButtons():

    sg.SetOptions(auto_size_buttons=True, margins=(0,0), button_color=sg.COLOR_SYSTEM_DEFAULT)

    toolbar_buttons = [[sg.Button('', image_data=get_image_bytes(close64),button_color=('white', 'black'), pad=(0,0), key='_close_'),
                        sg.Button('', image_data=get_image_bytes(timer64), button_color=('white', 'black'), pad=(0, 0), key='_timer_'),
                        sg.Button('', image_data=get_image_bytes(house64), button_color=('white', 'black'), pad=(0, 0), key='_house_'),
                        sg.Button('', image_data=get_image_bytes(cpu64), button_color=('white', 'black'), pad=(0,0), key='_cpu_'),]]

    # layout = toolbar_buttons
    layout =  [[sg.Frame('Launcher', toolbar_buttons,title_color='white', background_color='black')]]

    window = sg.Window('Toolbar', no_titlebar=True, grab_anywhere=True, background_color='black').Layout(layout)

    # ---===--- Loop taking in user input --- #
    while True:
        button, value = window.Read()
        print(button)
        if button == '_close_' or button is None:
            break       # exit button clicked
        elif button == '_timer_':
            pass        # add your call to launch a timer program
        elif button == '_cpu_':
            pass        # add your call to launch a CPU measuring utility
if __name__ == '__main__':
    ShowMeTheButtons()

