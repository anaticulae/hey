# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import math
import typing

import utila


def common_items(
        collected: list,
        max_difference: float = 10.0,
        min_elements=2,
        selector=None,
) -> list:
    """Cluster items due `same_area_cluster`.

    Args:
        collected: items to cluster
        max_difference(float): upper bound of differences which is accepted
                               by classificator as same item.
        min_elements(int): smallest accepted cluster
        selector(callable): select property to cluster
    Returns:
        list of filtered cluster

    Example:
        [
            [(bounds,item), (bounds,item), (bounds,item)],
            [(bounds,item), (bounds,item)],
            [(bounds,item), (bounds,item), (bounds,item), (bounds,item)],
        ]
    """
    assert min_elements >= 1, str(min_elements)
    if selector is None:
        selector = lambda x: x[0]
    flat = utila.flatten(collected)
    assert all([selector(item) is not None for item in flat]), flat
    clusters = same_area_cluster(
        flat,
        max_difference=max_difference,
        min_elements=min_elements,
        selector=selector,
    )
    result = [page_from_cluster(cluster, collected) for cluster in clusters]
    return result


def max_distance(items, diff: float = 1.0, min_elements=2):

    def classifier(candidat, clusteritem):
        return math.fabs(candidat - clusteritem) <= diff

    return determine_cluster(
        items,
        classifier=classifier,
        min_elements=min_elements,
    )


def page_from_cluster(cluster, collected) -> list:
    result = []
    for pagecount, content in enumerate(collected):
        result.extend([(
            pagecount,
            test,
        ) for test in content if test in cluster])
    return result


def three_side_equal_cluster(todo):

    def classificator(candidat, clusteritem):

        def matcher(candidat, clusteritem):
            candidat_pos, _ = candidat
            cluster_pos, _ = clusteritem

            eqaul = sum([
                abs(first - second) < 0.001  # float difference is allowed
                for (first, second) in zip(candidat_pos, cluster_pos)
            ])
            return eqaul >= 3

        return matcher(candidat, clusteritem)

    return determine_cluster(todo, classificator, min_elements=2)


def same_area_cluster(
        todo,
        max_difference: float = 10.0,
        min_elements: int = 2,
        selector=None,
):
    if selector is None:
        selector = lambda x: x[0]

    def classificator(candidat, clusteritem, max_difference=max_difference):

        def distance(x0, y0, x1, y1):
            return math.sqrt(pow((x1 - x0), 2) + pow((y1 - y0), 2))

        def matcher(candidat, clusteritem):
            testbox = selector(candidat)
            goalbox = selector(clusteritem)
            equality = distance(
                testbox[2],
                testbox[3],
                goalbox[2],
                goalbox[3],
            ) + distance(
                testbox[0],
                testbox[1],
                goalbox[0],
                goalbox[1],
            )
            return equality <= max_difference

        return matcher(candidat, clusteritem)

    return determine_cluster(todo, classificator, min_elements=min_elements)


class Cluster:

    def __init__(self, item):
        self.content = [item] if item is not None else []
        self.changed = True

    def extend(self, cluster):
        self.content.extend(cluster.content)
        self.changed = True

    @property
    def center(self):
        if self.changed:
            self.update()
            self.changed = False
        return self.content[0]

    def update(self):
        pass

    def __len__(self):
        return len(self.content)

    def __getitem__(self, index):
        return self.content[index]


Clusters = typing.List[Cluster]


def determine_cluster(
        todo: list,
        classifier: callable,
        min_elements: int = 2,
        ctor: Cluster = None,
) -> Clusters:
    """Determine cluster out of `todo`.

    Sort clustered result by length of cluster descending.
    """
    assert min_elements >= 1, str(min_elements)
    if not todo:
        return []
    if ctor is None:
        ctor = Cluster
    # prepare cluster, a single element is a cluster
    result = [ctor(item) for item in todo]
    # Break when cluster does not change result
    # Cluster till cluster move does not change the result
    before = set()
    while True:
        result = clusterme(result, classifier=classifier)
        if len(result) == 1:
            # all elements are in the same group
            break
        hashid = hash(str(result))
        if hashid in before:
            break
        before.add(hashid)
    # A cluster must have at least 2 items
    clusters = [item for item in result if len(item) >= min_elements]
    clusters = sorted(clusters, key=len, reverse=True)
    return clusters


def match(cluster: Cluster, todo: Clusters, classifier: callable) -> int:
    for clusterindex, candiat in enumerate(todo):
        matched = classifier(
            candidat=candiat.center,
            clusteritem=cluster.center,
        )
        if not matched:
            continue
        return clusterindex
    return None


def clusterme(clusters: Clusters, classifier: callable) -> Clusters:
    current, todo = clusters[0], clusters[1:]
    result = [current]
    while todo:
        test = todo.pop()
        index = match(test, result, classifier)
        if index is None:
            # No match, create new cluster
            result.insert(0, test)
        else:
            result[index].extend(test)
    return result
