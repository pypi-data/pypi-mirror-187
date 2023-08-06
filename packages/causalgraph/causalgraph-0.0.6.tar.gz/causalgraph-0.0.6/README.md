[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
# causalgraph

A python package made for the representation of Causal Graph data and the storage from related information in a knowledge graph.

## Similar Projects

- [owlready2](https://owlready2.readthedocs.io/en/v0.35/) -> Makes Ontologies and Knowledge Graphs workable in python. Is used for storing information
- [networkX](https://networkx.org/) -> Represent graphs in python; is used as inspiration for the Calls and structure of the project
- [Causal Graphical Models Python Package](https://github.com/ijmbarr/causalgraphicalmodels) -> Major inspiration for this package, but we want to do these things differently:
  - Represent Nodes and Edges as individual objects, establishing the connection to datasources / models
  - usage of [networkX MultiDiGraph](https://networkx.org/documentation/stable/reference/classes/multidigraph.html) as base for the SCMs to support multiple connections (at different times) between nodes   
- [Causal Inference in Statistics](https://github.com/DataForScience/Causality/blob/master/CausalModel.py) -> Python Code accompanying a book, which also implements SCMs (without Time-Series)
