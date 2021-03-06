# Contributing to DefElement
You can contribute to DefElement by forking the [DefElement GitHub repo](https://github.com/mscroggs/defelement.com),
making changes, then opening a pull request.

## Defining an element
Elements in the DefElement database are defined using a yaml file in the `elements/` folder.
The full file for a Lagrange element is:

```
name: Lagrange
html-name: Lagrange
alt-names:
  - Polynomial
  - Galerkin
  - DGT
  - Hdiv trace
  - Q (quadrilaterals and hexahedra)
notes:
  - DGT and Hdiv trace are names given to this element when it is defined on the facets of a mesh.
short-names:
  - P
  - CG
  - DG
exterior-calculus:
  - P-,0,simplex
  - P,0,simplex
  - Q-,0,tp
ndofs:
  interval:
    formula: k+1
    oeis: A000027
  triangle:
    formula: (k+1)(k+2)/2
    oeis: A000217
  tetrahedron:
    formula: (k+1)(k+2)(k+3)/6
    oeis: A000292
  quadrilateral:
    formula: (k+1)^2
    oeis: A000290
  hexahedron:
    formula: (k+1)^3
    oeis: A000578
entity-ndofs:
  vertices:
    formula: 1
    oeis: A000012
  edges:
    formula: k-1
    oeis: A000027
  faces:
    triangle:
      formula: (k-1)(k-2)/2
      oeis: A000217
    quadrilateral:
      formula: (k-1)^2
      oeis: A000290
  volumes:
    tetrahedron:
      formula: (k-1)(k-2)(k-3)/6
      oeis: A000292
    hexahedron:
      formula: (k-1)^3
      oeis: A000578
min-order: 1
categories:
  - scalar
reference elements:
  - interval
  - triangle
  - tetrahedron
  - quadrilateral
  - hexahedron
dofs:
  vertices: point evaluations
  edges: point evaluations
  faces: point evaluations
  volumes: point evaluations
polynomial set:
  interval: poly[k]
  triangle: poly[k]
  tetrahedron: poly[k]
  quadrilateral: qoly[k]
  hexahedron: qoly[k]
symfem:
  interval: Lagrange
  triangle: Lagrange
  tetrahedron: Lagrange
  quadrilateral: Q
  hexahedron: Q
basix: Lagrange
examples:
  - interval,1
  - interval,2
  - interval,3
  - triangle,1
  - triangle,2
  - triangle,3
  - quadrilateral,1
  - quadrilateral,2
  - quadrilateral,3
test: 1
```

The entries in this yaml file are:

<table class='bordered align-left'>
<thead>
<tr><td>Name</td><td>Required</td><td>Description</td></tr>
</thead>
<tr><td>`name`</td><td>Yes</td><td>The name of the element (ascii).</td></tr>
<tr><td>`html-name`</td><td>Yes</td><td>The name of the element, including HTML special characters.</td></tr>
<tr><td>`alt-names`</td><td></td><td>Alternative (HTML) names of the element.</td></tr>
<tr><td>`short-names`</td><td></td><td>Abbreviated names of the element.</td></tr>
<tr><td>`exterior-calculus`</td><td></td><td>The family name and exerior derivatuve order.</td></tr>
<tr><td>`ndofs`</td><td></td><td>The number of DOFs the element has and the A-numbers of the [OEIS](http://oeis.org) sequence(s) giving the number of DOFs.</td></tr>
<tr><td>`entity-ndofs`</td><td></td><td>The number of DOFs the element has per subentity type and the A-numbers of the [OEIS](http://oeis.org) sequence(s) giving the number of DOFs.</td></tr>
<tr><td>`categories`</td><td></td><td>Categories the element belongs to. Categories are defined in the file [`/data/categories`](https://github.com/mscroggs/defelement.com/blob/main/data/categories).</td></tr>
<tr><td>`reference&nbsp;elements`</td><td>Yes</td><td>The reference element(s) that this finite element can be defined on.</td></tr>
<tr><td>`dofs`</td><td></td><td>Description of the DOFs of this element.</td></tr>
<tr><td>`polynomial&nbsp;set`</td><td></td><td>The polynomial set of this element. This can use sets defined in the file [`/data/polysets`](https://github.com/mscroggs/defelement.com/blob/main/data/polysets). Other sets can be given by writing `<k>[LaTeX definition of set]`. Unions of multiple sets can be given, separated by ` && `.</td></tr>
<tr><td>`examples`</td><td></td><td>Reference elements and orders to be included in the examples section of the entry.</td></tr>
<tr><td>`symfem`</td><td></td><td>The string used to define this element in [Symfem](https://github.com/mscroggs/symfem)'s `create_element` function.</td></tr>
<tr><td>`basix`</td><td></td><td>The string used to define this element in [Basix](https://github.com/fenics/basix)'s `create_element` function.</td></tr>
<tr><td>`notes`</td><td></td><td>Notes about the element.</td></tr>
<tr><td>`test`</td><td></td><td>If included, this element's examples will be included when the test version of the website is built. If not, the examples will be skipped to speed up the test build.</td></tr>
</table>
