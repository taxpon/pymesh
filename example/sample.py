import env
from pymesh import stl
from pymesh import obj


def main():
    m = stl.Stl('test2.stl')
    # m.scale(1, 2, 1)
    # m.rotate_x(90)
    # m.rotate_y(30)
    # m.save('sample_out.stl')
    # m = obj.Obj("sample.obj")
    # m.scale(10, 10, 10)
    # m.rotate_x(90)
    # m.rotate_y(30)
    print(m.get_volume())
    m.save_stl("hoge.stl")
    # m.save_obj("hoge.obj")


if __name__ == '__main__':
    main()
