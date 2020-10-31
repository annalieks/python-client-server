import os
import re


class FSManager:
    def __init__(self):
        self.dir = '.'

    def process(self, search_type, pattern=None):
        if search_type == 'files':
            return self.get_files(pattern)
        elif search_type == 'dir':
            return self.get_dirs(pattern)
        elif search_type == 'content':
            result = self.get_files(pattern)
            result.extend(self.get_dirs(pattern))
            return result
        else:
            raise AttributeError()

    def get_files(self, pattern=None):
        return [file for file in os.listdir(self.dir) if os.path.isfile(file)
                and (re.search(pattern, file) if pattern else True)]

    def get_dirs(self, pattern=None):
        return [file for file in os.listdir(self.dir) if os.path.isdir(file)
                and (re.search(pattern, file) if pattern else True)]
