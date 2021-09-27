from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np
import mpl_toolkits.mplot3d.axes3d as p3
import random
from itertools import product
from time_and_space.animation_2d import spiraling


def find_nearest_point(point, _dict, interval):
    for key in _dict:
        if np.abs(point - key) <= interval + 0.0001:
            return key
    raise ValueError('could not find nearest point')


def dot_shape(d):
    """
    :param d: dim (int)
    :return: 2d array
    """
    return np.zeros((1, d))


def two_dot_shape(d):
    """
    :param d: dim (int)
    :return: 2d array
    """
    arr = np.zeros(d)
    if d == 3:
        arr = np.array([[0, 0, 0], [1, 10, 0]])
    elif d == 2:
        arr = np.array([[0, 0], [10, 0]])
    return arr


def sphere(d):
    num = 10
    rs = np.linspace(1, 1, 1)
    thetas = np.linspace(0, 1 * np.pi, num, endpoint=False)
    phis = np.linspace(0, 2 * np.pi, num, endpoint=False)
    x, y, z = [], [], []
    for r in rs:
        for theta in thetas:
            for phi in phis:
                x.append(r * np.sin(theta) * np.cos(phi))
                y.append(r * np.sin(theta) * np.sin(phi))
                z.append(r * np.cos(theta))

    arr = np.zeros(3)
    if d == 2:
        arr = np.asarray([x, y])
    elif d == 3:
        arr = np.asarray([x, y, z])

    # figure
    if False:
        fig = plt.figure()
        ax = p3.Axes3D(fig)
        ax.plot(arr[0], arr[1], arr[2], '*')
        plt.show()

    return arr


def advance_one(i, point):
    return point + 1


def advance_random(i, point):
    return point + random.choice([-3, -4, 1, 5])


def time_advancing(_object, t_final, advance_object):
    """
    creating a dictionary {time: object}
    :param _object: list of points that form an object
    :param t_final: int
    :param advance_object: function
    :return: points: 2d nd.array (num_of_points*4)
    """
    num_of_dots = np.size(_object, 1)
    time_and_object = np.append(np.zeros((1, num_of_dots)), _object, axis=0)
    for i in range(1, t_final):
        _object = advance_object(i, _object)
        time_and_object = np.append(time_and_object,
                                    np.append(np.zeros((1, num_of_dots)) + i, _object, axis=0), axis=1)

    return time_and_object


def organize_points(points, d, n, new_time_row=1):
    """
    reorganize animation by swapping between the time axes and another axes
    :param points: dict {time: object}
    :param new_time_row: int (1, 2 or 3)
    :return: organized_points: dict {time: object}
    """

    # variables
    near = True if new_time_row != 0 else False
    near_factor = 3
    axes = [j for j in range(d + 1) if j != new_time_row]

    # building dictionary {new_t: new_coordinates}
    if near:
        max_new_time = points[new_time_row, :].max()
        min_new_time = points[new_time_row, :].min()
        organized_points = {new_t: [] for new_t in np.linspace(min_new_time, max_new_time, n * near_factor)}
        interval = (max_new_time - min_new_time) / (n * near_factor - 1) / 2
    else:
        organized_points = {new_t: [] for new_t in points[new_time_row, :]}

    # putting new coordinates in the new time
    for i in range(np.size(points, 1)):
        new_t = points[new_time_row][i]
        if near:
            new_t = find_nearest_point(new_t, organized_points, interval)
        else:
            new_t = points[new_time_row][i]
        coordinates = tuple([points[j][i] for j in axes])
        organized_points[new_t].append(coordinates)

    # organize points to np arrays for easy plotting
    for key, value in organized_points.items():
        organized_points[key] = np.array(value).T

    return organized_points


def update(num, data, time_line, line, d):
    # low = num - l if num - l > 0 else 0
    t = time_line[num]
    line.set_data(data[t][:2, :])
    if d == 3:
        line.set_3d_properties(data[t][2, :])


def circle(d):
    if d != 2:
        raise ValueError('dim should be equal 2 when using circle shape')
    return advance_circle_outside(0)


def advance_circle_outside(num, points=None):
    print (num)
    num_points = 30
    num_radii = 10
    max_radius = 16
    interval = 1
    rs = np.linspace(num * interval, (num_radii + num - 1) * interval, num_radii)
    rs = np.mod(rs, max_radius * interval)
    phis = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
    x, y = [], []
    for r in rs:
        for phi in phis:
            x.append(r * np.cos(phi))
            y.append(r * np.sin(phi))

    arr = np.asarray([x, y])
    return arr


def grid(d):
    if d != 2:
        raise ValueError('dim should be equal 2 when using circle shape')
    return advance_grid_sideways(0)


def advance_grid_sideways(num, points=None):
    num_points = 10
    num_lines = 10
    interval = 3.0
    int_factor = interval / num_points
    factor = 1
    y = np.array(range(-num_lines, num_lines + 1)) * interval
    x = [0]
    for i in range(num_points * 2):
        space = convert_num(i, num, num_points * 2)
        int_tmp = int_factor * (num_points - space)
        x.append(x[-1] + int_tmp)
    x = (np.array(x) - max(x) / 2) * factor
    y = [0]
    for i in range(num_points * 2):
        space = convert_num(i, num, num_points * 2)
        int_tmp = int_factor * (num_points - space)
        y.append(y[-1] + int_tmp)
    y = (np.array(y) - max(y) / 2) * factor
    arr = np.array(zip(*(product(x, y))))

    return arr


def convert_num(num, center, tot_spaces):
    space_from_center = num - center
    zero_to_tot_space = np.mod(space_from_center, tot_spaces)
    if zero_to_tot_space >= tot_spaces / 2:
        zero_to_half_spaces = tot_spaces - zero_to_tot_space - 1
    else:
        zero_to_half_spaces = zero_to_tot_space

    return zero_to_half_spaces


def spiral():
    pass


def advance_spiral_outside():
    pass


def triangle(d):
    if d != 2:
        raise ValueError('dim should be equal 2 when using triangle shape')
    return advance_triangle_sideways(0)


def advance_triangle_sideways(num, points=None):
    dot_in_base = 11  # only 1 side
    x_interval = 1
    y_interval = x_interval * 0.5
    x = []
    y = []

    # build pyramid, positive y
    for i in range(dot_in_base):
        tmp_y = []
        for j in range(dot_in_base - i):
            tmp_y.append(j * y_interval)
        y += tmp_y + tmp_y
        tmp_x = (np.mod(num + i, dot_in_base)) * x_interval
        x += [-tmp_x] * (dot_in_base - i) + [tmp_x] * (dot_in_base - i)

    return np.asarray([x, y])


def main():

    # variables
    num_of_frames = 13
    dim = 2
    new_time_axis = 'time'
    mp4_file_name = "circle.mp4"

    # choose animation
    shape_choice = spiral
    animation_function = advance_spiral_outside

    lim_plot = 20
    if new_time_axis == 'time':
        new_time_axis = 0
    elif new_time_axis == 'x':
        new_time_axis = 1
    elif new_time_axis == 'y':
        new_time_axis = 2

    if shape_choice == spiral:
        spiraling()
        return

    # creating point and mixing them
    initial_shape = shape_choice(dim)
    points = time_advancing(initial_shape, num_of_frames, animation_function)
    organized_points = organize_points(points, dim, num_of_frames, new_time_axis)
    time_line = sorted(organized_points)

    # plot animation
    fig = plt.figure()
    if dim == 2:
        ax = plt.subplot()
    elif dim == 3:
        ax = p3.Axes3D(fig)
    initial_data = organized_points[time_line[0]]
    if dim == 3:
        plot_line, = ax.plot(initial_data[0], initial_data[1], initial_data[2], '.')
    elif dim == 2:
        plot_line, = ax.plot(initial_data[0], initial_data[1], '.', markersize=4)

    if dim == 3:
        ax.set_xlim3d([-lim_plot, lim_plot])
        ax.set_ylim3d([-lim_plot, lim_plot])
        ax.set_zlim3d([-lim_plot, lim_plot])
    elif dim == 2:
        ax.set_xlim([-1, 14])
        ax.set_ylim([-lim_plot, lim_plot])

    # Set up formatting for the movie files
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=1)

    ani = animation.FuncAnimation(fig, update, num_of_frames, fargs=(organized_points, time_line, plot_line, dim),
                                  interval=1000, blit=False)

    ani.save(mp4_file_name, writer=writer)
    plt.show()


if __name__ == '__main__':
    main()
