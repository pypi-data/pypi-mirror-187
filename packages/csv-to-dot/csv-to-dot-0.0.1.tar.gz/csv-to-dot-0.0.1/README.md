# Csv > Dot

Convert a 2 columns CSV file to a .dot, who can be converted with
[Graphviz](https://graphviz.org/) to .jpg, .ps, ...

# How to use it

```sh
python entry_points_csv_to_dot/csv_to_dot.py -h
> usage: csv_to_dot [-h] [--csv-file [CSV_FILE]] [--csv-delim [CSV_DELIM]] [--dot-file [DOT_FILE]] [--nodes-shape [NODES_SHAPE]] [--nodes-style [NODES_STYLE]] [--nodes-bg-color [NODES_BG_COLOR]] [--nodes-font-color [NODES_FONT_COLOR]] [--version]
```

* Available node shapes : https://graphviz.org/doc/info/shapes.html
* Node styles : https://graphviz.org/doc/info/shapes.html#styles-for-nodes
* Node font/background colors : https://graphviz.org/docs/attr-types/color/

# Support version

Python : `>=3.9`
