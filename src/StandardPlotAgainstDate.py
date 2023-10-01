from datetime import datetime
import pandas as pd


def plot_data(selected_names, selected_options, selected_multipliers,
              selected_graph_type, ax, canvas, searchfile, suffix):

    for i, name in enumerate(selected_names):
        final_string: str = searchfile + name + suffix
        print("final string {}", final_string)
        df = pd.read_csv(final_string)
        x_values = [datetime.strptime(date, '%Y-%m-%d') for date in df['Date']]
        y_values: float = df[selected_options[i]] * selected_multipliers[i]
        plot_graph(selected_graph_type, name, x_values, y_values, ax)

    ax.set_title('Price Vs Date')
    ax.set_ylabel('Usd')
    ax.legend()
    canvas.draw()


def plot_graph(selected_graph_type, selected_name, x_values, y_values, ax):
    if selected_graph_type == "line":
        ax.plot(x_values, y_values, label=selected_name)
    elif selected_graph_type == "scatter":
        ax.scatter(x_values, y_values, s=1, label=selected_name)
    elif selected_graph_type == "bar":
        ax.bar(x_values, y_values, label=selected_name)