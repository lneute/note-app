# -*- coding: utf-8 -*-

"""This is a simple note taking plugin

By default it saves your notes at ~/Documents/notes using the epoch timestamp notaion as filename, each file is one note, you can view, edit, delete, and copy the content to the clipboard.
Don't forget to set a few params like your default text editor and arguments (if needed) to be able to edit notes

You can search notes by Title and content, the question mark show all notes, to search for a specific one just keep typing (case sensitive)

To Register a new note use the syntax: ? new title:content, then confirm

for more information visit: github.com/lneute/albert-note-app

Synopsis: <trigger> <query>"""

from albert import *
from subprocess import Popen
from json import load as jload
from json import dump as jdump

import os
import datetime as dt


__title__ = "Notes App"
__version__ = "0.1.0"
__triggers__ = "? "
__authors__ = "lneute"
__site__ = "github.com"
__exec_deps__ = ["zenity", "notify-send"]

iconPath = iconLookup("text")
path = f"{os.environ['HOME']}/Documents/notes"


# Can be omitted
def initialize():
    pass

def check_dir():
    
    if not os.path.exists(path):
        os.mkdir(path)

# Can be omitted
def finalize():
    pass


def show_msg(title, message):
    cmd = ["zenity", "--info", "--no-markup", f"--title={title.title()}", f"--text={message}", "--icon-name=text"]
    Popen(cmd)


def new(title, note):
    ts = str(int(dt.datetime.now().timestamp()*1000)) + ".txt"
    with open(os.path.join(path, ts), "w+") as file:
        content = f"{title}\n--------------------\n{note}"
        file.write(content)


def read(file):
    with open(os.path.join(path, file), "r") as file:
        contents = file.readlines()
        if not contents:
            return None, None
        title = contents[0]
        note = "".join(contents[2:])
        return (title, note)


def get_settings():
    settings_path = os.path.join(path, "settings.json")
    if os.path.exists(settings_path):
        with open(settings_path, "r") as file:
            settings = jload(file)
            return settings
    else:
        settings = {
            "text-editor":"",
            "text-editor-params":[]
        }
        with open(settings_path, "w") as file:
            jdump(settings, file, indent=2)
        
        show_msg("Check Settings", "Please update the text-editor and params to be able to edit notes (? cfg set setting:value)\nYou can list all settings using: '? cfg '")


def save_setting(obj, key, value):

    if key in obj.keys():
        
        if isinstance(obj[key], list):
            obj[key] = []
            for val in value.split(" "):
                obj[key].append(val)
            with open(os.path.join(path, "settings.json"), "w") as file:
                jdump(obj, file, indent=2)
            return
        
        obj[key] = value
        
        with open(os.path.join(path, "settings.json"), "w") as file:
            jdump(obj, file, indent=2)
        return      
    else:
        os.system(f"notify-send 'Albert Note App' 'Setting: {key} not found'")


def edit(file, text_editor, params):
    _file = os.path.join(path, file)
    cmd = f"{text_editor} {' '.join(params)} {_file}"

    print(cmd)
    os.popen(cmd)


def delete(file):
    filepath = os.path.join(path, file)
    if os.path.exists(filepath):
        os.remove(filepath)

def handleQuery(query):
    if not query.isTriggered:
        return
    check_dir()
    settings = get_settings()
    query.disableSort()

    # Note that when storing a reference to query, e.g. in a closure, you must not use
    # query.isValid. Apart from the query beeing invalid anyway it will crash the appplication.
    # The Python type holds a pointer to the C++ type used for isValid(). The C++ type will be
    # deleted when the query is finished. Therfore getting isValid will result in a SEGFAULT.

    if query.string.startswith("new "):
        title, string = query.string.split("new ")[1].split(":", maxsplit=1)
        return Item(id=__title__,
                    icon=iconLookup("checkmark"),
                    text=f"Save? {title}",
                    subtext=f"Note: {string}", 
                    actions=[FuncAction(text="FuncAction", callable=lambda: new(title, string))])
    
    if query.string.startswith("cfg "):

        if query.string.startswith("cfg set "):

            key, value = query.string.split("cfg ")[1].split(":", maxsplit=1)
            
            return Item(id=__title__,
                        icon=iconLookup("checkmark"),
                        text=f"Set {key} as {value}?",
                        actions=[FuncAction(text="Save Config", callable=lambda: save_setting(settings, key.split(' ')[1], value))])
        else:
            result = []
            
            for k, v in settings.items():
        
                result.append(
                        Item(id=__title__,
                        icon=iconLookup("settings"),
                        text=f"Setting: {k} as {v}"))
            
        return result

    
    results = []
    c = 0
    files = list(filter(lambda x: ".txt" in x, os.listdir(path)))

    files = sorted(files)

    if query.string == "":

        for file in files:
            if ".txt" in file:
                c+=1
                title, note = read(file)
                i = str(c).zfill(3)
                
                if not title and not note:
                    c -= 1
                    continue

                results.append(
                        Item(id=i,
                        icon=iconLookup("text"),
                        text=f"{i}. {title} - [{file.split('.')[0]}]",
                        subtext=f"{note}",
                        actions=[
                                FuncAction(text="Show Note", callable=lambda note=note, title=title: show_msg(title, note)),
                                FuncAction(text="Edit Note", callable=lambda file=file: edit(file, settings["text-editor"], 
                                                                                                settings["text-editor-params"])),
                                FuncAction(text="Delete Note", callable=lambda file=file: delete(file)),
                                ClipAction(text="Copy <title> to clipboard", clipboardText=title),
                                ClipAction(text="Copy <note> to clipboard", clipboardText=note),
                                ClipAction(text="Copy <content> to clipboard", clipboardText=f"{title}{note}")
                                ]
                        )
                        )
    else:
        for file in files:
            if ".txt" in file:
                c+=1
                title, note = read(file)
                i = str(c).zfill(3)
                
                if not title and not note:
                    c -= 1
                    continue
                
                q = query.string.lower()
                if q in title.lower() or q in note.lower() or q in i.lower() or q in file.lower():
                    results.append(
                            Item(id=i,
                            icon=iconLookup("text"),
                            text=f"{i}. {title} - [{file.split('.')[0]}]",
                            subtext=f"{note}",
                            actions=[
                                    FuncAction(text="Show Note", callable=lambda note=note, title=title: show_msg(title, note)),
                                    FuncAction(text="Edit Note", callable=lambda file=file: edit(file, settings["text-editor"], 
                                                                                                    settings["text-editor-params"])),
                                    FuncAction(text="Delete Note", callable=lambda file=file: delete(file)),
                                    ClipAction(text="Copy <title> to clipboard", clipboardText=title),
                                    ClipAction(text="Copy <note> to clipboard", clipboardText=note),
                                    ClipAction(text="Copy <content> to clipboard", clipboardText=f"{title}{note}")
                                    ]
                            )
                            )                        

    return results