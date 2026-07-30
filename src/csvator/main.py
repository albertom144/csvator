import numpy as np
import pandas as pd
from simpleeval import simple_eval
import networkx as nx

class Columna:
    def __init__(self, name, N, distribution, params):
        self.name = name
        self.N = N # número de observaciones a generar
        self.distribution = distribution # "normal", "catergorical", "discrete"
        self.params = params

    def generate(self):
        match self.distribution:
            case "normal":
                return self.params["mean"] + np.sqrt(self.params["var"])*np.random.randn(self.N)
            case "discrete":
                return np.random.choice(self.params["states"], size=self.N, p=self.params["p"])
            case "categorical":
                return np.random.binomial(1, self.params["p"], size=self.N)




class DAG:
    def __init__(self, schema, N):
        self.N = N
        self.df = pd.DataFrame()
        self.depends = {column: schema[column].get("depends")
                        for column in schema.keys()}
        self.graph = nx.DiGraph(self.depends).reverse()
        self.columnas = nx.topological_sort(self.graph) # Perfectly sorted!

    def generate(self, columna):
        for columna in self.columnas:
            params = 0