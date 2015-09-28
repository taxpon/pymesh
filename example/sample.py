import env
from pymesh import stl


def main():
    m = stl.Stl('sample_bin.stl')
    m.scale(1, 2, 1)
    m.rotate_x(90)
    m.rotate_y(30)
    m.save('sample_out.stl')


if __name__ == '__main__':
    main()
