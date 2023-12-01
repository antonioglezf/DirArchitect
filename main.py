import os
import sys


def parse_gitignore(gitignore_path):
    ignored_files = set()

    if os.path.isfile(gitignore_path):
        with open(gitignore_path, 'r') as gitignore_file:
            for line in gitignore_file:
                line = line.strip()
                if line and not line.startswith('#'):
                    ignored_files.add(line)

    return ignored_files


def is_ignored(path, gitignore_rules):
    for rule in gitignore_rules:
        if rule.startswith('/') and path.endswith(rule):
            return True
        elif not rule.startswith('/') and path.endswith('/' + rule):
            return True
    return False


def generate_file_tree(path, prefix='', output_file=None, gitignore_rules=None):
    if not os.path.isdir(path):
        return

    files = sorted(os.listdir(path))

    for i, file in enumerate(files):
        current_path = os.path.join(path, file)

        # Check if the file should be ignored based on gitignore rules
        if gitignore_rules and is_ignored(current_path, gitignore_rules):
            continue

        if file == '.git':
            continue

        if i == len(files) - 1:
            output = prefix + '└── ' + file
            print(output)
            if output_file:
                output_file.write(output + '\n')
            if os.path.isdir(current_path):
                generate_file_tree(current_path, prefix + '    ', output_file, gitignore_rules)
        else:
            output = prefix + '├── ' + file
            print(output)
            if output_file:
                output_file.write(output + '\n')
            if os.path.isdir(current_path):
                generate_file_tree(current_path, prefix + '│   ', output_file, gitignore_rules)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python file_tree_generator.py <directory_path>')
        sys.exit(1)

    directory_path = sys.argv[1]
    output_path = os.path.join(directory_path, 'file_tree.txt')

    gitignore_path = os.path.join(directory_path, '.gitignore')
    gitignore_rules = parse_gitignore(gitignore_path) if os.path.isfile(gitignore_path) else None

    with open(output_path, 'w') as output_file:
        generate_file_tree(directory_path, output_file=output_file, gitignore_rules=gitignore_rules)

    print(f'File tree saved to {output_path}')
