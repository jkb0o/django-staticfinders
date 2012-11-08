import functools
import fnmatch

from django.conf import settings
from django.contrib.staticfiles import utils
from django.contrib.staticfiles.finders import FileSystemFinder, AppDirectoriesFinder

class BaseFilteredFinder(object):
    def matches(self, path):
        result = self._matches(path)
        return result

    def _matches(self, path):
        include = getattr(settings, 'STATICFILES_INCLUDE', [])
        exlude = getattr(settings, 'STATICFILES_EXCLUDE', [])
        check = functools.partial(fnmatch.fnmatch, path)
        return filter(check, include) and not filter(check, exlude)

class FilteredFileSystemFinder(FileSystemFinder, BaseFilteredFinder):
    """
    A static files finder that uses the ``STATICFILES_DIRS`` setting
    to locate files.
    """

    def find_location(self, root, path, *args, **kwargs):
        found_path = super(FilteredFileSystemFinder, self).find_location(root, path, *args, **kwargs)
        if found_path and self.matches(path):
            return found_path
        else:
            return None

    def list(self, ignore_patterns):
        """
        List all files in all locations.
        """
        for prefix, root in self.locations:
            storage = self.storages[root]
            for path in utils.get_files(storage, ignore_patterns):
                if self.matches(path):
                    yield path, storage


class FilteredAppDirectoriesFinder(AppDirectoriesFinder, BaseFilteredFinder):

    def list(self, ignore_patterns):
        """
        List all files in all app storages.
        """
        for storage in self.storages.itervalues():
            if storage.exists(''):  # check if storage location exists
                for path in utils.get_files(storage, ignore_patterns):
                    if self.matches(path):
                        yield path, storage

    def find_in_app(self, app, path):
        found_path = super(FilteredAppDirectoriesFinder, self).find_in_app(app, path)
        if self.matches(path):
            return found_path
        else:
            return None

