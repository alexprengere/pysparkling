from __future__ import print_function

from pysparkling import Context


def test_broadcast():
    b = Context().broadcast([1, 2, 3])
    assert b.value[0] == 1


def test_parallelize_single_element():
    my_rdd = Context().parallelize([7], 100)
    assert my_rdd.collect()[0] == 7


def test_parallelize_matched_elements():
    my_rdd = Context().parallelize([1, 2, 3, 4, 5], 5)
    assert my_rdd.collect()[2] == 3 and len(my_rdd.collect()) == 5


def test_parallelize_empty_partitions_at_end():
    my_rdd = Context().parallelize(range(3529), 500)
    print(my_rdd.getNumPartitions())
    my_rdd.foreachPartition(lambda p: print(sum(1 for _ in p)))
    assert my_rdd.getNumPartitions() == 500 and my_rdd.count() == 3529


def test_union():
    sc = Context()
    rdd1 = sc.parallelize(['Hello'])
    rdd2 = sc.parallelize(['World'])
    union = sc.union([rdd1, rdd2]).collect()
    assert len(union) == 2 and 'Hello' in union and 'World' in union


def test_version():
    assert isinstance(Context().version, str)


if __name__ == '__main__':
    test_parallelize_empty_partitions_at_end()
