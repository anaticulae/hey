"""
Start working on footer extractor.

Required resources:

    # PageSize
    # HorizontalLines
    # Text annotated with location

Required API:

    # before/ after method to determine items
"""

from iamraw import BoundingBox
from utila import from_raw_or_path
from yaml import FullLoader
from yaml import load


def work():
    pass


def determine_footer(pagesizes, textlocations, horizontals):
    top, bottom = [], []

    return top, bottom
    # size, border = load_pageborders


def load_textposition(content: str):
    # TODO: This is from rawmaker->position.py,
    # TODO: remove after moving to serialzeraw
    content = from_raw_or_path(content, ftype='yaml')
    loaded = load(content, Loader=FullLoader)

    result = []
    for page in loaded:
        pagedata = {}
        for item in page['content']:
            key, position = item.split(maxsplit=1)
            pagedata[int(key)] = BoundingBox.from_str(position)
        result.append(pagedata)
    return result


TOP_BORDER = 0.1  # Header in the range of 0% till 10%
TOP_MAX_DIFFERENCE = 20.0

BOTTOM_BORDER = 0.9  # Footer is in range of 90% till 100%
BOTTOM_MAX_DIFFERENCE = 10.0


def header(navigator):
    collector = [page.before(TOP_BORDER) for page in navigator]
    common = common_items(collector, max_difference=TOP_MAX_DIFFERENCE)
    return common


def footer(navigator):
    collector = [page.after(BOTTOM_BORDER) for page in navigator]
    common = common_items(collector, max_difference=BOTTOM_MAX_DIFFERENCE)
    return common


def common_items(collected, max_difference):
    flat = []
    for item in collected:
        flat.extend(item)

    clusters = same_area_cluster(
        flat,
        max_difference=max_difference,
    )

    result = [page_from_cluster(cluster, collected) for cluster in clusters]
    return result


def page_from_cluster(cluster, collected):
    result = []
    for pagecount, content in enumerate(collected):
        result.extend([(
            pagecount,
            test,
        ) for test in content if test in cluster])
    return result


def three_side_cluster_equal(todo):

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

    return determine_cluster(todo, classificator)


def same_area_cluster(todo, max_difference=10.0):

    def classificator(candidat, clusteritem, max_difference=max_difference):
        assert max_difference > 0.0

        from math import sqrt

        def distance(x0, y0, x1, y1):
            return sqrt(pow((x0 - x1), 2) + pow((y0 - y1), 2))

        def matcher(candidat, clusteritem):
            testbox, _ = candidat
            goalbox, _ = clusteritem
            equality = distance(
                testbox.x_bottom,
                testbox.y_bottom,
                goalbox.x_bottom,
                goalbox.y_bottom,
            ) + distance(
                testbox.x_top,
                testbox.y_top,
                goalbox.x_top,
                goalbox.y_top,
            )
            return equality <= max_difference

        return matcher(candidat, clusteritem)

    return determine_cluster(todo, classificator)


# TODO: Remove after having classificator in UTILA from rawmaker
def determine_cluster(todo, classificator):
    if not todo:
        return []

    # prepare cluster, a single element is a cluster
    result = [[item] for item in todo]

    def match(result, current):
        for clusterindex, cluster in enumerate(result):
            for clusteritem in cluster:
                match = [
                    classificator(candidat=test, clusteritem=clusteritem)
                    for test in current
                ]
                if any(match):
                    return clusterindex
        return None

    def clusterme(result):
        result, todo = result[0], result[1:]
        if not isinstance(result[0], list):
            result = [result]
        while todo:
            current = todo.pop()
            index = match(result, current)
            if index is None:
                # No match, create new cluster
                result.insert(0, current)
            else:
                result[index].extend(current)
        return result

    # Break when cluster does not change result
    # Cluster till cluster move does not change the result
    before = set()
    while True:
        result = clusterme(result)
        hashid = hash(str(result))
        if hashid in before:
            break
        before.add(hashid)

    # A cluster must have at least 2 items
    clusters = [item for item in result if len(item) > 1]
    return clusters
