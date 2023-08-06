import pandas as pd

class Report:

    def __init__(self, file_name):

        """ Generic distribution class for calculating and
        visualizing a probability distribution.
        Attributes:
        mean (float) representing the mean value of the distribution
        stdev (float) representing the standard deviation of the distribution
        data_list (list of floats) a list of floats extracted from the data file
        """

        self.file_name = file_name

    def show_best_campaign(self):
        """Function to read in data from a txt file. The txt file should have
        one number (float) per line. The numbers are stored in the data attribute.

        Args:
        file_name (string): name of a file to read from

        Returns:
        None

        """
        df = pd.read_csv(self.file_name, skiprows=[0, 1], skipfooter=6, engine='python')

        df = df.sort_values(by='Conversions',ascending=False)
        conversions = df['Conversions'].iloc[0]
        cost_per_conversion = df['Cost / conv.'].iloc[0]
        cost = df['Cost'].iloc[0]
        campaign_name = df['Campaign'].iloc[0]
        summary = "The best campaign was {} and it had the following results: \n\n Conversions: {} \n Cost per conversion: {} \n Cost: $ {} ".format(campaign_name, conversions, cost_per_conversion, cost)
        print(summary)
