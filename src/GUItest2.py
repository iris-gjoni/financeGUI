import tkinter as tk
from datetime import datetime
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import ReadStockNames

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

# Create the main window
window = tk.Tk()
window.title("Tkinter with Matplotlib - graphing")
window.geometry("1200x1200")

# Create and pack a Combobox with names from the CSV file
name_label = tk.Label(window, text="Select Stock:")
name_label.grid(column=0, row=0, padx=3, pady=3, sticky="ew")
fields_label = tk.Label(window, text="Select Stock:")
fields_label.grid(column=1, row=0, padx=3, pady=3, sticky="ew")

name_combobox = ttk.Combobox(window, values=names)
name_combobox.grid(column=0, row=1, padx=3, pady=3, sticky="ew")
fields_combobox = ttk.Combobox(window)
fields_combobox.config(state='disabled')
fields_combobox.grid(column=0, row=2, padx=3, pady=3, sticky="ew")
multiplier_combobox = ttk.Combobox(window, values=multipliers)
multiplier_combobox.set(1)
multiplier_combobox.grid(column=0, row=3, padx=3, pady=3, sticky="ew")

name_combobox2 = ttk.Combobox(window, values=names)
name_combobox2.grid(column=1, row=1, padx=3, pady=3, sticky="ew")
fields_combobox2 = ttk.Combobox(window)
fields_combobox2.config(state='disabled')
fields_combobox2.grid(column=1, row=2, padx=3, pady=3, sticky="ew")
multiplier_combobox2 = ttk.Combobox(window, values=multipliers)
multiplier_combobox2.set('1')
multiplier_combobox2.grid(column=1, row=3, padx=3, pady=3, sticky="ew")
graph_type_combobox = ttk.Combobox(window, values=graph_types)
graph_type_combobox.set('line')
graph_type_combobox.grid(column=1, row=4, padx=3, pady=3, sticky="ew")

fig, ax = plt.subplots(figsize=(10, 10))
canvas = FigureCanvasTkAgg(fig, master=window)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(column=0, row=6, columnspan=2, padx=5, pady=5, sticky="ew")

toolbar_frame = tk.Frame(master=window)
toolbar_frame.grid(column=0, row=7, columnspan=2, sticky="ew")
toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)

window.grid_rowconfigure(0, weight=2, minsize="30")
window.grid_rowconfigure(1, weight=2, minsize="30")
window.grid_rowconfigure(2, weight=2, minsize="30")
window.grid_rowconfigure(3, weight=1, minsize="30")
window.grid_rowconfigure(4, weight=1, minsize="30")
window.grid_rowconfigure(5, weight=1, minsize="30")
window.grid_rowconfigure(6, weight=1, minsize="50")
window.grid_rowconfigure(7, weight=1, minsize="30")
window.grid_columnconfigure(0, weight=1, minsize="75")
window.grid_columnconfigure(1, weight=1, minsize="75")


def clear_data():
    ax.clear()
    fields_combobox.set('')
    fields_combobox2.set('')
    canvas.draw()


def plot_data():
    selected_name = keyValues.get(name_combobox.get())
    selected_option = fields_combobox.get()
    selected_name2 = keyValues.get(name_combobox2.get())
    selected_option2 = fields_combobox2.get()
    selected_graph_type: str = graph_type_combobox.get()
    ax.clear()

    if selected_option != '':
        final_string: str = searchfile + selected_name + suffix
        # print("final string {}", final_string)
        df = pd.read_csv(final_string)
        x_values = [datetime.strptime(date, '%Y-%m-%d') for date in df['Date']]
        y_values: float = df[selected_option] * int(multiplier_combobox.get())
        plot_graph(selected_graph_type, selected_name, x_values, y_values)

    if selected_option2 != '':
        final_string: str = searchfile + selected_name2 + suffix
        # print("final string {}", final_string)
        df = pd.read_csv(final_string)
        x_values = [datetime.strptime(date, '%Y-%m-%d') for date in df['Date']]
        y_values: float = df[selected_option2] * int(multiplier_combobox2.get())
        plot_graph(selected_graph_type, selected_name2, x_values, y_values)

    ax.set_title(f'{selected_option} for {selected_name}')
    ax.set_ylabel('Usd')
    ax.legend()
    canvas.draw()


def plot_graph(selected_graph_type, selected_name, x_values, y_values):
    if selected_graph_type == "line":
        ax.plot(x_values, y_values, label=selected_name)
    elif selected_graph_type == "scatter":
        ax.scatter(x_values, y_values, s=1, label=selected_name)
    elif selected_graph_type == "bar":
        ax.bar(x_values, y_values, label=selected_name)


def load_file():
    if not (name_combobox.get() == '' or name_combobox.get() is None):
        fields_combobox.config(state='normal')
        do_load(1)
    if not (name_combobox2.get() == '' or name_combobox2.get() is None):
        fields_combobox2.config(state='normal')
        do_load(2)


def do_load(combo_box):
    selectedComboBox = None
    selectedFields = None
    if combo_box == 1:
        selectedComboBox = name_combobox
        selectedFields = fields_combobox

    if combo_box == 2:
        selectedComboBox = name_combobox2
        selectedFields = fields_combobox2

    selected_name = keyValues.get(selectedComboBox.get())
    finalstring: str = searchfile + selected_name + suffix
    print("final string {}", finalstring)
    df = pd.read_csv(finalstring)
    selectedFields['values'] = df.columns.tolist()


plot_button = tk.Button(window, text="Plot Data", command=plot_data)
plot_button.grid(column=0, row=5, padx=3, pady=3, sticky="ew")
clear_button = tk.Button(window, text="Clear Data", command=clear_data)
clear_button.grid(column=1, row=5, padx=3, pady=3, sticky="ew")

load_button = tk.Button(window, text="Load Data", command=load_file)
load_button.grid(column=0, row=4, padx=3, pady=3, sticky="ew")

# Run the Tkinter event loop
window.mainloop()
