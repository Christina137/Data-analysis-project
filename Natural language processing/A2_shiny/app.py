from shiny import App, render, ui


import pandas as pd
import matplotlib.pyplot as plt
app_ui = ui.page_fluid(
    ui.input_date_range(
        "daterange", 
        "Date range", 
        start="2020-12-29", 
        end= '2023-03-09'
        ),  
    ui.output_plot('myplot'),
)

def server(input, output, session):
    @output
    @render.plot
    def myplot():
        
        # Read the data
        # select the data for Canada
        
        covid19_vaccine = pd.read_csv("https://raw.githubusercontent.com/govex/COVID-19/master/data_tables/vaccine_data/global_data/time_series_covid19_vaccine_global.csv")
        canada_covid_data = covid19_vaccine[covid19_vaccine['Country_Region'] == 'Canada']
        canada_covid_data['Date'] = pd.to_datetime(canada_covid_data['Date'])

        df = canada_covid_data


        # If you call the data frame as `df`, then the 
        # following codes select the rows in the user 
        # selected date range
        df = df[df['Date'] > pd.Timestamp(input.daterange()[0])]
        df = df[df['Date'] < pd.Timestamp(input.daterange()[1])]
        
        # Create the plot using `df`
        plt.plot(df['Date'], df['Doses_admin'],label='Doses_admin')
        plt.plot(df['Date'], df['People_at_least_one_dose'],label='People_at_least_one_dose')
        plt.yscale("log")
        plt.xticks(rotation=45)
        plt.legend(loc="lower right")

app = App(app_ui, server)