#!/usr/bin/python
import argparse
import os
import subprocess
import sys

class Repository(object):
    class Type:
        git = 1
        svn = 1

    def __init__(self, name, paths, type):
        self._name = name
        self._type = type
        self._paths = paths
        self._files = []
        self._includes = []

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @property
    def paths(self):
        return self._paths

    @property
    def files(self):
        return self._files

    @property
    def includes(self):
        return self._includes

    @staticmethod
    def create(name, paths, type=None):
        if type is None:
            type = Repository.Type.git

        if type is Repository.Type.git:
            return GitRepository(name, paths, type)

class GitRepository(Repository):
    def __init__(self, name, paths, type):
        Repository.__init__(self, name, paths, type)
        self._gather_files()

    def _gather_files(self):
        for path in self.paths:
            os.chdir(path)
            find_cmd = subprocess.Popen('find', stdout=subprocess.PIPE)
            files = subprocess.check_output(['grep','-E', '(cc|cpp|mm|h|idl|gn|gni|gyp|gypi|py|java|js|json|grd|tmpl|S|y|sh|in)$'], stdin=find_cmd.stdout).splitlines()
            files = [os.path.abspath(file_path) for file_path in files]
            self._files = self._files + files
            self._includes = self._includes + [x[0] for x in os.walk(path)]
        self._files.sort()
        self._includes.sort();

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', '-r', action='store', required=True, help='Repository name.')
    parser.add_argument('--repo-paths', '-rp', action='append', required=True, help='Repository path(s).')
    parser.add_argument('--output-dir', '-o', action='store', required=True, help='Output directory to store the generated QtCreator project files.')
    parser.add_argument('--include-pattern', '-p', action='store', help='Regular expression consisting of the file inclusion pattern.')
    args = parser.parse_args()
    repo = Repository.create(args.repo, args.repo_paths)

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
