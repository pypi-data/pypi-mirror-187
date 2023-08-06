import pandas as pd
import matplotlib.pyplot as plt

class ClauseStatistics:
    def __init__(self, path, query_column):
        self.path = path
        self.query_column = query_column
        self.df = pd.read_json(self.path)
        self.order_by = order_by = self.df['query'].str.contains('order_by', case = False)

    def order_by_count(self):
        return order_by.sum()
    
    def order_by_limit_1_count(self):
        self.order_by_limit_1 = self.order_by & self.df[self.query_column].str.contains('limit 1', case = False)
        return self.order_by_limit_1.sum()
    
    def order_by_limit_count(self):
        order_by_limit = self.order_by & self.df[self.query].str.contains('limit', case = False)
        order_by_limit_other_than_1 = order_by_limit.sum() - self.order_by_limit_1.sum()
        return order_by_limit_other_than_1
    def order_by_without_limit_count(self):
        order_by_limit = self.order_by & self.df[self.query].str.contains('limit', case = False)
        order_by_without_limit = self.order_by.sum()- order_by_limit.sum()
        return order_by_without_limit
    def stat(self):
        df1 = pd.DataFrame()
        df1['order_by'] = [self.order_by_count()]
        df1['order_by_limit_1'] = [self.order_by_limit_1()]
        df1['order_by_limit_other_than_1'] = [self.order_by_limit_count()]
        df1['order_by_without_limit'] = [self.order_by_without_limit_count()]
        return df1
    def visual_graph(self):
        df1.plot(kind= 'bar', stacked = False)
        plt.xlabel('caluse Type')
        plt.ylabel('count')
        plt.title('Clause Statistics')
        plt.show()