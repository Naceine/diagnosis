"""Handy utility classes.

   @author
     Victor I. Afolabi
     Artificial Intelligence & Software Engineer.
     Email: javafolabi@gmail.com
     GitHub: https://github.com/victor-iyiola

   @project
     File: utils.pyx
     Created on 2nd June, 2019 @ 12:23 PM.

   @license
     BSD-3 Clause license.
     Copyright (c) 2019. Victor I. Afolabi. All rights reserved.
"""

# Built-in libraries.
import os
import sys
import stat
import pickle
import logging
import tarfile
import zipfile
import urllib.error
import urllib.parse
import urllib.request

from abc import ABCMeta
from enum import IntEnum
from pprint import PrettyPrinter
from logging.config import fileConfig
from typing import Iterable, Callable

# Third-party library.
import numpy as np

# Custom libraries.
from config import consts

# Exported classes and functions.
__all__ = [
    'Downloader', 'Cache', 'File', 'Log',
]


################################################################################################
# +--------------------------------------------------------------------------------------------+
# | Downloader: For fetching resources from the internet & extracting compressed files.
# +--------------------------------------------------------------------------------------------+
################################################################################################
class Downloader(metaclass=ABCMeta):
    @staticmethod
    def get_source(str url, dict query_dict=None):
        """Retrieve the source code of a given URL.

        Args:
            url (str): Target URL.
            query_dict (Dict[str, str]): Key value pair to be constructed
                for query string.

        Returns:
            str: Decoded source code of the give URL.
        """
        cdef str response = None, data = None
        cdef dict headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3)'
                          ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                          '50.0.2661.102 Safari/537.36'
        }

        try:
            if query_dict is not None:
                data = urllib.parse.urlencode(query_dict)
                data = data.encode('utf-8')

            # Request webpage with query-strings & headers.
            req = urllib.request.Request(url, data=data, headers=headers)
            request = urllib.request.urlopen(req)
            response = request.read().decode()

        except urllib.error.HTTPError as http_err:
            Log.exception(f'HTTPError: {http_err}')
        except urllib.error.URLError as url_err:
            Log.exception(f'URLError: {url_err}')

        return response

    @staticmethod
    def maybe_download(str url, str download_dir=None, bint extract=False, bint overwrite=False):
        """Download and extract the data if it doesn't already exist.

        Notes:
            Assumes the url is a zip or tar-ball file.

        Arguments:
            url {str} -- Internet URL for the tar-file to download.
                e.g: "http://nlp.stanford.edu/data/glove.6B.zip"

            download_dir {str} -- Directory to download files.
                e.g: "datasets/GloVe/" (default {'downloads'})

            extract {bool} -- If set to `True` compressed files are extracted automatically.
                (default {False})

            overwrite {bool} -- Force download even if the file already exists.
                (default {False})

        Returns:
            str: Filename if `extract==False`, otherwise `extract_dir` is returned.
        """

        # Filename for saving the file downloaded from the internet.
        # Use the filename from the URL and add it to the download_dir.
        download_dir = download_dir or "downloads/"
        cdef str filename = File.join(download_dir, File.basename(url))

        # Check if the file already exists.
        # If it exists then we assume it has also been extracted,
        # otherwise we need to download and extract it now.
        if not File.exists(filename) or overwrite:
            # Check if the download directory exists, otherwise create it.
            File.make_dirs(download_dir)

            # Download the file from the internet.
            filename, _ = urllib.request.urlretrieve(
                url=url, filename=filename,
                reporthook=Log.report_hook
            )

            Log.info("\nDownload finished.")

            return (Downloader.maybe_extract(file=filename,
                                             extract_dir=download_dir,
                                             overwrite=overwrite) if extract
                    else filename)

        Log.info("Data has apparently already been downloaded and unpacked.")
        return filename

    @staticmethod
    def maybe_extract(str file, str extract_dir=None, bint overwrite=False):
        # Ensure the file exists.
        if not File.is_file(file):
            raise FileNotFoundError('"{}" not found!'.format(file))

        # Retrieve extracted directory.
        extract_dir = extract_dir or File.dirname(file)
        extract_dir = File.join(extract_dir, File.basename(file))

        # Don't extract if it's already been extracted.
        if File.is_dir(extract_dir) and not overwrite:
            Log.warn('Already extracted to "{}"'.format(extract_dir))
            return extract_dir

        # Create extract directory if it doesn't exist.
        File.make_dirs(extract_dir)

        # Read mode.
        cdef str mode = "r"

        if zipfile.is_zipfile(file):
            Extractor = zipfile.ZipFile
        elif tarfile.is_tarfile(file):
            # Change to tarball extractor.
            Extractor = tarfile.open

            # Update mode for a gzipped file.
            if file.endswith('gz'):
                mode = "r:gz"
        else:
            # Unrecognized compressed file.
            raise ValueError('{} must a zipped or tarball file'.format(file))

        with Extractor(file, mode=mode) as ex:
            ex.extractall(extract_dir)

        # Display & return extracted directory.
        Log.info('Successfully extracted to {}'.format(extract_dir))
        return extract_dir


################################################################################################
# +--------------------------------------------------------------------------------------------+
# | File: File utility class for working with directories & files.
# +--------------------------------------------------------------------------------------------+
################################################################################################
class File(metaclass=ABCMeta):
    @staticmethod
    def make_dirs(str path, int verbose=0):
        """Create Directory if it doesn't exist.

        Args:
            path (str): Directory/directories to be created.
            verbose (bool, optional): Defaults to 0. 0 turns of logging,
                while 1 gives feedback on creation of director(y|ies).

        Example:
            ```python
            >>> path = File.join("path/to", "be/created/")
            >>> File.make_dirs(path, verbose=1)
            INFO  |  "path/to/be/created/" has been created.
            ```
        """

        # if director(y|ies) doesn't already exist.
        if not File.is_dir(path):
            # Create director(y|ies).
            os.makedirs(path)

            if verbose:
                # Feedback based on verbosity.
                Log.info('"{}" has been created.'.format(path))

    @staticmethod
    def remove(str path, int verbose=0):
        """Remove directories & files if it already exist.

        Args:
            path (str): Directory/file to be removed.
            verbose (bool, optional): Defaults to 0. 0 turns of logging,
                while 1 gives feedback on creation of director(y|ies).

        Example:
            ```python
            >>> # Removing directories.
            >>> path = File.join("path/to", "be/removed")
            >>> File.remove(path, verbose=1)
            INFO  |  "path/to/be/removed/" has been removed.
            >>> # Removing a file.
            >>> path = File.join("path/to", "be/removed/file.ext")
            >>> File.remove(path, verbose=1)
            WARNING |  Removing directories & it's content(s).
            INFO    |  "path/to/be/removed/file.ext" has been removed.
            ```
        """

        # if director(y|ies) doesn't already exist.
        if File.is_dir(path):
            # Recursively delete directory & it's children.
            import shutil
            Log.warn('Removing directories & it\'s content(s).')
            shutil.rmtree(path)
        else:
            # Remove file.
            os.remove(path)

        if verbose:
            # Feedback based on verbosity.
            Log.info('"{}" has been created.'.format(path))

    @staticmethod
    def get_dirs(str path, exclude: Iterable[str] = None, bint optimize = False):
        """Retrieve all directories in a given path.

        Args:
            path (str): Base directory of directories to retrieve.
            exclude (Iterable[str], optional): Defaults to None. List of paths to
                remove from results.
            optimize (bool, optional): Defaults to False. Return an generator object,
                to prevent loading all directories in memory, otherwise: return results
                as a normal list.

        Raises:
            FileNotFoundError: `path` was not found.

        Returns:
            Union[Generator[str], List[str]]: Generator expression if optimization is turned on,
                otherwise list of directories in given path.
        """
        # Return only list of directories.
        return File.listdir(path, exclude=exclude, dirs_only=True, optimize=optimize)

    @staticmethod
    def get_files(str path, exclude: Iterable[str] = None, bint optimize = False):
        """Retrieve all files in a given path.

        Args:
            path (str): Base directory of files to retrieve.
            exclude (Iterable[str], optional): Defaults to None. List of paths to
                remove from results.
            optimize (bool, optional): Defaults to False. Return an generator object,
                to prevent loading all directories in memory, otherwise: return results
                as a normal list.

        Raises:
            FileNotFoundError: `path` was not found.

        Returns:
            Union[Generator[str], List[str]]: Generator expression if optimization is turned on,
                otherwise list of files in given path.
        """
        # Return only list of directories.
        return File.listdir(path, exclude=exclude, files_only=True, optimize=optimize)

    @staticmethod
    def listdir(str path, exclude: Iterable[str] = None,
                bint dirs_only=False, bint files_only=False,
                bint optimize=False):
        """Retrieve files/directories in a given path.

        Args:
            path (str): Base directory of path to retrieve.
            exclude (Iterable[str], optional): Defaults to None. List of paths to
                remove from results.
            dirs_only (bool, optional): Defaults to False. Return only directories in `path`.
            files_only (bool, optional): Defaults to False. Return only files in `path`.
            optimize (bool, optional): Defaults to False. Return an generator object,
                to prevent loading all directories in memory, otherwise: return results
                as a normal list.

        Raises:
            FileNotFoundError: `path` was not found.

        Returns:
            Union[Generator[str], List[str]]: Generator expression if optimization is turned on,
                otherwise list of directories in given path.
        """
        if not File.is_dir(path):
            raise FileNotFoundError('"{}" was not found!'.format(path))

        # Get all files in `path`.
        if files_only:
            paths = (File.join(path, p) for p in os.listdir(path)
                     if File.is_file(File.join(path, p)))
        else:
            # Get all directories in `path`.
            if dirs_only:
                paths = (File.join(path, p) for p in os.listdir(path)
                         if File.is_dir(File.join(path, p)))
            else:
                # Get both files and directories.
                paths = (File.join(path, p) for p in os.listdir(path))

        # Exclude paths from results.
        if exclude is not None:
            # Remove excluded paths.
            paths = filter(lambda p: File.basename(p) not in exclude, paths)

        # Convert generator expression to list.
        if not optimize:
            paths = list(paths)

        return paths

    @staticmethod
    def join(str path, *paths: Iterable[str]):
        """Join two or more paths together.

        Args:
            path (Union[str, bytes]): Base path. Starting point.
            *paths (Iterable[Union[str, bytes]]): List of paths to be joined to `path`.

        Returns:
            Union[bytes, str]: Joined path.
        """
        return os.path.join(path, *paths)

    @staticmethod
    def exists(str path):
        """Test whether a path exists.

        Args:
            path (str): Path to test.

        Returns:
            bool - Returns False for broken symbolic links, True if path exists.
        """
        try:
            os.stat(path)
        except OSError:
            return False
        return True

    @staticmethod
    def is_file(str path):
        """Test whether a path is a regular file.

        Args:
            path (str): Path to test.

        Returns:
            bool - Return true if the pathname refers
                to an existing regular file.
        """
        try:
            st = os.stat(path)
        except OSError:
            return False
        return stat.S_ISREG(st.st_mode)

    @staticmethod
    def is_dir(str path):
        """Test whether a path is an existing directory.

        Args:
            path (str): Path to test.

        Returns:
            bool - Return true if the pathname refers
                to an existing directory.
        """
        try:
            st = os.stat(path)
        except OSError:
            return False
        return stat.S_ISDIR(st.st_mode)

    @staticmethod
    def rel_path(str path, str start=None):
        """Return a relative version of a path.

        Args:
            path (str): An absolute path.
            start (str): Where to start relativity.
                Uses current dir if not given.

        Returns:
            str - Relative path from `start`.
        """
        return os.path.relpath(path, start)

    @staticmethod
    def abs_path(str path):
        """Return the absolute version of a path.

        Args:
            path (str): Path.

        Returns:
            str - Empty path must return current working directory.
                Bad path returns unchanged.
        """
        return os.path.abspath(path)

    @staticmethod
    def basename(str path):
        """Returns the final component of a pathname.

        Args:
            path (str): Path name.

        Returns:
            AnyStr - Base name of the given path.
        """
        return os.path.split(path)[1]

    @staticmethod
    def filename(str path):
        """Returns the final component of a pathname without extension.

        Args:
            path (str): Path name.

        Returns:
            AnyStr - File name of the given path without extension.
        """
        return os.path.splitext(File.basename(path))[0]

    @staticmethod
    def dirname(str path):
        """Returns the directory component of a pathname.

        Args:
            path (AnyStr): Path name.

        Returns:
            AnyStr - Directory of a given file.
        """
        return os.path.split(path)[0]

    @staticmethod
    def ext(str path):
        """Returns extension of a give path.

        Args:
            path (AnyStr): Path name.

        Examples:
            ```python
            >>> # For files.
            >>> path = 'path/to/file.ext'
            >>> ext = File.ext(path)
            >>> assert(ext, 'ext')
            >>> # For directories.
            >>> path = 'path/to/directory'
            >>> ext = File.ext(path)
            >>> assert(ext, '')
            ''
            ```

        Returns:
            AnyStr - Extension of path.
        """
        return os.path.splitext(path)[-1].lstrip('.')


################################################################################################
# +--------------------------------------------------------------------------------------------+
# | Log: For logging and printing download progress, etc...
# +--------------------------------------------------------------------------------------------+
################################################################################################
class Log(metaclass=ABCMeta):
    # File logger configuration.
    fileConfig(consts.LOGGER.ROOT)
    _logger = logging.getLogger()

    # Log Levels.
    Level = IntEnum('Level', names={
        'CRITICAL': 50,
        'ERROR': 40,
        'WARNING': 30,
        'INFO': 20,
        'DEBUG': 10,
        'NOTSET': 0,
    })

    # Log Level.
    level = _logger.level

    @staticmethod
    def setLevel(level: int):
        Log._logger.setLevel(level=level)

    @staticmethod
    def getLogger():
        return Log._logger

    @staticmethod
    def debug(*args, **kwargs):
        Log._logger.debug(*args, **kwargs)

    @staticmethod
    def info(*args, **kwargs):
        Log._logger.info(*args, **kwargs)

    @staticmethod
    def warn(*args, **kwargs):
        Log._logger.warning(*args, **kwargs)

    @staticmethod
    def error(*args, **kwargs):
        Log._logger.error(*args, **kwargs)

    @staticmethod
    def critical(*args, **kwargs):
        Log._logger.critical(*args, **kwargs)

    @staticmethod
    def exception(*args, **kwargs):
        Log._logger.exception(*args, **kwargs)

    @staticmethod
    def fatal(*args, int code=-1, **kwargs):
        Log._logger.fatal(*args, **kwargs)
        exit(code)

    @staticmethod
    def log(*args, **kwargs):
        """Logging method avatar based on verbosity.

        Args:
            *args (Any): List of arguments to be printed.

        Keyword Args:
            verbose (int, optional): Defaults to 1. Verbosity level.

        Returns:
            None
        """

        # No logging if verbose is not 'on'.
        if not kwargs.pop('verbose', 1):
            return

        Log._logger.log(Log.level, *args, **kwargs)

    @staticmethod
    def pretty(args, stream=None, size_t indent=1, size_t width=80, size_t depth=0, *, bint compact=False):
        """Handle pretty printing operations onto a stream using a set of configured parameters.

        Args:
            args (Any): Structured arguments to be printed.
            stream (BinaryIO[bytes], optional): Defaults to `sys.stdout`. The
                desired output stream. Stream must be writable. If omitted (or false),
                the standard output stream available at construction will be used.
            indent (int, optional): Defaults to 1. Number of spaces to indent
                for each level of nesting.
            width (int, optional): Defaults to 80. Attempted maximum number of
                columns in the output.
            depth (int, optional): Defaults to None. The maximum depth to print
                out nested structures.
            compact (bool, optional): Defaults to False. If true, several items
                will be combined in one line.
        """
        printer = PrettyPrinter(stream=sys.stdout, indent=indent,
                                width=width, depth=None if depth == 0 else depth, compact=compact)
        printer.pprint(args)

    @staticmethod
    def progress(int count, int max_count):
        """Prints task progress *(in %)*.

        Args:
            count {int}: Current progress so far.
            max_count {int}: Total progress length.
        """

        # Percentage completion.
        cdef float pct_complete = count / max_count

        # Status-message. Note the \r which means the line should
        # overwrite itself.
        cdef str msg = "\r- Progress: {0:.02%}".format(pct_complete)

        # Print it.
        sys.stdout.write(msg)
        sys.stdout.flush()

    @staticmethod
    def report_hook(int block_no, bytes read_size, bytes file_size):
        """Calculates download progress of downloaded files.

        Args:
            block_no {int}: Current download state.
            read_size {bytes}: Current downloaded size.
            file_size {bytes}: Total file size.

        Returns:
            None.
        """
        # Calculates download progress given the block number, a read size,
        #  and the total file size of the URL target.
        cdef float pct_complete = float(block_no * read_size) / float(file_size)

        cdef str msg = "\r\t -Download progress {:.02%}".format(pct_complete)
        sys.stdout.stdwrite(msg)
        sys.stdout.flush()


################################################################################################
# +--------------------------------------------------------------------------------------------+
# | Cache: For saving objects and converting numpy objects to pickle.
# +--------------------------------------------------------------------------------------------+
################################################################################################
class Cache(metaclass=ABCMeta):
    @staticmethod
    def cache(str cache_path, fn: Callable, bint use_numpy=False, int verbose=1, *args, **kwargs):
        """Cache-wrapper for a function or class.

        Notes:
            If the cache-file exists then the data is reloaded and
            returned, otherwise the function is called and the result
            is saved to cache. The fn-argument can also be a class
            instead, in which case an object-instance is created and
            saved to the cache-file.

        Args:
            cache_path (str): File-path for the cache-file.
            fn (Callable): Function or class to be called.
            use_numpy (bool, optional): Defaults to False. Save object as
                a numpy object.
            verbose (int, optional): Defaults to 1. Verbosity level.
            args (Any): Arguments to the function or class-init.
            kwargs(Dict[str, Any]): Keyword arguments to the function
                or class-init.

        Raises:
            TypeError: Expected a NumPy object, got `type(obj)`.

        See Also:
            `Cache.cache_numpy(...)`

        Returns:
            Any: The result of calling the function or creating the object-instance.
        """

        # If the cache-file exists.
        if File.exists(cache_path):
            if use_numpy:
                obj = np.load(cache_path)
            else:
                # Load the cached data from the file.
                with open(cache_path, mode='rb') as file:
                    obj = pickle.load(file)

            if verbose:
                Log.info(f"- Data loaded from cache-file: {File.rel_path(cache_path)}")
        else:
            # The cache-file does not exist.

            # Call the function / class-init with the supplied arguments.
            obj = fn(*args, **kwargs)

            # Create cache-directory if it doesn't exist.
            File.make_dirs(File.dirname(cache_path))

            # Save the data to a cache-file.
            if use_numpy:
                if isinstance(obj, np.ndarray):
                    np.save(cache_path, obj)
                else:
                    raise TypeError(f"Expected a NumPy object, got {type(obj)}")
            else:
                with open(cache_path, mode='wb') as file:
                    pickle.dump(obj, file)

            if verbose:
                Log.info(f"- Data saved to cache-file: {File.rel_path(cache_path)}")

        return obj

    @staticmethod
    def cache_numpy(str cache_path, fn: Callable, int verbose=1, *args, **kwargs):
        """Cache-wrapper for a function or class.

        Notes:
            If the cache-file exists then the data is reloaded and
            returned, otherwise the function is called and the result
            is saved to cache. The fn-argument can also be a class
            instead, in which case an object-instance is created and
            saved to the cache-file.

        Args:
            cache_path (str): File-path for the cache-file.
            fn (Callable): Function or class to be called.
            args (Any): Arguments to the function or class-init.
            verbose (int, optional): Defaults to 1. Verbosity level.
            kwargs(Dict[str, Any]): Keyword arguments to the function
                or class-init.

        Raises:
            TypeError: Expected a NumPy object, got `type(obj)`.

        See Also:
            `Cache.cache(...)`

        Returns:
            Any: The result of calling the function or creating the object-instance.
        """
        return Cache.cache_numpy(cache_path=cache_path, fn=fn, use_numpy=True,
                                 verbose=verbose, *args, **kwargs)

    @staticmethod
    def convert_numpy2pickle(str in_path, str out_path):
        """Convert a numpy-file to pickle-file.

        Notes:
            The first version of the cache-function used numpy for
            saving the data. Instead of re-calculating all the data,
            you can just convert the cache-file using this function.

        Args:
            in_path (str): Input file in numpy-format written using numpy.save().
            out_path (str): Output file written as a pickle-file.

        Returns:
            Nothing.
        """

        # Load the data using numpy.
        data = np.load(in_path)

        # Save the data using pickle.
        with open(out_path, mode='wb') as file:
            pickle.dump(data, file)
