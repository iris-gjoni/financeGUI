import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import ReadStockNames
import StandardPlotAgainstDate
import GUIOrganisation

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
    fields_combobox.set('')
    canvas.draw()


def plot_data_datetime():
    selected_names = []
    selected_options = []
    selected_multipliers = []
    entries = listbox.get(0, tk.END)
    # print(entries)
    for entry in entries:
        selected_names.append(keyValues.get(entry[0]))
        selected_options.append(entry[1])
        selected_multipliers.append(int(entry[2]))

    selected_graph_type: str = graph_type_combobox.get()
    ax.clear()

    StandardPlotAgainstDate.plot_data(
        selected_names=selected_names,
        selected_options=selected_options,
        selected_multipliers=selected_multipliers,
        selected_graph_type=selected_graph_type,
        ax=ax,
        canvas=canvas,
        searchfile=searchfile,
        suffix=suffix
    )


def read_file():
    if not (name_combobox.get() == '' or name_combobox.get() is None):
        fields_combobox.config(state='normal')
        selected_name = keyValues.get(name_combobox.get())
        finalstring: str = searchfile + selected_name + suffix
        # print("final string {}", finalstring)
        df = pd.read_csv(finalstring)
        fields_combobox['values'] = df.columns.tolist()


def load_data_to_model():
    name = name_combobox.get()
    field = fields_combobox.get()
    multiplier = multiplier_combobox.get()
    if name and field and multiplier:
        row = [name, field, multiplier]
        listbox.insert(tk.END, row)


def remove_entry():
    curselection = listbox.curselection()
    if curselection:
        listbox.delete(curselection)


# Create the main window
window = tk.Tk()
window.title("Tkinter with Matplotlib - graphing")
window.geometry("1200x1200")

# user inputs
name_label = tk.Label(window, text="Select Stock:")
name_label.grid(column=0, row=0, padx=3, pady=3, sticky="ew")
name_combobox = ttk.Combobox(window, values=names)
name_combobox.grid(column=0, row=1, padx=3, pady=3, sticky="ew")
fields_combobox = ttk.Combobox(window)
fields_combobox.config(state='disabled')
fields_combobox.grid(column=0, row=2, padx=3, pady=3, sticky="ew")
multiplier_combobox = ttk.Combobox(window, values=multipliers)
multiplier_combobox.set(1)
multiplier_combobox.grid(column=0, row=3, padx=3, pady=3, sticky="ew")
graph_type_combobox = ttk.Combobox(window, values=graph_types)
graph_type_combobox.set('line')
graph_type_combobox.grid(column=0, row=4, padx=3, pady=3, sticky="ew")

listbox = tk.Listbox(window, selectmode=tk.SINGLE, exportselection=0)
listbox.grid(column=1, row=0, rowspan=3, padx=3, pady=3)

# graph
fig, ax = plt.subplots(figsize=(10, 10))
canvas = FigureCanvasTkAgg(fig, master=window)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(column=1, row=3, columnspan=10, rowspan=17, padx=5, pady=5, sticky="ew")
toolbar_frame = tk.Frame(master=window)
toolbar_frame.grid(column=1, row=21, columnspan=10, sticky="ew")
toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)

GUIOrganisation.set_grid_sizes(window)

# Buttons
plot_button = tk.Button(window, text="Plot DateTime Data", command=plot_data_datetime)
plot_button.grid(column=0, row=7, padx=3, pady=3, sticky="ew")
clear_button = tk.Button(window, text="Clear Data", command=clear_data)
clear_button.grid(column=0, row=8, padx=3, pady=3, sticky="ew")
load_button = tk.Button(window, text="Read Csv Data", command=read_file)
load_button.grid(column=0, row=5, padx=3, pady=3, sticky="ew")
read_button = tk.Button(window, text="Load Data into Model", command=load_data_to_model)
read_button.grid(column=0, row=6, padx=3, pady=3, sticky="ew")
remove_entry_button = tk.Button(window, text="remove selected", command=remove_entry)
remove_entry_button.grid(column=2, row=1, padx=3, pady=3, sticky="ew")

# Run the Tkinter event loop
window.mainloop()