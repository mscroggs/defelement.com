import os

import pytest
import yaml

element_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../elements")

inputs = []
for i in os.listdir(element_path):
    if i.endswith(".def"):
        with open(os.path.join(element_path, i)) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        inputs += [(i, c) for c in data["reference-cells"]]


@pytest.mark.parametrize("file, cellname", inputs)
def test_sequence(file, cellname):
    with open(os.path.join(element_path, file)) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    if "mapping" not in data:
        pytest.skip()
    if "sobolev" not in data:
        pytest.skip()

    m = data["mapping"]
    c = data["sobolev"]
    if isinstance(c, dict):
        c = list(c.values())
    else:
        c = [c]

    if m == "identity":
        for i in c:
            assert i in ["L2", "H1", "H2", "H3"]
    elif m == "L2 Piola":
        for i in c:
            assert i in ["L2"]
    elif m == "covariant Piola":
        for i in c:
            assert i == "H(curl)"
    elif m == "contravariant Piola":
        for i in c:
            assert i in ["H(div)", "H1(div)", "H1"]
    elif m == "double covariant Piola":
        for i in c:
            assert i == "H(curl curl)"
    elif m == "double contravariant Piola":
        for i in c:
            assert i in ["H(div div)", "L2"]
    elif m == "covariant-contravariant Piola":
        for i in c:
            assert i == "H(curl div)"
    else:
        pytest.skip(f"Non-standard mapping: {m}")
