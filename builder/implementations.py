import re


def _parse_value(v):
    v = v.strip()
    if v[0] == "[" and v[-1] == "]":
        return [_parse_value(i) for i in v[1:-1].split(";")]
    if re.match(r"[0-9]+$", v):
        return int(v)
    return v


def parse_example(e):
    if " {" in e:
        e, rest = e.split(" {")
        rest = rest.split("}")[0]
        while re.search(r"\[([^\]]*),", rest):
            rest = re.sub(r"\[([^\]]*),", r"[\1;", rest)
        kwargs = {}
        for i in rest.split(","):
            key, value = i.split("=")
            kwargs[key] = _parse_value(value)
    else:
        kwargs = {}
    ref, order = e.split(",")
    return ref, int(order), kwargs


def symfem_example(element):
    out = "import symfem"
    for e in element.examples:
        ref, ord, kwargs = parse_example(e)
        ord = int(ord)

        symfem_name, params = element.get_implementation_string("symfem", ref)

        if symfem_name is not None:
            out += "\n\n"
            out += f"# Create {element.name} order {ord} on a {ref}\n"
            if ref == "dual polygon":
                out += f"element = symfem.create_element(\"{ref}(4)\","
            else:
                out += f"element = symfem.create_element(\"{ref}\","
            if "variant" in params:
                out += f" \"{symfem_name}\", {ord}, variant=\"{params['variant']}\""
            else:
                out += f" \"{symfem_name}\", {ord}"
            for i, j in kwargs.items():
                if isinstance(j, str):
                    out += f", {i}=\"{j}\""
                else:
                    out += f", {i}={j}"
            out += ")"
    return out


def basix_example(element):
    out = "import basix"
    for e in element.examples:
        ref, ord, kwargs = parse_example(e)
        assert len(kwargs) == 0
        ord = int(ord)

        basix_name, params = element.get_implementation_string("basix", ref)

        if basix_name is not None:
            out += "\n\n"
            out += f"# Create {element.name} order {ord} on a {ref}\n"
            out += "element = basix.create_element("
            out += f"basix.ElementFamily.{basix_name}, basix.CellType.{ref}, {ord}"
            if "lagrange_variant" in params:
                out += f", lagrange_variant=basix.LagrangeVariant.{params['lagrange_variant']}"
            if "dpc_variant" in params:
                out += f", dpc_variant=basix.DPCVariant.{params['dpc_variant']}"
            if "discontinuous" in params:
                if params["discontinuous"] == "True":
                    out += ", discontinuous=True"
                else:
                    assert params["discontinuous"] == "False"
                    out += ", discontinuous=False"
            out += ")"
    return out


def ufl_example(element):
    out = "import ufl"
    for e in element.examples:
        ref, ord, kwargs = parse_example(e)
        assert len(kwargs) == 0
        ord = int(ord)

        ufl_name, params = element.get_implementation_string("ufl", ref)

        if ufl_name is not None:
            out += "\n\n"
            out += f"# Create {element.name} order {ord} on a {ref}\n"
            if "type" in params:
                out += f"element = ufl.{params['type']}("
            else:
                out += "element = ufl.FiniteElement("
            out += f"\"{ufl_name}\", \"{ref}\", {ord})"
    return out


def bempp_example(element):
    out = "import bempp.api"
    out += "\n"
    out += "grid = bempp.api.shapes.regular_sphere(1)"
    for e in element.examples:
        ref, ord, kwargs = parse_example(e)
        assert len(kwargs) == 0
        ord = int(ord)

        bempp_name, params = element.get_implementation_string("bempp", ref)
        if bempp_name is None:
            continue
        orders = [int(i) for i in params["orders"].split(",")]

        if ord in orders:
            out += "\n\n"
            out += f"# Create {element.name} order {ord}\n"
            out += "element = bempp.api.function_space(grid, "
            out += f"\"{bempp_name}\", {ord})"
    return out


def points(ref):
    import numpy as np

    if ref == "interval":
        return np.array([[i / 15] for i in range(16)])
    if ref == "quadrilateral":
        return np.array([[i / 10, j / 10] for i in range(11) for j in range(11)])
    if ref == "hexahedron":
        return np.array([[i / 6, j / 6, k / 6]
                         for i in range(7) for j in range(7) for k in range(7)])
    if ref == "triangle":
        return np.array([[i / 10, j / 10] for i in range(11) for j in range(11 - i)])
    if ref == "tetrahedron":
        return np.array([[i / 6, j / 6, k / 6]
                         for i in range(7) for j in range(7 - i) for k in range(7 - i - j)])
    if ref == "prism":
        return np.array([[i / 6, j / 6, k / 6]
                         for i in range(7) for j in range(7 - i) for k in range(7)])
    if ref == "pyramid":
        return np.array([[i / 6, j / 6, k / 6]
                         for i in range(7) for j in range(7) for k in range(7 - max(i, j))])

    raise ValueError(f"Unsupported cell type: {ref}")


def symfem_tabulate(element, example):
    import numpy as np
    import symfem

    ref, ord, kwargs = parse_example(example)
    ord = int(ord)
    symfem_name, params = element.get_implementation_string("symfem", ref)
    assert symfem_name is not None
    if ref == "dual polygon":
        ref += "(4)"
    e = symfem.create_element(ref, symfem_name, ord, **params)
    return np.array([[float(i) for i in j] for j in e.tabulate_basis(points(ref))])


def basix_tabulate(element, example):
    import basix

    ref, ord, kwargs = parse_example(example)
    assert len(kwargs) == 0
    ord = int(ord)
    basix_name, params = element.get_implementation_string("basix", ref)
    if basix_name is None:
        raise NotImplementedError()
    kwargs = {}
    if "lagrange_variant" in params:
        kwargs["lagrange_variant"] = getattr(basix.LagrangeVariant, params['lagrange_variant'])
    if "dpc_variant" in params:
        kwargs["dpc_variant"] = getattr(basix.DPCVariant, params['dpc_variant'])
    if "discontinuous" in params:
        kwargs["discontinuous"] = params["discontinuous"] == "True"

    e = basix.create_element(
        getattr(basix.ElementFamily, basix_name), getattr(basix.CellType, ref), ord,
        **kwargs)
    table = e.tabulate(0, points(ref))[0]
    return table.reshape((table.shape[0], -1))


examples = {
    "symfem": symfem_example,
    "basix": basix_example,
    "bempp": bempp_example,
    "ufl": ufl_example,
}

verifications = {
    "symfem": symfem_tabulate,
    "basix": basix_tabulate,
}