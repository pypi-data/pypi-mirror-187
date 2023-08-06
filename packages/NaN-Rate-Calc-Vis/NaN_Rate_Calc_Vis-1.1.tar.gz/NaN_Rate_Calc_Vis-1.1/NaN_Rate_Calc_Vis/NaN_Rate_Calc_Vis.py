import matplotlib.pyplot as plt
import pandas as pd

class NaN_Rate_Calc_Vis:
    '''
    The NaN_Rate_Calc_Vis class is used to calculate, analyze and 
    visualize the NaN values in a given Dataframe.
    '''
    def __init__(self, df):
        '''
        Initialize the class with a Dataframe.
        
        Parameters:
            df (Dataframe): The Dataframe that needs to be analyzed.
        '''
        
        self.df = df
        self.dict_nan_rate = {}
        self.dict_nan_separation = {}
    
    def nan_quote_df(self):
        ''' 
        Calculate the NaN-Quote of the whole dataframe
        
        INPUT 
        None

        OUTPUT
        dict_nan_rate - dictonary with the columns as 
        keys and the corresponding NaN-rate
        ''' 

        # Create a dictonary to fill it with the columns as keys 
        # and the corresponding NaN-rates.
        for i in self.df:
            self.dict_nan_rate[i] = self.df[i].isna().sum()/len(self.df[i])
        return self.dict_nan_rate
    
    def barchart_columns(self, fig_lenght, fig_wide):
        '''
        Plot the barchart of the NaN rate for all columns of the dataset.
        The method 'nan_quote_df' should be activated. 
        
        INPUT 
        fig_lenght - Lenght of the ploted figure
        fig_wide - Wide of the ploted figure

        OUTPUT
        None - Plot barchart
        '''
        
        # Definie figure size
        plt.figure(figsize=(fig_lenght, fig_wide))
        # create a new axis
        ax = plt.axes()
        # plot the bar chart
        plt.bar(self.dict_nan_rate.keys(), list(self.dict_nan_rate.values()),\
                width=0.3)
        plt.title("NaN-rate For All Columns Of The Dataset")
        plt.ylabel("NaN-Rate")
        plt.xlabel("Columns Of The Dataframe")
        plt.setp(ax.get_xticklabels(), rotation=90, ha='right')
        plt.grid(alpha=0.5)
        plt.show()
    
    def infl_nan_columns(self, column, na_column):
        ''' 
        Create a dictonary which shows the nan quote of one column 
        related to the other column. This helps to understand if specific 
        unique values  of an column have an influence on the nan-quote 
        of another column.
        
        INPUT 
        column - The target column to check the influence
        na_column - The column with their nan rates

        OUTPUT
        dict_nan_rate - dictonary with the unique values of a column as 
        keys and the nan rates of the corresponding na_column
        ''' 
        
        self.column = column
        self.na_column = na_column
        
        # Create a list with the unique values of a column
        unique_values = list(self.df[column].unique()) 
        for i in unique_values: # Fill the dictionary with the NaN-rates
            if pd.notna(i):
                self.dict_nan_separation[i] = self.df[self.df\
                [self.column] == i][self.na_column].isna().sum()/len(self.df\
                                                [self.df[self.column] == i])
        return self.dict_nan_separation      
     

    def barchart_infl_nan_columns(self, fig_lenght, fig_wide):
        '''
        Plot the barchart of the NaN rate for all columns of the dataset.
        The method 'infl_nan_columns' should be activated. 
        
        INPUT 
        fig_lenght - Lenght of the ploted figure
        fig_wide - Wide of the ploted figure

        OUTPUT
        None - Plot barchart
        '''
        
        # Definie figure size
        plt.figure(figsize=(fig_lenght, fig_wide))
        # create a new axis
        ax = plt.axes()
        # plot the bar chart
        plt.bar(self.dict_nan_separation.keys(),\
                list(self.dict_nan_separation.values()), width=0.3)
        plt.title("NaN-rate influence of column '{}' to column '{}'"\
                   .format(self.column, self.na_column))
        plt.ylabel("NaN-Rate Of The Column '{}' For The Unique Values Of The Column '{}'".format(self.na_column, self.column))
        plt.xlabel("Unique Values Of Column'{}'".format(self.column))         
        plt.setp(ax.get_xticklabels(), rotation=90, ha='right')
        plt.grid(alpha=0.5)
        plt.show()                   

        
