'''
This module contains a class that can be used to create similar groups based 
on correlation for testing purposes.
'''

# Required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Classes
class CorrelTestingGroups:
    '''
    Creates an object containing comparable groups based on correlation.
    It contains the attribute ".groups" which is a list of lists containing:
    - The members of the first group
    - The Pearson correlation coefficient of the first group members
    - The members of the second group
    - The Pearson correlation coefficient of the second group members
    - The correlation coefficient between the first and second group
    Note: the list is ordered in descending order by this last attribute.

    Parameters
    ----------
    :data: pandas dataframe where each column is a possible group member. The 
        dataframe must be ordered in a time series fashion.
    :test: list containing members of the testing group (if desired). Default=None.
    :min_corr: threshold correlation coefficient to form groups.
    :qt_members: list containing the possible quantity of group members.

    Returns
    -------
    A list of lists containing:
    - The members of the first group
    - The Pearson correlation coefficient of the first group members
    - The members of the second group
    - The Pearson correlation coefficient of the second group members
    - The correlation coefficient between the first and second group
    Note: the list is ordered in descending order by this last attribute.

    Examples
    --------
    >> from testgrps import CorrelTestingGroups as ctg
    >> df.head()
    	a	b	c	d	e
    0	491	950	695	334	739
    1	186	232	738	201	692
    2	605	842	828	546	244
    3	191	752	899	821	689
    4	490	525	663	174	897
    ...
    >> test = [a,c]
    >> my_test = ctg.CorrelTestingGroups(data=df, test=test, qt_members=[2, 3])
    
    # This returns the set of groups with highest correlation:
    >> my_test.groups[0]

    # This plots the groups with the highest correlation:
    >> my_test.plot_best_correlated_groups()

    Requirements
    ------------
    - pandas
    - numpy
    - matplotlib.pyplot
    '''
    def __init__(self, data, test=None, min_corr=0.7, qt_members=[10]):
        self.data = data
        self.test = test
        self.min_corr = min_corr
        self.qt_members = qt_members
        self.__find_best_correlated_groups()

    def __find_best_correlated_groups(self):
        data = self.data
        test = self.test
        min_corr = self.min_corr
        qt_members = self.qt_members
        
        # check parameters
        if type(qt_members) != list:
            print('"qt_members" parameter must be a list of possible values.')
            return None

        data_corr = data.corr()
        computed = []
        results = []
        used_grps = []

        if test is None:
            x_vals = [i for i in data.columns]
        else:
            x_vals = [i for i in test]

        for x in x_vals:
            computed.append(x)
            y_vals = [i for i in data.columns if i not in computed]
            
            for y in y_vals:
                for qt in qt_members:
                    # x group
                    xs = [i for i in data_corr[x].sort_values(ascending=False).index if i in x_vals][0:qt]
                    xs.sort()
                    x_avg_corr = data_corr[x][data_corr[x].index.isin(xs)].mean()

                    # y group
                    if test is None:
                        ys = [i for i in data_corr[y].sort_values(ascending=False).index if i not in xs][0:qt]
                    else:
                        ys = [i for i in data_corr[y].sort_values(ascending=False).index if i not in x_vals][0:qt]
                        
                    ys.sort()
                    y_avg_corr = data_corr[y][data_corr[y].index.isin(ys)].mean()
                    # corr xy
                    avg_x_vals = data[xs].mean(axis=1)
                    avg_y_vals = data[ys].mean(axis=1)
                    correlxy = np.corrcoef(avg_x_vals, avg_y_vals)[0][1]

                    if (ys not in used_grps) & (correlxy >= min_corr):
                        used_grps.append(ys)
                        results.append([xs, x_avg_corr, ys, y_avg_corr, correlxy])

        results.sort(key=lambda tup: tup[4], reverse=True)
        self.groups = results

    def plot_best_correlated_groups(self, figsize=(18,4)):
        '''
        This method plots the groups with the highest correlation.
        For more details:
        >> from testgrps import CorrelTestingGroups as ctg
        >> help(ctg)
        '''
        results = self.groups[0]
        data = self.data
        g1 = data[results[0]].mean(axis=1).reset_index(drop=True)
        g2 = data[results[2]].mean(axis=1).reset_index(drop=True)
        plt.figure(figsize=figsize)
        # 1st plot
        plt.subplot(1, 3, 1)
        plt.plot(g1)
        plt.title('Group 1')
        
        # 2nd plot
        plt.subplot(1, 3, 2)
        plt.plot(g2)
        plt.title('Group 2')
        
        # 3rd plot
        plt.subplot(1, 3, 3)
        plt.plot(g1, label='Group 1')
        plt.plot(g2, label='Group 2')
        plt.title(f'Group 1 vs 2: correl of {results[4]:.3f}')
        plt.legend()
