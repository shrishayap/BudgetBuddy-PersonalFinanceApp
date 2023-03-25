import plotly.graph_objs as go
import plotly.offline as opy

def charts(budgetmap, spentmap):

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

    # Create the layout for the bar chart
    layout = go.Layout(title='Spending Status', xaxis={'title': 'Categories'}, yaxis={'title': 'Dollars ($)'}, barmode='overlay')

    fig = go.Figure(data=[trace3, trace1, trace2], layout=layout)

    # Export figure to HTML
    html = opy.plot(fig, auto_open=False, output_type='div')
    
    return html

budgetmap = {'fashion': 50, 'food': 150, 'utilities': 100, 'transportation': 60}
spentmap = {'fashion': 40, 'food': 100, 'utilities': 140, 'transportation': 80}

html = charts(budgetmap, spentmap)

with open("charts.html", "w") as file:
    file.write(html)
