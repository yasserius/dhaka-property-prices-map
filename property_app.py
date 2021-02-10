import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd

from plotly import graph_objs as go
from plotly.graph_objs import *
from dash.dependencies import Input, Output, State

import plotly.express as px

px.set_mapbox_access_token("pk.eyJ1IjoiZ2FnYTMzMzUiLCJhIjoiY2trbnY0Y2F2MzQ3aTJ1bW54YnV3ZHppOCJ9.UpPcJzBzRB9zliyJbuOh4A")

# ------------------------------------------------------------------------------

df = pd.read_csv('bproperty_data.csv', index_col=0)

# ------------------------------------------------------------------------------

app = dash.Dash(__name__,
                external_stylesheets=['https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css'])
server = app.server
app.title = 'Property Prices in Dhaka'

# ------------------------------------------------------------------------------

property_types = list(df['Type'].unique())

property_types_box = dcc.Checklist(
    id = 'types-checklist',
    options=[
        {'label': type, 'value': type}
        for type in property_types
    ],
    value=property_types,
    labelStyle={
        'display': 'inline-block',
        # 'margin': '10px',
        'padding': '5px',
        'left': '50px'},
    inputStyle={
        'margin': '5px'},
)

bedrooms = ['Two Beds', 'Three Beds', 'Four Beds', 'Other',]

bedrooms_box = dcc.Checklist(
    id = 'bedrooms-checklist',
    options=[
        {'label': b, 'value': b}
        for b in bedrooms
    ],
    value=bedrooms,
    labelStyle={
        'display': 'inline-block',
        # 'margin': '10px',
        'padding': '5px',
        'left': '50px'},
    inputStyle={
        'margin': '5px'},
)

checklist_section = html.Div([

    html.Div(property_types_box,
        style={
            'display': 'inline-block',
            'verical-align': 'top',
            'width': '50%',
        }),

    html.Div(bedrooms_box,
        style={
            'display': 'inline-block',
            'verical-align': 'top',
            'width': '50%',
        }),

], style={ 'padding': 20, 'padding-bottom': 0, })

# ------------------------------------------------------------------------------

# prices = df['Price']
#
# max_price = prices.max()
# min_price = prices.min()
#
# range = max_price - min_price
#
# def get_lakhs_crores(money):
#     if money < 1e7:
#         output = int(money/1e5)
#         output = "{} lakh".format(output)
#     else:
#         output = int(money/1e7)
#         output = "{} crore".format(output)
#
#     return output

price_slider = html.Div([
    html.Div([
        'Slide to change prices:'
    ], style={
        'width': '20%',
        'min-height': 50,
        'display': 'inline-block',
        'vertical-align': 'top',
        'font-weight': 'bold',
    }),

    html.Div([
            dcc.RangeSlider(
                id='price-slider',
                min=500000,
                max=80000000,
                step=10000,
                # min=min_price,
                # max=max_price,
                # step=range/1000,
                value=[500000, 80000000],
                # value=[min_price, max_price],
                marks={
                # https://community.plotly.com/t/range-slider-labels-not-showing/6605/2
                # key must be int
                    500000: '5 Lakh',
                    10000000: '1 crore',
                    80000000: '8 crore',
                    # min_price: get_lakhs_crores(min_price),
                    # 10000000: get_lakhs_crores(10000000),
                    # max_price: get_lakhs_crores(max_price),
                },
            ),

        ], style={
            'width': '80%',
            'min-height': 50,
            'display': 'inline-block',
            'vertical-align': 'top',
    }),
])

# ------------------------------------------------------------------------------

def get_map(df_inner):
    fig = px.scatter_mapbox(df_inner,
                     lat="Latitude",
                     lon="Longitude",
                     color="Region",
                     hover_name="Location",
                     hover_data={'Latitude': False,
                                 'Longitude': False,
                                 'Location': False,
                                 'Region': False,
                                 'Price': True,
                                 'No. Beds': True,
                                 'No. Baths': True,
                                 'Type':True,},
#                      size=df["Price"]/df["Area"],
                     color_continuous_scale=px.colors.cyclical.IceFire,
                     size_max=30,
                     zoom=10)

    return fig


scatter_map = html.Div(
    [
        dcc.Graph(id='scattermap',
          style={'margin': '10'}),

        html.Div(
        children='Displaying',
        id='count_and_price',
        style={
            # 'margin': 10,
            'padding-bottom': 30}),
    ],
    # className='col-md-6',
    style={
        'text-align': 'center',
    }
)


# ------------------------------------------------------------------------------

def get_histogram(dataframe):
    fig = px.histogram(df, x="Price",
                        # https://plotly.com/python/figure-labels/
                        # labels={
                        #      "Price": "Price in Taka",
                        #      "count": "Number of Properties",
                        # }
    )
    # fig.update_xaxes(visible=False)
    # fig.update_yaxes(visible=False)
    # https://plotly.com/python/reference/layout/#layout-paper_bgcolor
    fig.update_layout(
        yaxis_title="Number of properties",
        xaxis_title="Price in Taka",
        paper_bgcolor="rgb(0,0,0,0)",
        plot_bgcolor="rgb(0,0,0,0)")
    # fig.update_layout(title="Hello")

    # causes errors
    # fig.update_layout(grid_xaxes=[1e5, 1e6])

    # https://plotly.com/python/tick-formatting/
    # https://github.com/d3/d3-format#format
    fig.update_layout(xaxis=dict(tickformat=","))

    return fig

barchart_box = html.Div(
    [

        dcc.Graph(id='barchart',
          figure=get_histogram(df),
          style={
            'margin': 0,
            'height': 300,
            },
          )
    ],
    # className='col-md-6',
)


# ------------------------------------------------------------------------------

header = html.Div(
    [
        html.Div(
            [
                html.H1("Property Prices in Dhaka", style={'color': '#245ead'}),
                html.P("Interactive Map of some property listings from BProperty"),
                html.A("View Code", href="https://github.com/yasserius/dhaka-property-prices-map"),


            ]
        )
    ],
    # className='col-md-6',
    style={
        'padding': 20,
        'padding-bottom': 10,

    }
)

# ------------------------------------------------------------------------------

def get_heatmap(dataframe):
    fig = px.density_mapbox(dataframe,
                     lat="Latitude",
                     lon="Longitude",
                     z=dataframe["Price"] / dataframe["Area"],
                     radius=8,
                     center=dict(lat=23.8103, lon=90.4125),
                     hover_data={'Latitude': False, 'Longitude': False, 'Price': True, 'Region': True},
                     zoom=9,
                     opacity=0.8)
#                      mapbox_style="stamen-terrain")
    return fig

heatmap_box = html.Div([

    html.Div([
        dcc.Graph(id='heatmap',
          figure=get_heatmap(df),
          style={
            'margin': 0,

            },
          )
    ], className='',
    style={
        'padding': 10,
        'min-height': 300,
        'display': 'inline-block',
        'vertical-align': 'top',
        'width': '70%',
    }),

    html.Div([

        html.H2('Heatmap of Property Price per Unit Area')

    ], className='',
    style={
        'padding': 10,
        'display': 'inline-block',
        'vertical-align': 'top',
        'width': '30%',
    }),

], style={
    'padding': 20,
    }
)

# ------------------------------------------------------------------------------

def get_box(text, num, unit, id1, id2):
    box = html.Div(
        [
            html.Div(text,
            style={
             'padding-bottom': 5,
             'font-weight': 'bold',
             'text-transform': 'uppercase',}),

            html.Div(children=f"{num:1,.0f}",
            style={
                # 'padding-bottom': 5,
                'font-size': 30,

            },
            id=id1),

            html.Div(children=unit,
            style={
                # 'padding-bottom': 5,
                'font-size': 10,
                'text-transform': 'uppercase',

            },
            id=id2),

        ], className='',
         style={
            'padding': '10px 20px',
            'display': 'inline-block',
            'vertical-align': 'top',
            'width': '30%',
            'min-width': 250,
        })

    return box

mean_price = df['Price'].mean()
mean_area = df['Area'].mean()

df['Price_per_area'] = df['Price'] / df['Area']

mean_price_per_area = df['Price_per_area'].mean()

avgbox = get_box('Average Price of Property', mean_price, "taka",
                'price-average', 'price-unit')
area_box = get_box('Average Area of Property', mean_area, "square feet",
                    'area-average', 'area-unit')
price_per_area_box = get_box('Average Price per Square Feet of Property', mean_price_per_area, "taka per square feet",
                            'price-per-area-average', 'price-per-unit')

number_boxes = html.Div([
    avgbox,
    area_box,
    price_per_area_box,
])

# ------------------------------------------------------------------------------

def get_barchart_of_types(dataframe):
    types_counts = dataframe['Type'].value_counts().reset_index()
    fig = px.bar(types_counts, x='index', y='Type',
                labels={
                     "index": "Property Type",
                     "Type": "Counts",
                 })
    fig.update_layout(title_text="Counts for Property Type", title_x=0.5,)
    return fig

def get_barchart_of_beds(dataframe):
    beds_counts = dataframe['No. Beds'].value_counts().reset_index()
    beds_counts = beds_counts[beds_counts['index'] < 5]
    fig = px.bar(beds_counts, x='index', y='No. Beds',
                    labels={
                         "index": "Number of Beds",
                         "No. Beds": "Counts",
                     }
                )
    fig.update_layout(
        xaxis = dict(
            tickmode = 'linear',
            tick0 = 0,
            dtick = 1
        ),
        title_text="Counts for Number of Bedrooms", title_x=0.5,
    )
    return fig

types_bedroom_box = html.Div([

    html.Div([
        dcc.Graph(id='barchart-types',
          figure=get_barchart_of_types(df),
          style={
            'margin': 0,

            },
          )
    ], className='',
    style={
        'padding': 10,
        'min-height': 300,
        'display': 'inline-block',
        'vertical-align': 'top',
        'width': '50%',
    }),

    html.Div([
        dcc.Graph(id='barchart-bedrooms',
          figure=get_barchart_of_beds(df),
          style={
            'margin': 0,

            },
          )
    ], className='',
    style={
        'padding': 10,
        'min-height': 300,
        'display': 'inline-block',
        'vertical-align': 'top',
        'width': '50%',
    }),

], style={
    'padding': 20,
    }
)

# ------------------------------------------------------------------------------

app.layout = html.Div(children=[
    header,
    html.Hr(),
    checklist_section,
    scatter_map,
    price_slider,
    barchart_box,
    html.Hr(),
    heatmap_box,
    number_boxes,
    html.Hr(),
    types_bedroom_box,
    html.Hr(),
], className='container')

# ------------------------------------------------------------------------------

def process_bedrooms(input):
    # ['Two Beds', 'Three Beds', 'Four Beds', 'Other',]
    output = []

    if "Two Beds" in input: output.append(2.0)
    if "Three Beds" in input: output.append(3.0)
    if "Four Beds" in input: output.append(4.0)
    if "Other" in input: output = output + [12., 16.,  5.,  1., 27., 22., 20., 36.,  7., 6., 24., 15., 32., 46., 26., 18.,  9.,  8., 14.]

    return output

@app.callback(
    [Output(component_id='scattermap', component_property='figure'),
    Output(component_id='count_and_price', component_property='children'),],
    [Input(component_id='price-slider', component_property='value'),
    Input(component_id='types-checklist', component_property='value'),
    Input(component_id='bedrooms-checklist', component_property='value'),]
)
def update_selected_row_indices(price_range, types, bedrooms):
    df_inner = df.copy()

    df_inner = df_inner[df_inner['Type'].isin(types)]

    bedrooms2 = process_bedrooms(bedrooms)
    df_inner = df_inner[df_inner['No. Beds'].isin(bedrooms2)]

    lower_price = int(price_range[0])
    upper_price = int(price_range[1])

    df_inner = df_inner[df_inner["Price"] > lower_price]
    df_inner = df_inner[df_inner["Price"] < upper_price]

    no_houses = df_inner.shape[0]

    # display_text = f"Displaying {no_houses} properties/apartments."
    display_text = f"Displaying {no_houses} properties/apartments within the price range of {lower_price:,} and {upper_price:,} taka."
    # .format(no_houses, lower_price, upper_price)
    # https://queirozf.com/entries/python-number-formatting-examples

    return get_map(df_inner), display_text

# ------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)
