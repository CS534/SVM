from glob import glob
import os


def path_getter(path, file_name):
    """ Return a file with the format of label and path """
    dirs = os.path.join(path, "*")
    dirs = glob(dirs)
    paths = [glob("{}/*.jpg".format(dir)) for dir in dirs]
    x, y = [], []
    for directory in paths:
        for path in directory:
            path = '/'.join(path.split('\\'))
            print(path)
            x.append(path)
            y.append(os.path.dirname(path).split('/')[-1].split('.')[0])
    with open(os.path.dirname(dirs[0]) + '/' + file_name, 'w')as f:
        for i in range(len(x)):
            f.write("{} {}\n".format(x[i], y[i]))
    return x, y


if __name__ == '__main__':
    path_getter('./images/train', 'train.txt')
    path_getter('./images/test', 'test.txt')
