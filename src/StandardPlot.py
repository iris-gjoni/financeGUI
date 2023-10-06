import pandas as pd
import DateFormattingHelper


def plot_data(selected_names, y_vals, x_vals, selected_multipliers, options,
              selected_graph_type, ax, canvas, searchfile, suffix):

    for i, name in enumerate(selected_names):
        y_field = y_vals[i]
        x_field = x_vals[i]
        graph_info = get_graph_info(name, x_field, y_field)
        final_string: str = searchfile + name + suffix

        df = pd.read_csv(final_string)
        y_values: float = df[y_vals[i]] * selected_multipliers[i]

        if x_field == 'Date':
            x_values = [DateFormattingHelper.parse_date(date) for date in df['Date']]
        elif x_field == 'date':
            x_values = [DateFormattingHelper.parse_date(date) for date in df['date']]
        else:
            x_values = df[x_field]
        # print("x: ", x_values)
        # print("y: ", y_values)
        plot_graph(selected_graph_type, graph_info, x_values, y_values, ax)

        for o in options[name]:
            string_o = str(o)
            if "14dMA" in string_o:
                plot_ma_with_num(14, "14dMA", ax, df, graph_info, i, selected_graph_type,
                                 x_values, y_vals, selected_multipliers[i])
            elif "50dMA" in string_o:
                plot_ma_with_num(50, "50dMA", ax, df, graph_info, i, selected_graph_type,
                                 x_values, y_vals, selected_multipliers[i])
            elif "200dMA" in string_o:
                plot_ma_with_num(200, "200dMA", ax, df, graph_info, i, selected_graph_type,
                                 x_values, y_vals, selected_multipliers[i])

    ax.set_title('Price Vs Date')
    ax.legend()
    canvas.draw()


def plot_ma_with_num(num, ma_name, ax, df, graph_info, i, selected_graph_type, x_values, y_vals, mul):
    mv_y_values: float = df[y_vals[i]].rolling(window=num).mean() * mul
    ma_info = graph_info + ma_name
    plot_graph(selected_graph_type, ma_info, x_values, mv_y_values, ax)


def get_graph_info(name, x_field, y_field):
    graph_info = ''
    graph_info += name
    graph_info += ", "
    graph_info += y_field
    graph_info += ", "
    graph_info += x_field
    return graph_info


def plot_graph(selected_graph_type, selected_name, x_values, y_values, ax):
    if selected_graph_type == "line":
        ax.plot(x_values, y_values, label=selected_name)
    elif selected_graph_type == "scatter":
        ax.scatter(x_values, y_values, s=1, label=selected_name)
    elif selected_graph_type == "bar":
        ax.bar(x_values, y_values, label=selected_name)