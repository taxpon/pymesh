import env
from pymesh import stl
from pymesh import obj


def main():
    m = stl.Stl('sample.stl')
    m2 = obj.Obj('sample.obj')
    print(m.get_volume())
    m.scale(1, 2, 1)
    m.rotate_x(90)
    m.rotate_y(30)
    m.translate_x(2)
    m.join(m2)
    m.save_stl("sample_out.stl", update_normals=True)


if __name__ == '__main__':
    main()
