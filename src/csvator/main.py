import numpy as np
import pandas as pd
from simpleeval import simple_eval
import networkx as nx

class Columna:
    def __init__(self, name, N, distribution, schema=None, params={}):
        self.schema = schema
        self.name = name
        self.N = N # número de observaciones a generar
        self.distribution = distribution # "normal", "catergorical", "discrete"
        self.params = params

    def set_params(self, params):
        self.params = params

    def _generate(self, df, N): # Requires all dependencies to be already sampled
        df_temp = pd.DataFrame()
        for parameter in self.params:
            df_temp[parameter] = simple_eval(self.schema, names={column: df[column]})

        df[self.name] = 0

class DAG:
    def __init__(self, schema, N):
        self.N = N
        self.df = pd.DataFrame()
        self.depends = {column: schema[column].get("depends")
                        for column in schema.keys()}
        self.graph = nx.DiGraph(self.depends).reverse()
        self.columnas = nx.topological_sort(self.graph) # Perfectly sorted!

    def generate(self, columna):
        pass