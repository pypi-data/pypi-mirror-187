import numpy as np
from rdflib import Graph
from typing import Optional, Iterable
import pandas as pd
from scipy.spatial.distance import cdist

import glob


def load_ontology(source, source_type: Optional[str] = 'directory'):

    # if source is a web GitHub repository
    if source_type == 'repo':
        raise NotImplementedError

    # if source is local GitHub repository
    elif source_type == 'directory':
        return get_ontology_files(source)

    # if source is an ontology file
    elif source_type == 'file':
        return read_rdf_files([source])


def get_ontology_files(ontology_path: str, allowed_types: Iterable[str] = (".ttl")):
    paths = glob.glob(ontology_path + "/**", recursive=True)
    filtered_files = list(filter(lambda path: filter_path(path, allowed_types), paths))
    print(f"Found ontology with {len(filtered_files)} files")
    return read_rdf_files(filtered_files)


def filter_path(path: str, types: Iterable[str]):
    for _type in types:
        if path.endswith(_type):
            return True
    return False


def prepare_topics(graph, topics: str = "skos:Concept", labels: str = "skos:prefLabel",
                   select: Optional[Iterable[str]] = None):
    """"""
    columns = ['topic', 'label']
    if select is not None:
        columns = select
    query_select = ' '.join(["?" + field for field in columns])

    query = f"""
    SELECT DISTINCT {query_select} WHERE {{
      ?topic a {topics};
            {labels} ?label.
    }}"""
    return pd.DataFrame(list(graph.query(query)), columns=columns)


def read_rdf_files(file_list: Iterable[str]):
    print(f"Creating graph")
    graph = Graph()
    for file in file_list:
        graph += Graph().parse(file)
    return graph


def predict(
        texts: pd.DataFrame,
        topics: pd.DataFrame,
        top: Optional[int] = None,
        threshold: Optional[float] = None,
        return_distance: Optional[bool] = False,
        details: Optional = True,
        metric: Optional = 'euclidean'
):
    if len(texts.shape) == 1:
        texts = pd.DataFrame(texts).T

    texts_embedding = texts.select_dtypes('float')

    show_cols = ['id']
    if details:
        show_cols = ['id', 'title', 'summary']
    distances = cdist(texts_embedding.values, topics.select_dtypes('float').values, metric=metric)

    if top is not None:
        topic_ids = np.argsort(distances, axis=1)[:, :top]
        mapping = pd.melt(pd.DataFrame(topic_ids).reset_index(), id_vars='index')[['index', 'value']].rename(
            columns={'index': 0, 'value': 1})
    elif threshold is not None:
        topic_ids = np.argwhere(distances <= threshold)
        mapping = pd.DataFrame(topic_ids)

    mapping = mapping.sort_values(0)
    result = mapping.merge(texts['id'], right_index=True, left_on=0).merge(topics[show_cols], left_on=1,
                                                                           right_index=True,
                                                                           suffixes=('_text', '_topic'))
    result = result.drop([0, 1], axis=1)
    result = result.sort_values('id_text')
    result = result.reset_index(drop=True)

    if return_distance:
        result['distance'] = distances[mapping.values.T[0], mapping.values.T[1]]

    return result