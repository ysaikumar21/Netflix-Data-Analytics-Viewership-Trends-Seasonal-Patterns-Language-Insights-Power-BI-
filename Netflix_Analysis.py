'''This we are going develop the Netflix data set of 2023 that we pull the information about how Netflix Content strategy Analysis with python programming'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
import plotly
import plotly.express as px
import sys
import plotly.graph_objects as go
import plotly.io as pio

class NetflixAnalysis:
    def __init__(self,netflix_data):
        try:
            self.netflix_data=netflix_data
            pio.templates.default = "plotly_white"
            self.netflix_data['Hours Viewed'] = self.netflix_data['Hours Viewed'].replace(',', '', regex=True).astype(float)
        except FileNotFoundError:
            print("Error: File not found.")
        except Exception as e:
            error_type, error_msg, err_line = sys.exc_info()
            print(f"Error from Line {err_line.tblineno} -> type {error_type.__name__} -> Error msg -> {error_msg}")
    def Content_type_Viewership_hours(self):
        try:
            content_type_viwership = self.netflix_data.groupby('Content Type')['Hours Viewed'].sum()
            # aggregate viewership hours by content type
            fig = go.Figure(data=[
                go.Bar(
                    x=content_type_viwership.index,
                    y=content_type_viwership.values,
                    marker_color=['skyblue', 'salmon']
                )
            ])
            fig.update_layout(
                title='Total Viewership Hours by Content Type (2023)',
                xaxis_title='Content Type',
                yaxis_title='Total Hours Viewed (in billions)',
                xaxis_tickangle=0,
                height=500,
                width=800
            )
            fig.show()

        except Exception as e:
            error_type, error_msg, err_line = sys.exc_info()
            print(f"Error from Line {err_line.tblineno} -> type {error_type.__name__} -> Error msg -> {error_msg}")
    def viewership_hours_by_language(self):
        try:
            # aggregate viewership hours by language
            language_viewership = self.netflix_data.groupby('Language Indicator')['Hours Viewed'].sum().sort_values(
                ascending=False)
            fig = go.Figure(data=[
                go.Bar(
                    x=language_viewership.index,
                    y=language_viewership.values,
                    marker_color='lightcoral'
                )
            ])

            fig.update_layout(
                title='Total Viewership Hours by Languages (2023)',
                xaxis_title='Language',
                yaxis_title='Total Hours Viewed (in billions)',
                xaxis_tickangle=0,
                height=600,
                width=1000
            )
            fig.show()
        except Exception as e:
            error_type, error_msg, err_line = sys.exc_info()
            print(f"Error from Line {err_line.tblineno} -> type {error_type.__name__} -> Error msg -> {error_msg}")
    def viewership_hours_by_release_month(self):
        try:
            # convert the "Release Date" to a datetime format and extract the month
            self.netflix_data['Release Date'] = pd.to_datetime(self.netflix_data['Release Date'])
            self.netflix_data['Release Month'] = self.netflix_data['Release Date'].dt.month

            # aggregate viewership hours by release month
            monthly_viewership = self.netflix_data.groupby('Release Month')['Hours Viewed'].sum()

            fig = go.Figure(data=[
                go.Scatter(
                    x=monthly_viewership.index,
                    y=monthly_viewership.values,
                    mode='lines+markers',
                    marker=dict(color='blue'),
                    line=dict(color='blue')
                )
            ])

            fig.update_layout(
                title='Total Viewership Hours by Release Month (2023)',
                xaxis_title='Month',
                yaxis_title='Total Hours Viewed (in billions)',
                xaxis=dict(
                    tickmode='array',
                    tickvals=list(range(1, 13)),
                    ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                ),
                height=600,
                width=1000
            )

            fig.show()
        except Exception as e:
            error_type, error_msg, err_line = sys.exc_info()
            print(f"Error from Line {err_line.tblineno} -> type {error_type.__name__} -> Error msg -> {error_msg}")

    def Top5_titles_by_viewership_hours(self):
        try:
            # extract the top 5 titles based on viewership hours
            top_5_titles = self.netflix_data.nlargest(5, 'Hours Viewed')
            selected_columns=['Title', 'Available Globally?', 'Release Date', 'Hours Viewed', 'Language Indicator', 'Content Type']
            print(f'Top5 viewership Hours movies and Shows are:')
            print(top_5_titles[selected_columns])
        except Exception as e:
            error_type, error_msg, err_line = sys.exc_info()
            print(f"Error from Line {err_line.tblineno} -> type {error_type.__name__} -> Error msg -> {error_msg}")

    def content_type_release_month_vs(self):
        try:
            # aggregate viewership hours by content type and release month
            monthly_viewership_by_type = self.netflix_data.pivot_table(index='Release Month',
                                                                  columns='Content Type',
                                                                  values='Hours Viewed',
                                                                  aggfunc='sum')

            fig = go.Figure()

            for content_type in monthly_viewership_by_type.columns:
                fig.add_trace(
                    go.Scatter(
                        x=monthly_viewership_by_type.index,
                        y=monthly_viewership_by_type[content_type],
                        mode='lines+markers',
                        name=content_type
                    )
                )

            fig.update_layout(
                title='Viewership Trends by Content type and Release Month (2023)',
                xaxis_title='Month',
                yaxis_title='Total Hours Viewed (in billions)',
                xaxis=dict(
                    tickmode='array',
                    tickvals=list(range(1, 13)),
                    ticktext=['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
                ),
                height=600,
                width=1000,
                legend_title='Content type'

            )

            fig.show()
        except Exception as e:
            error_type, error_msg, err_line = sys.exc_info()
            print(f"Error from Line {err_line.tblineno} -> type {error_type.__name__} -> Error msg -> {error_msg}")

    def release_seasons_vs(self):
        try:
            # define seasons based on release months
            def get_season(month):
                if month in [12, 1, 2]:
                    return 'Winter'
                elif month in [3, 4, 5]:
                    return 'Spring'
                elif month in [6, 7, 8]:
                    return 'Summer'
                else:
                    return 'Fall'

            # apply the season categorization to the dataset
            self.netflix_data['Release Season'] = self.netflix_data['Release Month'].apply(get_season)
            # aggregate viewership hours by release season
            seasonal_viewership = self.netflix_data.groupby('Release Season')['Hours Viewed'].sum()
            # order the seasons as 'Winter', 'Spring', 'Summer', 'Fall'
            seasons_order = ['Winter', 'Spring', 'Summer', 'Fall']
            seasonal_viewership = seasonal_viewership.reindex(seasons_order)

            fig = go.Figure(data=[
                go.Bar(
                    x=seasonal_viewership.index,
                    y=seasonal_viewership.values,
                    marker_color='orange'
                )
            ])

            fig.update_layout(
                title='Total Viewership Hours by Release Season (2023)',
                xaxis_title='Season',
                yaxis_title='Total Hours Viewed (in billions)',
                xaxis_tickangle=0,
                height=500,
                width=800,
                xaxis=dict(
                    categoryorder='array',
                    categoryarray=seasons_order
                )
            )

            fig.show()
        except Exception as e:
            error_type, error_msg, err_line = sys.exc_info()
            print(f"Error from Line {err_line.tblineno} -> type {error_type.__name__} -> Error msg -> {error_msg}")

    def monthly_release_vs(self):
        try:
            # let’s analyze the number of content releases and their viewership hours across months
            monthly_releases = self.netflix_data['Release Month'].value_counts().sort_index()
            monthly_viewership = self.netflix_data.groupby('Release Month')['Hours Viewed'].sum()
            fig = go.Figure()
            fig.add_trace(
                go.Bar(
                    x=monthly_releases.index,
                    y=monthly_releases.values,
                    name='Number of Releases',
                    marker_color='goldenrod',
                    opacity=0.7,
                    yaxis='y1'

                )
            )
            fig.add_trace(
                go.Scatter(
                    x=monthly_viewership.index,
                    y=monthly_viewership.values,
                    name='Viewership Hours',
                    mode='lines+markers',
                    marker=dict(color='red'),
                    line=dict(color='red'),
                    yaxis='y2'
                )
            )
            fig.update_layout(
                title='Monthly Release Patterns and Viewership Hours (2023)',
                xaxis=dict(
                    title='Month',
                    tickmode='array',
                    tickvals=list(range(1, 13)),
                    ticktext=['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

                ),
                yaxis=dict(
                    title='Number of Releases',
                    showgrid=False,
                    side='left'
                ),
                yaxis2=dict(
                    title='Total Hours Viewed (in billions)',
                    overlaying='y',
                    side='right',
                    showgrid=False
                ),
                legend=dict(
                    x=1.05,
                    y=1,
                    orientation='v',
                    xanchor='left'
                ),
                height=600,
                width=1000
            )

            fig.show()
        except Exception as e:
            error_type, error_msg, err_line = sys.exc_info()
            print(f"Error from Line {err_line.tblineno} -> type {error_type.__name__} -> Error msg -> {error_msg}")

    def weekdays_release_vs(self):
        try:
            # let’s explore whether Netflix has a preference for releasing content on specific weekdays and how this influences viewership patterns
            self.netflix_data['Release Day'] = self.netflix_data['Release Date'].dt.day_name()
            weekday_releases = self.netflix_data['Release Day'].value_counts().reindex(
                ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            )
            # aggregate viewership hours by day of the week
            weekday_viewership = self.netflix_data.groupby('Release Day')['Hours Viewed'].sum().reindex(
                ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
            fig = go.Figure()
            fig.add_trace(
                go.Bar(
                    x=weekday_releases.index,
                    y=weekday_releases.values,
                    name='Number of releases',
                    marker_color='blue',
                    opacity=0.6,
                    yaxis='y1'

                )
            )
            fig.add_trace(
                go.Scatter(
                    x=weekday_viewership.index,
                    y=weekday_viewership.values,
                    name='Viewership Hours',
                    mode='lines+markers',
                    marker=dict(color='red'),
                    line=dict(color='red'),
                    yaxis='y2'
                )
            )
            fig.update_layout(
                title='Weekly Release Patterns and Viewership Hours (2023)',
                xaxis=dict(
                    title='Day of the Week',
                    categoryorder='array',
                    categoryarray=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                ),
                yaxis=dict(
                    title='Number of Releases',
                    showgrid=False,
                    side='left'
                ),
                yaxis2=dict(
                    title='Total Hours Viewed (in billions)',
                    overlaying='y',
                    side='right',
                    showgrid=False
                ),
                legend=dict(
                    x=1.05,
                    y=1,
                    orientation='v',
                    xanchor='left'
                ),
                height=600,
                width=1000
            )

            fig.show()
        except Exception as e:
            error_type, error_msg, err_line = sys.exc_info()
            print(f"Error from Line {err_line.tblineno} -> type {error_type.__name__} -> Error msg -> {error_msg}")

    def holidays_events_vs(self):
        try:
            # define significant holidays and events in 2023
            important_dates = [
                '2023-01-01',  # new year's day
                '2023-02-14',  # valentine's ay
                '2023-07-04',  # independence day (US)
                '2023-10-31',  # halloween
                '2023-12-25'  # christmas day
            ]
            # convert to datetime
            important_dates = pd.to_datetime(important_dates)
            # check for content releases close to these significant holidays (within a 3-day window)
            holiday_releases = self.netflix_data[self.netflix_data['Release Date'].apply(
                lambda x: any((x - date).days in range(-3, 4) for date in important_dates)
            )]
            # aggregate viewership hours for releases near significant holidays
            holiday_viewership = holiday_releases.groupby('Release Date')['Hours Viewed'].sum()

            selected_columns=['Title', 'Release Date', 'Hours Viewed']
            print(f'Holidays time released movies and shows list :')
            print(holiday_releases[selected_columns])
        except Exception as e:
            error_type, error_msg, err_line = sys.exc_info()
            print(f"Error from Line {err_line.tblineno} -> type {error_type.__name__} -> Error msg -> {error_msg}")

if __name__=='__main__':
    try:
        object=NetflixAnalysis(netflix_data=pd.read_csv('C:\\Users\\Saiku\\Downloads\\Netflix Content Strategy\\netflix_content_2023.csv'))
        object.Content_type_Viewership_hours()
        object.viewership_hours_by_language()
        object.viewership_hours_by_release_month()
        object.Top5_titles_by_viewership_hours()
        object.content_type_release_month_vs()
        object.release_seasons_vs()
        object.monthly_release_vs()
        object.weekdays_release_vs()
        object.holidays_events_vs()


    except Exception as e:
        error_type, error_msg, err_line = sys.exc_info()
        print(f"Error from Line {err_line.tblineno} -> type {error_type.__name__} -> Error msg -> {error_msg}")
