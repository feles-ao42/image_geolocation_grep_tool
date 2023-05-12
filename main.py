import subprocess as sp
import sys

input_path = ""
output_path = ""

x, y = 0, 0
x_dash, y_dash = 0, 0


def make_ls_list():
    global input_path
    ls_cmd = "ls %s" % input_path
    proc = sp.Popen(ls_cmd, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    std_out, std_err = proc.communicate()
    ls_file_name = std_out.decode('utf-8').rstrip().split('\n')
    print(ls_cmd)
    return ls_file_name


def get_latitude(file_name):
    photo_path = input_path + file_name
    latitude_cmd = "exiftool -b -GPSLatitude %s" % photo_path
    proc = sp.Popen(latitude_cmd, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    std_out, std_err = proc.communicate()
    latitude = std_out.decode('utf-8').rstrip()
    print(file_name, latitude)
    return float(latitude)


def get_longitude(file_name):
    photo_path = input_path + file_name
    longitude_cmd = "exiftool -b -GPSLongitude %s" % photo_path
    proc = sp.Popen(longitude_cmd, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    std_out, std_err = proc.communicate()
    longitude = std_out.decode('utf-8').rstrip()
    return float(longitude)


def get_take_place(ls_file_name):
    take_place_list = []
    for file_name in ls_file_name:
        latitude = get_latitude(file_name)
        longitude = get_longitude(file_name)
        take_place_list.append([file_name, latitude, longitude])
    return take_place_list


def check_range(take_place_list):
    fit_list = []
    for take_place in take_place_list:
        if x <= take_place[1] <= x_dash and y <= take_place[2] <= y_dash:
            fit_list.append(take_place)
    return fit_list


def copy_file(fit_list):
    global output_path
    print("copy start")
    for fit_file in fit_list:
        photo_path = input_path + fit_file[0]
        copy_cmd = "cp %s %s" % (photo_path, output_path)
        print("copy_cmd")
        proc = sp.Popen(copy_cmd, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
        std_out, std_err = proc.communicate()
        print(std_out.decode('utf-8').rstrip())


def get_args():
    global x, y, x_dash, y_dash, input_path, output_path
    args = sys.argv
    if len(args) == 3:
        subject_type = args[1]
        magnification = args[2]
        if subject_type == "mori":
            # mori-----------------------------------
            x, y = 35.388829, 139.426260
            x_dash, y_dash = 35.390185, 139.426952
        elif subject_type == "buildings":
            # buildings-----------------------------
            x, y = 35.388526, 139.426533
            x_dash, y_dash = 35.388904, 139.427196
        input_path = "./images/%s/" % magnification
        output_path = "./fit/%s/%s" % (subject_type, magnification)
    else:
        print("Usage: python3 main.py [type] [magnification]")


def main():
    get_args()
    ls_file_name = make_ls_list()
    take_place_list = get_take_place(ls_file_name)
    fit_list = check_range(take_place_list)
    copy_file(fit_list)


if __name__ == '__main__':
    main()
