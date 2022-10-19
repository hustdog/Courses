import numpy as np
import pandas as pd
import networkx as nx
from scipy.sparse import csr_matrix
import matplotlib
import matplotlib.pyplot as plt
import collections
import scipy
import statistics as stats
import seaborn as sns

df = pd.read_csv("Cooffending1.csv")
df.CrimeDate = pd.to_datetime(df.CrimeDate)
n_cases_raw = len(df)
df = df.drop_duplicates()
df = df.loc[(df['NumberYouthOffenders']>0.5)]
# There are five people who are listed as both M and F, just drop one of them
df = df.drop_duplicates(subset=["OffenderIdentifier", "CrimeIdentifier"])
n_cases = len(df)
n_criminals = len(df.OffenderIdentifier.unique())
n_crimes = len(df.CrimeIdentifier.unique())
df.head()

# Remap to consecutive identifiers
OffenderIdentifier_dict = {OffenderIdentifier: i for i, OffenderIdentifier in enumerate(df.OffenderIdentifier.unique())}
CrimeIdentifier_dict = {CrimeIdentifier: i for i, CrimeIdentifier in enumerate(df.CrimeIdentifier.unique())}

# .replace has a lot of overhead
df.OffenderIdentifier = df.OffenderIdentifier.map(OffenderIdentifier_dict.get)
df.CrimeIdentifier = df.CrimeIdentifier.map(CrimeIdentifier_dict.get)

assert not df.OffenderIdentifier.isnull().any() and not df.CrimeIdentifier.isnull().any()
assert df.CrimeIdentifier.max() == df.CrimeIdentifier.nunique() - 1
assert df.OffenderIdentifier.max() == df.OffenderIdentifier.nunique() - 1

# Build matrix
row = df.OffenderIdentifier
col = df.CrimeIdentifier
vals = np.ones(len(row))

# Sparse representation
crime_matrix = csr_matrix((vals, (row, col)), shape=(row.max() + 1, col.max() + 1))

cooffend_matrix = crime_matrix @ crime_matrix.T

# Save an unmodified copy for later
cooffend_matrix_raw = cooffend_matrix.copy()

# convert to (binary) adj. matrix
# Could use the full cooffending matrix for project
cooffend_matrix[cooffend_matrix > 0] = 1
cooffend_matrix.setdiag(0)
cooffend_matrix.eliminate_zeros() # To avoid self loops since setdiag(0) does not itself change the sparsity pattern

g = nx.from_scipy_sparse_matrix(cooffend_matrix)

g_removed = g.copy()
g_removed.remove_nodes_from(list(nx.isolates(g_removed)))
G3 = g_removed
# print(G3)
degree_sequence = sorted([d for n, d in G3.degree()], reverse=True)
sns.set(font_scale=2)
sns.set_style("white")
ax = sns.displot(data = degree_sequence,  kind="kde", rug = True, height = 8)
ax.set(xlabel="Node degree size",ylabel= "Density",title='Entire graph - Node degree distribution')
plt.show()
# Separate matrices for repeating co-offenders vs non-repeating co-offenders
cooffend_matrix_repeat = cooffend_matrix_raw.copy()
cooffend_matrix_no_repeat = cooffend_matrix_raw.copy()

# Repeating co-offenders: edge strength >= 2
cooffend_matrix_repeat.data[np.where(cooffend_matrix_repeat.data<2)[0]]=0
cooffend_matrix_repeat[cooffend_matrix_repeat > 0] = 1
cooffend_matrix_repeat.setdiag(0)
cooffend_matrix_repeat.eliminate_zeros() # To avoid self loops since setdiag(0) does not itself change the sparsity pattern

# Non-repeating co-offenders: edge strength = 1
cooffend_matrix_no_repeat.data[np.where(cooffend_matrix_no_repeat.data!=1)[0]]=0
cooffend_matrix_no_repeat[cooffend_matrix_no_repeat > 0] = 1
cooffend_matrix_no_repeat.setdiag(0)
cooffend_matrix_no_repeat.eliminate_zeros() # To avoid self loops since setdiag(0) does not itself change the sparsity pattern

g_r = nx.from_scipy_sparse_matrix(cooffend_matrix_repeat)
g_nr = nx.from_scipy_sparse_matrix(cooffend_matrix_no_repeat)

g_r.remove_nodes_from(list(nx.isolates(g_r)))
g_nr.remove_nodes_from(list(nx.isolates(g_nr)))

g_r_component_list = sorted(nx.connected_components(g_r), key=len, reverse=True)
g_nr_component_list = sorted(nx.connected_components(g_nr), key=len, reverse=True)

g_r_largest_component = g_r.subgraph(g_r_component_list[0])
g_nr_largest_component = g_nr.subgraph(g_nr_component_list[0])

g_r_largest_component_clustering = list(nx.clustering(g_r_largest_component).values())
g_nr_largest_component_clustering = list(nx.clustering(g_nr_largest_component).values())

# g_r_largest_component_clustering_sequence = sorted([d for d in g_r_largest_component_clustering], reverse=True)
# g_nr_largest_component_clustering_sequence = sorted([d for d in g_nr_largest_component_clustering], reverse=True)


sns.set(font_scale=2)
sns.set_style("white")
ax = sns.displot(data = g_r_largest_component_clustering,  kind="kde", rug = True, height = 8)
ax.set(xlabel="clustering coefficients size",ylabel= "Density",title='Entire graph - clustering coefficients distribution for Gr')
plt.show()


ax = sns.displot(data = g_nr_largest_component_clustering,  kind="kde", rug = True, height = 8)
ax.set(xlabel="clustering coefficients size",ylabel= "Density",title='Entire graph - clustering coefficients distribution for Gnr')
plt.show()