# Python Mesh Library
This library enable you to load stl file (both binary and ascii), manipulate the loaded data (translate, scale and rotate) and export the data in memory to stl file (both binary and ascii).

This library is inspired by [numpy-stl](https://github.com/WoLpH/numpy-stl).

## Feature
- Supported format
    - STL(Binary, ASCII)
    - OBJ(Wavefront, no material supported)

- Manipulation: Support affine transform
    - Translate
    - Rotate
    - Scale
    
- Numpy is used for inner calculation so that it runs fast.
    
## Install
```
pip install pymesh
```

## Requirement
[numpy](http://www.numpy.org/) is required.

## Usage
### Load data
```
# STL
from mesh import stl
m = stl.Stl("sample.stl")

# OBJ
from mesh import obj
m = obj.Obj("sample.obj")
```

### Save data
```
# STL
m.save_stl("out.stl")

# OBJ
m.save_obj("out.obj")
```

### Transform
```
# Translate
m.translate_x(10)

# Rotate
m.rotate_y(30)

# Scale
m.scale(1, 2, 1)
```

## LICENSE
[MIT License](http://takuro.mit-license.org/)
