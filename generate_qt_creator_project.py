#!/usr/bin/python
import argparse
import os
import subprocess
import sys

class Repository(object):
    def __init__(self, args):
        self._name = args.repository_name
        self._paths = args.include_path
        self._files = []
        self._include_paths = []
        self._exclude_paths = ['.git', '.svn']
        if args.exclude_path != None:
            self._exclude_paths = self._exclude_paths + [os.path.abspath(file_path) for file_path in args.exclude_path]

        self._gather_files()

    @property
    def name(self):
        return self._name

    @property
    def files(self):
        return self._files

    @property
    def includes(self):
        return self._include_paths

    def _gather_files(self):
        for path in self._paths:
            os.chdir(path)
            found_files = subprocess.check_output(['find', os.getcwd()]).splitlines()
            for file in found_files:
                should_exclude_file = False
                for exclude_path in self._exclude_paths:
                    if exclude_path in file:
                        should_exclude_file = True
                        break
                if should_exclude_file:
                    continue
                self._files.append(file)
            self._include_paths = self._include_paths + [x[0] for x in os.walk(path)]
        self._files.sort()
        self._include_paths.sort();

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repository-name', '-r', action='store', required=True, help='Repository name.')
    parser.add_argument('--include-path', '-i', action='append', required=True, help='Repository path(s) to be included.')
    parser.add_argument('--exclude-path', '-x', action='append', help='Repository path(s) to be excluded.')
    parser.add_argument('--output-dir', '-o', action='store', required=True, help='Output directory to store the generated QtCreator project files.')
    args = parser.parse_args()
    repo = Repository(args)

    file_prefix = os.path.abspath(args.output_dir + '/' + repo.name.upper())
    config_file = open(file_prefix + '.config', 'w');
    config_file.write('''\
// Add predefined macros for your project here. For example:
// #define THE_ANSWER 42
''')
    config_file.close()

    includes_file = open(file_prefix + '.includes', 'w')
    includes_file.write('\n'.join(repo.includes))
    includes_file.close()

    files_file = open(file_prefix + '.files', 'w')
    files_file.write('\n'.join(repo.files))
    files_file.close()

    creator_file = open(file_prefix + '.creator', 'w')
    creator_file.write('[General]')

if __name__ == '__main__':
    sys.exit(main())
