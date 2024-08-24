from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QInputDialog, QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QHBoxLayout, QVBoxLayout,QInputDialog

import json

apps = QApplication([])
#======================================= note
notes_win = QWidget()
notes_win.setWindowTitle("Notes")
notes_win.resize(900, 600)

list_notes = QListWidget()
list_notes_label = QLabel()

button_note_create = QPushButton('Create note')
button_note_delete = QPushButton('Delete note')
button_note_save = QPushButton('Save note')
# ====================================

#============================== list of tag
field_tag = QLineEdit('')
field_tag.setPlaceholderText('enter tag...')
field_text = QTextEdit()


button_tag_add = QPushButton('Add to note')
button_tag_del = QPushButton('Untag from note')
button_tag_searc = QPushButton('Search notes by tag')


list_tags = QListWidget()
list_tags_label = QLabel('list of tags')
#================================

#================================ menambahkan widget ke layout
layout_notes = QHBoxLayout()
col_1 = QVBoxLayout()
col_1.addWidget(field_text)

col_2 = QVBoxLayout()
col_2.addWidget(list_notes)
col_2.addWidget(list_notes_label)

row_1 = QHBoxLayout()
row_1.addWidget(button_note_create)
row_1.addWidget(button_note_delete)

row_2 = QHBoxLayout()
row_2.addWidget(button_note_save)

col_2.addLayout(row_1)
col_2.addLayout(row_2)

col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)

row_3 = QHBoxLayout()
row_3.addWidget(button_tag_add)
row_3.addWidget(button_tag_del)
row_4 = QHBoxLayout()
row_4.addWidget(button_tag_searc)

col_2.addLayout(row_3)
col_2.addLayout(row_4)

layout_notes.addLayout(col_1, stretch=2)
layout_notes.addLayout(col_2, stretch=1)


#================================
notes_win.setLayout(layout_notes)

def show_notes():
    key = list_notes.selectedItems()[0].text()
    print(key)
    field_text.setText(notes[key]['text'])
    list_tags.clear()
    list_tags.addItems(notes[key]['tags'])

def add_note():
    note_name, ok = QInputDialog.getText(notes_win, "Add Note", "Note name:")
    if ok and note_name != "":
       notes[note_name] = {'text': "", 'tags': []}
       list_notes.addItem(note_name)
       list_tags.addItems(notes[note_name]["tags"])

def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]['text'] = field_text.toPlainText()
        with open("notes_data.json", "w") as file :
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("Select a note to save")

def delete_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_tags.clear()
        field_tag.clear()
        
        list_notes.addItems(notes)
        with open("notes_data.json", "w") as file :
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("Select a note to delete")

def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if not tag in notes[key]["tags"]:
            notes[key]["tags"].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
            with open("notes_data.json", "w") as file :
                json.dump(notes, file, sort_keys=True, ensure_ascii=False)
            print(notes)
    else:
        print("Select a note to add tag")

def delete_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[key]["tags"].remove(tag)
        list_tags.takeItem(list_tags.row(list_tags.selectedItems()[0]))
        field_tag.clear()
        with open("notes_data.json", "w") as file :
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
            print(notes)
    else:
        print("Select a note to delete tag")

def search_note():
    print(button_tag_searc.text())
    tag = field_tag.text()
    if button_tag_searc.text() == "Search notes by tag" and tag:
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]["tags"]:
                notes_filtered[note] = notes[note]

        button_tag_searc.setText("Reset search")
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filtered)

    elif button_tag_searc.text() == "Reset search":
        field_tag.clear()
        list_notes.clear()
        list_tags.clear()

        list_notes.addItems(notes)
        button_tag_searc.setText("Search notes by tag")
    else:
        pass

button_tag_searc.clicked.connect(search_note)
button_tag_del.clicked.connect(delete_tag)
button_tag_add.clicked.connect(add_tag)
button_note_delete.clicked.connect(delete_note)
button_note_save.clicked.connect(save_note)
button_note_create.clicked.connect(add_note)
list_notes.itemClicked.connect(show_notes)

notes_win.show()

with open('notes_data.json', 'r') as file:
    notes = json.load(file)
list_notes.addItems(notes)


apps.exec_()
