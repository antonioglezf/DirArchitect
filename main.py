import os
import sys


def generate_file_tree(path, prefix=''):
    if not os.path.isdir(path):
        return

    files = os.listdir(path)

    for i, file in enumerate(files):
        current_path = os.path.join(path, file)

        if i == len(files) - 1:
            print(prefix + '└── ' + file)
            if os.path.isdir(current_path):
                generate_file_tree(current_path, prefix + '    ')
        else:
            print(prefix + '├── ' + file)
            if os.path.isdir(current_path):
                generate_file_tree(current_path, prefix + '│   ')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python file_tree_generator.py <directory_path>')
        sys.exit(1)

    directory_path = sys.argv[1]
    generate_file_tree(directory_path)
