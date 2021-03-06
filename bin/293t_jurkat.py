import numpy as np
from sklearn.preprocessing import normalize, LabelEncoder
import sys

from process import load_names, merge_datasets
from scanorama import correct, visualize, process_data
from scanorama import dimensionality_reduce

NAMESPACE = '293t_jurkat'

data_names = [
    'data/293t_jurkat/293t',
    'data/293t_jurkat/jurkat',
    'data/293t_jurkat/jurkat_293t_50_50',
]

if __name__ == '__main__':
    datasets, genes_list, n_cells = load_names(data_names)
    datasets, genes = correct(datasets, genes_list)
    datasets = [ normalize(ds, axis=1) for ds in datasets ]
    datasets_dimred = dimensionality_reduce(datasets)

    labels = []
    names = []
    curr_label = 0
    for i, a in enumerate(datasets):
        labels += list(np.zeros(a.shape[0]) + curr_label)
        names.append(data_names[i])
        curr_label += 1
    labels = np.array(labels, dtype=int)
    
    embedding = visualize(datasets_dimred,
              labels, NAMESPACE + '_ds', names,
              perplexity=600, n_iter=400, size=100)
    
    cell_labels = (
        open('data/cell_labels/293t_jurkat_cluster.txt')
        .read().rstrip().split()
    )
    le = LabelEncoder().fit(cell_labels)
    labels = le.transform(cell_labels)
    cell_types = le.classes_
    
    visualize(None,
              labels, NAMESPACE + '_type', cell_types,
              perplexity=600, n_iter=400, size=100,
              embedding=embedding) 

    # Uncorrected.
    datasets, genes_list, n_cells = load_names(data_names)
    datasets, genes = merge_datasets(datasets, genes_list)
    datasets = [ normalize(ds, axis=1) for ds in datasets ]
    datasets_dimred = dimensionality_reduce(datasets)
    
    visualize(datasets_dimred, labels,
              NAMESPACE + '_type_uncorrected', cell_types,
              perplexity=600, n_iter=400, size=100)
