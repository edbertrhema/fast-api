import pytest
from app import add

@pytest.mark.parametrize("num1, num2, expected", [
    (3,2,5)
])
def test_add(num1, num2, expected):
    assert add(num1, num2) == expected

