# Python Mesh Library
## Feature
- Supported format
    - STL(Binary, ASCII)
    - OBJ(Wavefront, no material supported)

- Transform
    - Translate
    - Rotate
    - Scale
    
- Join

- Analyze
    - Volume
    
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
from pymesh import stl
m = stl.Stl("sample.stl")

# OBJ
from pymesh import obj
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

# Method chain supported
m.translate_x(10).rotate_y(30).scale(10, 1, 1)
```

### Join
- Combine multiple mesh data into one mesh
```
# Join
m.join(another)
```

### Analyze
```
# Volume
m.get_volume()
```

### Support
- Python2.7+
- Currently Python3 is not supported. It will be supported in near future.

## LICENSE
[MIT License](http://takuro.mit-license.org/)

## MISC
This library is inspired by [numpy-stl](https://github.com/WoLpH/numpy-stl).