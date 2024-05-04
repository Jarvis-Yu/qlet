[![PyPI Version](https://img.shields.io/pypi/v/qlet.svg)](https://pypi.org/project/qlet/)
![Python 3.10](https://img.shields.io/badge/python->=3.10-blue.svg)
[![license](https://img.shields.io/github/license/Jarvis-Yu/qlet)](https://github.com/Jarvis-Yu/qlet/blob/master/LICENSE)

# qlet

This is an extension package based on `flet`, which provides a variety of `layouts`
that can auto-resize based on their `ref_parent`.

## Installation

```sh
pip install qlet
```

## Examples

```py
assert isinstance(root_item, QItem)
root_item.add_children((
    QText(
        text="Hello, qlet",
        text_colour="#000000",
        align=QAlign(0.5, 0.5),  # centre the item
        width_pct=0.5,           # half the width of parent
        height_pct=0.5,          # half the height of parent
        colour="#FFFFFF",        # background colour
    ),
    QItem(
        anchor=QAnchor(left=0),       # adhere to the left
        wh_on_resize=lambda wh: (     # wh is a tuple[parent width, parent height]
            0.3 * min(wh[0], wh[1]),  # child width
            min(wh[0], wh[1]),        # child height
        ),
        colour="#AAAAAA",             # background colour
    ),
))
```

Please check repository directory `examples/` for more code example.
