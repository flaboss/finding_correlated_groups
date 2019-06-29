# finding_correlated_groups
This python module contains a class that can be used to create similar groups based  on correlation for testing purposes.


## Dcomentation:

**The class CorrelTestingGroups**
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

** The method plot_best_correlated_groups(self, figsize=(18,4))**

    This method plots the groups with the highest correlation.
    For more details:
    >> from testgrps import CorrelTestingGroups as ctg
    >> help(ctg)
