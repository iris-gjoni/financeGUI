import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import ReadStockNames
import StandardPlot
import GUISizing
import YahooFinUtil

# add new data sets into stockToName.txt
keyValues = ReadStockNames.read_key_value_file("stockToName.txt")
tickers = list(keyValues.values())
names = list(keyValues.keys())
# searchfile - this must be your path to your csv files
searchfile: str = "c:/quant/historicalStockPrices/historical_"
suffix: str = ".csv"
multipliers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '20', '30', '40', '50',
               '100', '150', '200', '300', '500', '1000']
graph_types = ['line', 'scatter']


def clear_data():
    ax.clear()
    y_field_combobox.set('')
    x_field_combobox.set('')
    canvas.draw()


def plot_data():
    selected_names = []
    x_vals = []
    y_vals = []
    selected_multipliers = []
    options = {}
    entries = listbox.get(0, tk.END)
    print("entries", entries)
    for entry in entries:
        name = keyValues.get(entry[0])
        check_options(entry, name, options)
        selected_names.append(name)
        y_vals.append(entry[1])
        x_vals.append(entry[2])
        selected_multipliers.append(int(entry[3]))

    selected_graph_type: str = graph_type_combobox.get()
    ax.clear()

    StandardPlot.plot_data(
        selected_names=selected_names,
        y_vals=y_vals,
        x_vals=x_vals,
        selected_multipliers=selected_multipliers,
        options=options,
        selected_graph_type=selected_graph_type,
        ax=ax,
        canvas=canvas,
        searchfile=searchfile,
        suffix=suffix
    )


def check_options(entry, name, options):
    if len(entry) >= 5:
        append_value(options, name, entry[4])
    if len(entry) >= 6:
        append_value(options, name, entry[5])
    if len(entry) >= 7:
        append_value(options, name, entry[6])
    if len(entry) <= 4:
        append_value(options, name, "0")


def append_value(dict_obj, key, value):
    if key in dict_obj:
        dict_obj[key].append(value)
    else:
        dict_obj[key] = [value]


def read_file():
    if not (name_combobox.get() == '' or name_combobox.get() is None):
        y_field_combobox.config(state='normal')
        x_field_combobox.config(state='normal')
        selected_name = keyValues.get(name_combobox.get())
        final_string: str = searchfile + selected_name + suffix
        # print("final string {}", finalstring)
        df = pd.read_csv(final_string)
        fields_list = df.columns.tolist()
        y_field_combobox['values'] = fields_list
        x_field_combobox['values'] = fields_list
        if fields_list.__contains__("Date"):
            x_field_combobox.set("Date")
        if fields_list.__contains__("date"):
            x_field_combobox.set("date")


def load_data_to_model():
    name = name_combobox.get()
    y_field = y_field_combobox.get()
    x_field = x_field_combobox.get()
    multiplier = multiplier_combobox.get()
    if name and x_field and y_field and multiplier:
        row = [name, y_field, x_field, multiplier]
        listbox.insert(tk.END, row)


def remove_entry():
    curselection = listbox.curselection()
    if curselection:
        listbox.delete(curselection)


def on_name_change(event):
    x_field_combobox['values'] = []
    x_field_combobox.set('')
    y_field_combobox['values'] = []
    y_field_combobox.set('')
    multiplier_combobox.set('1')
    read_file()


def do_refresh():
    name = name_combobox.get()
    if name:
        ticker = keyValues.get(name_combobox.get())
        final_string: str = searchfile + ticker + suffix
        YahooFinUtil.append_new_data(ticker, final_string)


def apply_moving_average():
    try:
        select = listbox.curselection()
        curselection = listbox.get(select)
        ma = ma_num_combobox.get()
        name_for_appending = str(ma) + "dMA"
        tuples = {name_for_appending}
        if name_for_appending not in curselection:
            if curselection:
                new_tuple = tuple((*curselection, *tuples))
                listbox.delete(select)
                listbox.insert(tk.END, new_tuple)
    except:
        print("no selection")


def apply_multiplier():
    try:
        select = listbox.curselection()
        curselection = listbox.get(select)
        mul = multiplier_combobox.get()
        # name_for_appending = str(ma) + "dMA"
        # tuples = {name_for_appending}
        # if name_for_appending not in curselection:
        if curselection:
            temp_list = list(curselection)
            temp_list[3] = mul
            new_tuple = tuple(temp_list)
            listbox.delete(select)
            listbox.insert(tk.END, new_tuple)
    except:
        print("no selection")


# Create the main window
window = tk.Tk()
window.title("Tkinter with Matplotlib - graphing")
window.geometry("1200x1200")

# user inputs
name_label = tk.Label(window, text="Select Stock:")
name_label.grid(column=0, row=0, padx=3, pady=3, sticky="ew")
name_combobox = ttk.Combobox(window, values=names)
name_combobox.grid(column=0, row=1, padx=3, pady=3, sticky="ew")
name_combobox.bind("<<ComboboxSelected>>", on_name_change)
y_field_combobox = ttk.Combobox(window)
y_field_combobox.config(state='disabled')
y_field_combobox.grid(column=0, row=2, padx=3, pady=3, sticky="ew")
x_field_combobox = ttk.Combobox(window)
x_field_combobox.config(state='disabled')
x_field_combobox.grid(column=0, row=3, padx=3, pady=3, sticky="ew")
graph_type_combobox = ttk.Combobox(window, values=graph_types)
graph_type_combobox.set('line')
graph_type_combobox.grid(column=0, row=5, padx=3, pady=3, sticky="ew")

listbox = tk.Listbox(window, width=250, selectmode=tk.SINGLE, exportselection=0)
listbox.grid(column=1, row=0, rowspan=3, padx=3, pady=3)

# graph
fig, ax = plt.subplots(figsize=(10, 10))
canvas = FigureCanvasTkAgg(fig, master=window)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(column=1, row=3, columnspan=10, rowspan=17, padx=5, pady=5, sticky="ew")
toolbar_frame = tk.Frame(master=window)
toolbar_frame.grid(column=1, row=21, columnspan=10, sticky="ew")
toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)

GUISizing.set_grid_sizes(window)

# Buttons
read_button = tk.Button(window, text="Read Csv Data", command=read_file)
read_button.grid(column=0, row=6, padx=10, pady=3, sticky="ew")
load_button = tk.Button(window, text="Load Data into Model", command=load_data_to_model, bg="blue")
load_button.grid(column=0, row=7, padx=10, pady=3, sticky="ew")
plot_button = tk.Button(window, text="Plot DateTime Data", command=plot_data, bg="green")
plot_button.grid(column=0, row=8, padx=10, pady=3, sticky="ew")
clear_button = tk.Button(window, text="Clear Data", command=clear_data)
clear_button.grid(column=0, row=9, padx=10, pady=3, sticky="ew")
refresh_data_entry_button = tk.Button(window, text="Load Latest Data (Yahoo)", command=do_refresh)
refresh_data_entry_button.grid(column=0, row=10, padx=3, pady=3, sticky="ew")
remove_entry_button = tk.Button(window, text="remove selected", command=remove_entry, width=150)
remove_entry_button.grid(column=2, row=0, padx=10, pady=3, sticky="ew")
add_moving_average_button = tk.Button(window, text="add moving average", command=apply_moving_average, width=150)
add_moving_average_button.grid(column=2, row=1, padx=10, pady=3, sticky="ew")
add_multiplier_button = tk.Button(window, text="add multiplier", command=apply_multiplier, width=150)
add_multiplier_button.grid(column=2, row=2, padx=10, pady=3, sticky="ew")
ma_num_combobox = ttk.Combobox(window, values=['14', '50', '200'], width=50)
ma_num_combobox.set('14')
ma_num_combobox.grid(column=3, row=1, padx=3, pady=3, sticky="ew")
multiplier_combobox = ttk.Combobox(window, values=multipliers)
multiplier_combobox.set(1)
multiplier_combobox.grid(column=3, row=2, padx=3, pady=3, sticky="ew")

# Run the Tkinter event loop
window.mainloop()
