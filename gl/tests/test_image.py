# -*- coding: utf-8 -*-

from PIL import Image
import pytest

from .. import image

def test_power_of_two():
    assert image.power_of_two(2**10) == 2**10
    assert image.power_of_two(2**10+1) == 2**10
    assert image.power_of_two(2**10-1) == 2**10

    assert image.power_of_two(2**10+(2**10/2)) == 2**10
    assert image.power_of_two(2**10+(2**10/2)+1) == 2**11
    assert image.power_of_two(2**10+(2**10/2)-1) == 2**10


def test_power_of_two_with_maximum():
    assert image.power_of_two(2**10, 2**10) == 2**10
    assert image.power_of_two(2**10+1, 2**10) == 2**10
    assert image.power_of_two(2**10-1, 2**10) == 2**10

    assert image.power_of_two(2**10+(2**10/2), 2**10) == 2**10
    assert image.power_of_two(2**10+(2**10/2)+1, 2**10) == 2**10
    assert image.power_of_two(2**10+(2**10/2)-1, 2**10) == 2**10

    with pytest.raises(AssertionError):
        image.power_of_two(2**10, 800)


def test_pot_resize():
    img = Image.new("RGB", (800, 600))
    res = image.pot_resize(img)
    assert res.size == (1024, 768)

    res = image.pot_resize(img, maximum=2**9)
    assert res.size == (512, 384)

    with pytest.raises(AssertionError):
        image.pot_resize(img, maximum=800)
