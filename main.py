from txt_to_excel import convert_to_excel
from plot_and_powerpoint import IV
from plot_and_powerpoint import JV
import os
from tkinter import Tk, Button, Label, Toplevel, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD


functions = {
    'IV': IV,
    'JV': JV,
}


def process_files(files):
    for file in files:
        status_label.config(text=f"Processing {os.path.basename(file)}...")
        root.update()
        status_label.config(text=f"Running excel conversion for {os.path.basename(file)}...\nPlease wait, this step can last up to 2 minutes")
        root.update()
        convert_to_excel(file)
        for func in current_funcs:
            status_label.config(text=f"Excel conversion successfully ended.\nRunning {func} for {os.path.basename(file)}...")
            root.update()
            functions[func](file)
    status_label.config(text="Done!")
    messagebox.showinfo("Success", "Task ended successfully for all files!")


def drop(event):
    files = root.tk.splitlist(event.data)
    process_files(files)


def set_func(func):
    current_funcs[:] = func
    dialog.destroy()


temp = Tk()
temp.withdraw()

current_funcs = []

dialog = Toplevel(temp)
dialog.geometry("200x100")
Label(dialog, text="Do you want I-V or J-V plot?").pack()
Button(dialog, text="I-V", command=lambda: set_func('IV')).pack(fill="x")
Button(dialog, text="J-V", command=lambda: set_func('JV')).pack(fill="x")
Button(dialog, text="Both", command=lambda: set_func(['IV', 'JV'])).pack(fill="x")

dialog.wait_window()

temp.destroy()

root = TkinterDnD.Tk()
root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', drop)

frame = Label(root, text="Drag and drop files here", width=50, height=20)
frame.pack()

status_label= Label(root, text = "")
status_label.pack()

root.mainloop()
