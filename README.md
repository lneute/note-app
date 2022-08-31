# Neute's Note Takiing App

Albert already has a few plugins to deal with taking notes, but, i've tried them and they were fine, but i wanted somethig different, so, i proceed to create my own note taking plugin for albert omnilauncher.

## Dependencies:

The **python** side of the dependencies is covered already, i'm keep it simple and this application uses only standard python modules, so any python instalation should work fine.

I've also tried to use only standard applications to completement funcinalities, and all of the system requirements should be fuffiled by default, but in any case, the suystem dependencies are:

* [zenity](https://help.gnome.org/users/zenity/stable/): Is an application writen in GTK that is used to create dialog boxes to display information to the user, this app is used to show a note on the screen

* [notify-send](https://wiki.archlinux.org/title/Desktop_notifications): Is used to inform certain erros to the user.

* Any text editor: Used to edit a note.

## Usage:

<trigger>: '? ' - Activate the application, it will only show created notes

* The first thing you should do is define your prefered text editor:
  
  * Trigger the application: '? '
  
  * Use the 'cfg ' keyword to show all the configurations avaliable
  
  * Then use the keyword 'set ' and the property name:value to be set, the complete command is like this:
    
    `? cfg set text-editor:xed `  
  
  * *(Optional)* You can also set arguments to your text editor, you have to use the property text-editor-params and the arguments should be separated by a space, like this:
    
    `? cfg set text-editor-params:--standalone --new-window`



#### Create a new note

Use the keyword 'new ' followed by the note title and body separated by a ':' (colon), like this `? new this is a title:this is the note body, here you can write anything`

#### Edit a note

To be able to edit a note, you have to setup any text editor, assuming you aready did that, just activate the application with the trigger and then navigate to the note you want to edit, press and hold `ALT`, select *Edit Note* then [ENTER], it will open your text editor with your note, just edit, then, save it, any modifications will be imidiatly be avaliable through albert

Ps.: There's only one rule, DO NOT mess with the note structure, a note shoul look like this:

```
Title of your note
--------------------
Here you have te note body, see? the title and the body 
are separated by a few dashes '---', you shoud keep it like this.
```

#### Delete Note

To delete a note, simply navigate to the note you want to delete press and hold `ALT`and select *Delete Note*, this is irreversible, be carefull.

#### Show Note

The show note action is the default, just select a note then press enter, it will open a dialog box with your note.

#### Seach

To search just type anything about the note, you can use the title, body, name or id, it has a automatic filter system, just type away



### Technicalities

The notes are stores at this path: `/home/USERNAME/Documents/notes` and the notes are simple **.txt** files, they are named using the epoch timestamp format at the time of creation.

> More about that: [Unix time - Wikipedia](https://en.wikipedia.org/wiki/Unix_time)

The **settings.json** file stores your text editor configurations, so, unless you know waht you're doing, dont mess with it.


