import pandas as pd
import plotly.graph_objects as go


def read_and_convert(input_file_path, year, drain_spacing, start, end):
    # Read the log file using pandas
    df = pd.read_csv(input_file_path, delimiter='\t')
    df['Date'] = pd.Timestamp(f'{year}-01-01') + pd.to_timedelta(df['time'], unit='H')
    start_month = start.split("-")[0]
    start_day = start.split("-")[1]
    end_month = end.split("-")[0]
    end_day = end.split("-")[1]
    start_pd = pd.Timestamp(year=int(year), month=int(start_month), day=int(start_day))
    end_pd = pd.Timestamp(year=int(year), month=int(end_month), day=int(end_day))

    df = df[(df['Date']>start_pd) & (df['Date']<=end_pd)]

    # Converting to [mm]
    df['oPrecSi'] = (df['oPrecSi'] / drain_spacing**2) * 1000
    df['oEvap'] = (df['oEvap'] / drain_spacing**2) * 1000
    df['sEtM'] = (df['sEtM'] / drain_spacing**2) * 1000
    df['sEtF'] = (df['sEtF'] / drain_spacing**2) * 1000
    df['sDit_0'] = (df['sDit_0'] / drain_spacing**2) * 1000
    df['sDit_1'] = (df['sDit_1'] / drain_spacing**2) * 1000
    df['sDra_0'] = (df['sDra_0'] / drain_spacing**2) * 1000
    df['sDra_1'] = (df['sDra_1'] / drain_spacing**2) * 1000
    df['oDit_0'] = (df['oDit_0'] / drain_spacing**2) * 1000

    # Extract data for the plot
    time_hours = df['time']
    precip_data = df['oPrecSi']
    evap_data = df[['oEvap','sEtM','sEtF']].sum(axis=1)
    discharge_to_open_ditch_data = df[['sDit_0','sDit_1']].sum(axis=1)
    drain_discharge_data = df[['sDra_0','sDra_1']].sum(axis=1)
    surface_runoff_data = df['oDit_0']
    snow_water_eq = df['oSnWaVo'] / drain_spacing**2 * 1000

    return (
        df, precip_data, evap_data, discharge_to_open_ditch_data,
        drain_discharge_data, surface_runoff_data, snow_water_eq
    )


#def calc_instant(df):
    #i = 1
    #max_id = df.index.size
    #new_list = []
    #while i < max_id:
        #new_list.append(df.iloc[i] - df.iloc[i-1])
        #i += 1
    #return new_list

def calc_instant(df, date_column):
    i = 1
    max_id = df.index.size
    new_list = [df.iloc[0]]
    while i < max_id:
        new_list.append(df.iloc[i] - df.iloc[i-1])
        i += 1
    return pd.DataFrame(data=new_list, index=date_column)


def create_plot(
    x, y_list, label_list,
    title = "",
    xaxis_title = "Date",
    yaxis_title = "Cumulative [mm]",
    font_size = 18,
    save_name = None,
    scale = 6,
    width = 2*1080,
    height = 1080
):
    fig = go.Figure()
    for y, label in zip(y_list, label_list):
        fig.add_trace(
            go.Scatter(x=list(x), y=list(y), name=label)
        )

    fig.update_layout(
        title = title,
        xaxis_title = xaxis_title,
        yaxis_title = yaxis_title,
        font = dict(size=font_size)
    )

    # Add range slider
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label="1m",
                         step="month",
                         stepmode="backward"),
                    dict(count=6,
                         label="6m",
                         step="month",
                         stepmode="backward"),
                    dict(count=1,
                         label="1y",
                         step="year",
                         stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    fig.show()

    if save_name is not None:
        fig.write_html(save_name + ".html")
        fig.write_image(save_name + ".png", scale=scale, width=width, height=height)
