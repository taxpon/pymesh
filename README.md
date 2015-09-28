# Python Mesh Library
This library enable you to load stl file (both binary and ascii), manipulate the loaded data (translate, scale and rotate) and export the data in memory to stl file (both binary and ascii).

This library is inspired by [numpy-stl](https://github.com/WoLpH/numpy-stl).

## Install
```
pip install pymesh
```

## Requirement
[numpy](http://www.numpy.org/) is required.

## Usage
```
from mesh import stl

# Load stl data
m = stl.Stl('sample.stl')

# Translate
m.translate_x(10)

# Rotate
m.rotate_y(30)

# Scale
m.scale(1, 2, 1)

# Save
m.save('sample_out.stl')
```

## LICENSE
MIT
