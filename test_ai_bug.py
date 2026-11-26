import pytest

from find_max import find_max


@pytest.mark.parametrize(
    ("scores", "expected"),
    [
        pytest.param([30, 90, 50], 90, id="maximum-in-middle"),
        pytest.param([90, 30, 50], 90, id="maximum-at-start"),
        pytest.param([-8, -2, -5], -2, id="all-negative"),
        pytest.param([70, 70, 70], 70, id="all-equal"),
    ],
)
def test_find_max_normal(scores, expected):
    assert find_max(scores) == expected


def test_find_max_empty_list_raises_index_error():
    with pytest.raises(IndexError):
        find_max([])


def test_find_max_single_score():
    assert find_max([42]) == 42


def test_find_max_two_scores_with_larger_second_score():
    assert find_max([10, 20]) == 20


def test_find_max_largest_score_at_end():
    assert find_max([10, 30, 90]) == 90
