import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Use this file to read in your data and prepare the plotly visualizations. The path to the data files are in
# `data/file_name.csv`

def cleandata(dataset):
    """Cleans US Census bureau data for a visualization dashboard.

    Input information here!

    Args:
        dataset (str): name of the excel data file

    Returns:
        cleaned excel file

    """    
    df = pd.read_excel(dataset, skiprows=7).dropna()
    df.columns = ['Year', '10th percentile limit', '20th percentile limit',
       '30th percentile limit', '40th percentile limit', '50th (median)',
       '60th percentile limit', '70th percentile limit',
       '80th percentile limit', '90th percentile limit',
       '95th percentile limit', '90th/10th', '95th/20th', '95th/50th',
       '80th/50th', '80th/20th', '20th/50th']

    to_drop = ['90th/10th', '95th/20th', '95th/50th',
       '80th/50th', '80th/20th', '20th/50th']

    df.drop(to_drop, inplace=True, axis=1)

    df['Year'] = df['Year'].astype(str) + '101'
    df['Year'] = df['Year'].str.extract(r'^(\d{4})')

    # output clean excel file, df[::-1] reverses the dataframe order, return function reverses column order to have synchronous legend order
    df = df[::-1]
    return df[['Year', '95th percentile limit', '90th percentile limit',
       '80th percentile limit', '70th percentile limit', '60th percentile limit',
       '50th (median)', '40th percentile limit',
       '30th percentile limit', '20th percentile limit',
       '10th percentile limit']]

def cleandata_ratio(dataset):
    """Cleans US Census bureau data for a visualization dashboard.

    Input information here!

    Args:
        dataset (str): name of the excel data file

    Returns:
        cleaned excel file

    """    
    df = pd.read_excel(dataset, skiprows=7).dropna()
    df.columns = ['Year', '10th percentile limit', '20th percentile limit',
       '30th percentile limit', '40th percentile limit', '50th (median)',
       '60th percentile limit', '70th percentile limit',
       '80th percentile limit', '90th percentile limit',
       '95th percentile limit', '90th/10th', '95th/20th', '95th/50th',
       '80th/50th', '80th/20th', '20th/50th']

    to_drop = ['10th percentile limit', '20th percentile limit',
       '30th percentile limit', '40th percentile limit', '50th (median)',
       '60th percentile limit', '70th percentile limit',
       '80th percentile limit', '90th percentile limit',
       '95th percentile limit']

    df.drop(to_drop, inplace=True, axis=1)

    df['Year'] = df['Year'].astype(str) + '101'
    df['Year'] = df['Year'].str.extract(r'^(\d{4})')
    df = df.drop(index = [4, 9]) # dropping additional data for 2013, 2017 - can perhaps deal better
    
    # output clean excel file
    df = df.loc[::-1]
    return df[['Year', '90th/10th', '95th/20th', '95th/50th',
       '80th/50th', '80th/20th', '20th/50th']]

def return_figures():
    """Creates [insert number] plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """
 
    df = cleandata('data/tableA4.xlsx')
    
    fig1 = px.line(df,x = 'Year',
                 y = [c for c in df.columns if c != 'Year'],
                 template = 'plotly_white',
                 title = 'Income Percentile', 
             )

    fig1.update_xaxes(tick0=1970, dtick="10",
                 tickformat="%Y"
             )
    
   

    fig2 = px.line(df,x = 'Year',
                 y = ['95th percentile limit', '50th (median)'],
                 color_discrete_map={'95th percentile limit':'#008B8B', '50th (median)':'#00FFFF'},
                 template = 'plotly_white',
                 title = 'Top 5% Income vs Median 50% Income',
             )
    
    fig2.update_xaxes(tick0=1970, dtick="10",
                 tickformat="%Y"
             )

    df_delete_2013_2017 = df.drop(index = [4, 9])
    df_delete_2013_2017['difference'] = df_delete_2013_2017['90th percentile limit'] - df_delete_2013_2017['50th (median)']
    
    fig3 = px.bar(df_delete_2013_2017,x = 'Year',
                 y = df_delete_2013_2017['difference'],
                 template = 'plotly_white',
                 title = 'Difference in Top 10% Income vs. Median 50% Income', 
             )

    fig3.update_xaxes(tick0=1970, dtick="10",
                 tickformat="%Y"
             )
    
    df = cleandata_ratio('data/tableA4.xlsx')
    
    fig4 = px.bar(df,x = 'Year',
                 y = [c for c in df.columns if c != 'Year'],
                 template = 'plotly_white',
                 title = 'Percentile Ratio', 
             )

    fig4.update_xaxes(tick0=1970, dtick="10",
                 tickformat="%Y"
            )
    
    
    # append all charts to the figures list  
    figures = []
    figures.append(fig1)
    figures.append(fig2)
    figures.append(fig3)
    figures.append(fig4)
    
    return figures