import plotly.graph_objs as go
import plotly.offline as opy

def barchart(budgetmap, spentmap, format):

    x_cats = list(budgetmap.keys())
    y_budget = list(budgetmap.values())
    y_spend = list(spentmap.values())
    y_overlay = []

    # Create the y data for the partially transparent bars
    for i in range(len(y_budget)):
        if y_spend[i] > y_budget[i]:
            y_overlay.append(y_spend[i])
            y_spend[i] = 0
        else:
            y_overlay.append(0)

    trace1 = go.Bar(x=x_cats, y=y_budget, name='Budget', opacity=1, marker_color='rgb(195, 230, 250)')

    trace2 = go.Bar(x=x_cats, y=y_spend, name='Spent So Far', opacity=1, marker_color='rgb(126, 201, 242)')

    # exceeded budget bars
    trace3 = go.Bar(x=x_cats, y=y_overlay, name='Exceeded Budget', opacity=1, marker_color='rgb(242, 138, 150)', hovertemplate='%{y:.2f} Exceeded')

    layout = go.Layout(title='Spending Status', xaxis={'title': 'Categories'}, yaxis={'title': 'Dollars ($)'}, barmode='overlay')

    fig = go.Figure(data=[trace3, trace1, trace2], layout=layout)

    if format == 'jpg':
        return opy.plot(fig, auto_open=False, output_type='div')
    else:
        return opy.plot(fig, auto_open=False, output_type='div')
    
    return html

# def toggle_visibility(data):
    # Get the index of the trace that was clicked
    trace_index = data['points'][0]['curveNumber']

    # Create a list of visibility values for each trace
    visible = [False] * len(data['figure']['data'])
    visible[trace_index] = True

    # Update the figure layout to set the visibility of the traces
    data['figure'].update_layout(
        {'updatemenus': [{
            'buttons': [{
                'args': [{'visible': visible}],
                'label': 'Toggle traces',
                'method': 'update'
            }]
        }]}
    )

def piechart(budgetmap, spentmap):
    spent_labels = list(spentmap.keys())
    spent_values = list(spentmap.values())

    budget_labels = list(budgetmap.keys())
    budget_values = list(budgetmap.values())

    trace1 = go.Pie(labels=spent_labels, values=spent_values, name='Spent So Far', hoverinfo='label+percent+name')
    # trace1.on_click(toggle_visibility)

    # Create the trace for the second pie chart
    trace2 = go.Pie(labels=budget_labels, values=budget_values, name='Budget', hoverinfo='label+percent+name')
    # trace2.on_click(toggle_visibility)

    # Create the layout for the pie chart
    layout = go.Layout(
        title='Spending Breakdown',
        updatemenus=[{
            'type': 'buttons',
            'direction': 'left',
            'showactive': True,
            'buttons': [{
                'label': 'Spent So Far',
                'method': 'update',
                'args': [{'values': [spent_values], 'labels': [spent_labels], 'visible': [True, False]}, {'title': 'Spending Breakdown'}]
            }, {
                'label': 'Budget',
                'method': 'update',
                'args': [{'values': [budget_values], 'labels': [budget_labels], 'visible': [False, True]}, {'title': 'Breakdown According to Budget'}]
            }]
        }],
        annotations=[dict(text='Double-click to switch data', x=0.5, y=0.5, font=dict(size=20), showarrow=False)]
    )

    frames = [go.Frame(data=[go.Pie(labels=budget_labels, values=budget_values, name='Budget', hole=0.5)]),
              go.Frame(data=[go.Pie(labels=spent_labels, values=spent_values, name='Spent', hole=0.5)])]

    fig = go.Figure(data=[trace1, trace2], layout=layout, frames=frames)

    fig.update_traces(hole=.5, hoverinfo="label+percent+name")

    html = opy.plot(fig, auto_open=False, output_type='div')

    return html

budgetmap = {'fashion': 50, 'food': 150, 'utilities': 100, 'transportation': 60}
spentmap = {'fashion': 40, 'food': 100, 'utilities': 140, 'transportation': 80}

html = barchart(budgetmap, spentmap, "html")
html1 = piechart(budgetmap, spentmap)

with open("barchart.html", "w") as file:
    file.write(html)

with open("piechart.html", "w") as file:
    file.write(html1)
