import env
from pymesh import stl
from pymesh import obj


def main():
    print(stl.__file__)
    empty = stl.Stl()
    e2 = obj.Obj()
    m = stl.Stl('sample.stl')
    m2 = obj.Obj('sample.obj')
    print(m.get_volume())
    m.scale(1, 2, 1)
    m.rotate_x(90)
    m.rotate_y(30)
    m.translate_x(2)
    m.join(m2)
    empty.join(m2)
    empty.join(e2)
    m.save_stl("sample_out.stl", update_normals=True)
    empty.save_stl("empty.stl")


if __name__ == '__main__':
    main()
