import tkinter as tk
from tkinterdnd2 import TkinterDnD
from excel import Excel_IV, Excel_JV
from init_BD import create_db
from plot_and_powerpoint import PowerPoint_IV, PowerPoint_JV

def drop(event):
    file_path = event.data
    db_results = create_db(file_path)
    create_checkboxes_screen(root, db_results)

def create_drag_and_drop_screen():
    root.geometry('500x500')
    root.configure(bg='white')

    text = tk.Label(root, text="Please drop your txt files below:", background='white')
    text.pack(side='top', fill='x', expand=False)

    dropzone = tk.Frame(root, width=200, height=200, borderwidth=1, highlightthickness=1, highlightbackground='black', highlightcolor='black')
    dropzone.pack(expand=1, fill='both')
    dropzone.drop_target_register('DND_Files')
    dropzone.dnd_bind('<<Drop>>', drop)

    dropzone_text = tk.Label(dropzone, text="Drop files here")
    dropzone_text.pack(expand=True)


def create_checkboxes_screen(root, db_results):
    for widget in root.winfo_children():
        widget.pack_forget()
    root.geometry('500x500')

    item_checkboxes = []
    func_checkboxes = []

    text = tk.Label(root, text="Which of these wafers do you want to proceed?", background='white')
    text.pack(fill='x', expand=False)

    for result in db_results:
        var = tk.IntVar()
        cb = tk.Checkbutton(root, text=result, variable=var, background='white')
        cb.var = var
        cb.pack()
        item_checkboxes.append((cb, var))

    text = tk.Label(root, text="What do you want to create?", background='white')
    text.pack(fill='x', expand=False)

    var_none = tk.IntVar()  # create IntVar for cb_none
    cb_none = tk.Checkbutton(root, text="None", variable=var_none, background='white', command=lambda: disable_other(cb_none, cb_none, var_none, func_checkboxes))
    cb_none.var = var_none
    cb_none.pack()


    cb_vars = [tk.IntVar() for _ in range(4)]
    funcs = [Excel_IV, Excel_JV, PowerPoint_IV, PowerPoint_JV]



    for func, var in zip(funcs, cb_vars):
        cb = tk.Checkbutton(root, text=func.__name__, variable=var, background='white')
        cb.var = var
        cb.config(command=lambda cb=cb: disable_other(cb, cb_none, var_none, func_checkboxes))
        cb.pack()
        func_checkboxes.append((cb, func))


    proceed_button = tk.Button(root, text="Proceed", command=lambda: proceed(item_checkboxes, func_checkboxes))
    proceed_button.pack()

def disable_other(clicked_cb, cb_none, var_none, func_checkboxes):
    if clicked_cb == cb_none and var_none.get() == 1:
        for checkbox, _ in func_checkboxes:
            if checkbox != cb_none:
                checkbox.var.set(0)
    elif clicked_cb != cb_none and clicked_cb.var.get() == 1:
        cb_none.var.set(0)

def proceed(item_checkboxes, func_checkboxes):
    update = tk.Label(root, text="Please wait, treatment in progress...", background='white')
    update.pack(fill='x', expand=False)

    selected_items = [item[0].cget("text") for item in item_checkboxes if item[1].get() == 1]
    for cb, func in func_checkboxes:
        if cb.var.get() == 1:
            for item in selected_items:
                func(item)

    update.config(text="All wafers proceeded successfully !", background='white')



root = TkinterDnD.Tk()
cb_vars = [tk.IntVar() for _ in range(4)]
item_checkboxes = []
func_checkboxes = []
create_drag_and_drop_screen()
root.mainloop()
