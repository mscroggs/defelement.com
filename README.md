# DefElement
This repo contains code to generate the website
[DefElement: an encylopedia of finite element definitions](https://defelement.com).

The code to generate the DefElement website (contained in `builder/` and `templates/`, plus the file `build.py`) is released
under an [MIT license](LICENSE.txt).
The content of the DefElement website itself (including that in `elements/`, `files/`, `pages/`)
is released under a
[Creative Commons Attribution 4.0 International (CC BY 4.0) license](LICENSE-CC.txt).

## Building the website
Before building the website, you must install the required Python dependencies:

```bash
pip3 install -r requirements.txt
```

The html files for the website can be built by running:

```bash
python build.py
```

A smaller version of the website (that will be faster to build) can be built by running:

```bash
python build.py --test
```

