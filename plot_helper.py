import plotly.graph_objs as go
import plotly.offline as offline_py
import config as cfg


def generate_ts(data_tuples):
    '''input:
    [ ('Returns', returns, color_scheme['major_line'])]
    '''
    traces = []

    for name, df, color in data_tuples:
        traces.append(go.Scatter(
            name = name,
            x = df.index,
            y = df,
            mode = 'lines',
            line = {'color': color}
        ))

    return traces

def plot_ts(data_tuples, title):
    config  = cfg.generate_config()
    layout  = go.Layout(title=title)

    # data_tuples = [()]
    ts      = generate_ts(data_tuples)
    offline_py.iplot({'data': ts, 'layout':layout}, config=config)

    