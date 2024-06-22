# -*- coding: utf-8 -*-
"""app.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/13T_XcGkL6sIbtiEXEVW99UCFy8riCvNI
"""

import dash
import os
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output


import pandas as pd
import barchart

import preprocess
import descriptions
from visualizations.vis2_3 import tactics_info
from visualizations.vis4 import vis4_goal_diff
from visualizations.vis5 import vis5_total_goals
from visualizations.vis6 import win_loss_outcome
from visualizations.vis7 import vis7_outcome_percentage
from visualizations.match_comp import match_comp

app = dash.Dash(__name__)
# This line is needed for deployment
server = app.server

app.title = 'Euro2020 - INF8808 - Amira Tamakloe'

base_path = os.path.dirname(__file__)
match_info_path = os.path.join(base_path, 'assets/data/match_info.csv')
df = pd.read_csv(match_info_path)

match_comp_path = os.path.join(base_path, 'assets/data/match_comp_stats.csv')
df_comparison = pd.read_csv(match_comp_path)

def prep_data_vis4(df):
    '''
        Imports the .csv file and does some preprocessing.

        Returns:
            A pandas dataframe containing the preprocessed data.
    '''
    df_filtered  = preprocess.drop_useless_columns(df)
    match_df = preprocess.get_statistics(df_filtered)
    

    return match_df

def prep_data_vis5(df):
    sorted_goals = preprocess.vis5_get_total_goals(df)
    goals_df = vis5_total_goals.draw_figure(sorted_goals)

    return goals_df

def prep_data_vis6(df):
    # Process the data
    final_results = win_loss_outcome.dataProcessing(df)
    win_loss_record = win_loss_outcome.calculateWinsLosses(final_results)

    # Generate the chart
    italic_country_names = barchart.MakeItalic(win_loss_record)
    fig = barchart.DrawBarChart(italic_country_names, win_loss_record)
    return fig

def prep_data_vis7(df):
    outcome_percentage = preprocess.vis7_get_outcome_percentage(df)
    outcome_df = vis7_outcome_percentage.draw_figure(outcome_percentage)

    return outcome_df


# TODO: add 5-6 parameters for this function
def init_app_layout(vis4, vis5, vis6, vis7):
    '''
        Generates the HTML layout representing the app.

        Args:
            figure: The figure to display.
        Returns:
            The HTML structure of the app's web page.
    '''
    return html.Div(className='content', children=[
        html.Header(children=[
            html.H1('Euro 2020 Data Analysis'),
        ]),
        html.Main(children=[
            dcc.Tabs([
                dcc.Tab(label='Goals Difference',
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                    children=[
                    html.Div(className='viz-container', children=[
                        html.Div([html.P(descriptions.vis4_description)], className='description'),
                        dcc.Graph(
                            figure=vis4,
                            config=dict(
                                scrollZoom=False,
                                showTips=False,
                                showAxisDragHandles=False,
                                doubleClick=False,
                                displayModeBar=False
                            ),
                            className='graph',
                            id='vis4-goal-diff-chart'
                        )
                    ]),
                ]),
                dcc.Tab(label='Total Goals',
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                    children=[
                    html.Div(className='viz-container', children=[
                        html.Div([html.P(descriptions.vis5_description)], className='description'),
                        dcc.Graph(
                            figure=vis5,
                            config=dict(
                                scrollZoom=False,
                                showTips=False,
                                showAxisDragHandles=False,
                                doubleClick=False,
                                displayModeBar=False
                            ),
                            className='graph',
                            id='vis5-total-goals-chart'
                        )
                    ]),
                ]),
                dcc.Tab(label='Win-Loss Outcome',
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                    children=[
                    html.Div(className='viz-container', children=[
                        html.Div([html.P(descriptions.vis6_description)], className='description'),                        
                        dcc.Graph(
                            figure=vis6,
                            config=dict(
                                scrollZoom=False,
                                showTips=False,
                                showAxisDragHandles=False,
                                doubleClick=False,
                                displayModeBar=False
                            ),
                            className='graph',
                            id='vis6-total-goals-chart'
                        )
                    ]),
                ]),
                dcc.Tab(label='Match Outcome', 
                    className='custom-tab',
                    selected_className='custom-tab--selected',                    
                    children=[
                    html.Div(className='viz-container',
                    children=[
                        html.Div([html.P(descriptions.vis7_description)], className='description'),                        
                        dcc.Graph(
                            figure=vis7,
                            config=dict(
                                scrollZoom=False,
                                showTips=False,
                                showAxisDragHandles=False,
                                doubleClick=False,
                                displayModeBar=False
                            ),
                            className='graph',
                            id='vis7-match-outcome'
                        )
                    ]),
                ]),
                dcc.Tab(label='Match Comparison', 
                    className='custom-tab',
                    selected_className='custom-tab--selected',
                    children=[
                    html.Div(children=[
                        dbc.Row([
                            dbc.Col(),
                            dbc.Col(html.H1('A Visualization of Gaming Results'), width=9, style={'text-align': 'center', 'margin-top': '7px'}),
                            html.Div([html.P(descriptions.vis2_vis3_description)], className='description'),
                        ]),
                        dbc.Row([
                            dbc.Col(sidebar),
                            dbc.Col(dcc.Graph(id='score-graph'), width=9, align='center', style = {'margin-top':'3px'})
                        ]),
                        dbc.Row([
                            dbc.Col(),
                            dbc.Col(dcc.Graph(id='match_stats'),width=9, align='center', style={'margin-top': '3px'})
                        ])
                    ])
                ]),
            ])
        ]),
    ])


# DATA PREP:

# VIS 2-3
tactics_info.register_callbacks(app, df_comparison)

# VIS 4
vis4_data_bar_chart = prep_data_vis4(df)
fig4 = vis4_goal_diff.init_figure()
fig4 = vis4_goal_diff.draw(fig4, vis4_data_bar_chart)

# VIS 5
fig5 = prep_data_vis5(df)

# VIS 6
fig6 = prep_data_vis6(df)

# VIS 7
fig7 = prep_data_vis7(df)

# Sidebar
sidebar = match_comp.create_sidebar_layout(df_comparison)

# TOTAL LAYOUT
app.layout = init_app_layout(fig4, fig5, fig6, fig7)
