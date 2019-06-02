"""diagnosis.core.utils - Consist of utility class for the `diagnosis` API.

   @author
     Victor I. Afolabi
     Artificial Intelligence & Software Engineer.
     Email: javafolabi@gmail.com
     GitHub: https://github.com/victor-iyiola

   @project
     File: utils.pyi
     Created on 2nd June, 2019 @ 12:37 PM.

   @license
     Apache License 2.0
     Copyright (c) 2019. Victor I. Afolabi. All rights reserved.
"""

# Built-in libraries.
from enum import IntEnum
from abc import ABCMeta, abstractmethod
from typing import (List, Tuple, Iterable, Callable, Union, SupportsBytes,
                    TypeVar, Generic, SupportsFloat, SupportsInt, Dict,
                    Optional, Generator, Any, AnyStr, Type, BinaryIO)

# Third-party libraries.
import numpy as np
from logging import Logger

# Generic types.
I = TypeVar('I', SupportsInt, np.int_t)  # Int Types.
F = TypeVar('F', SupportsFloat, np.float_t)  # Float types.
T = TypeVar('T', int, float, complex, np.int_t, np.float_t)


class __ArrayLike(Generic[T], np.ndarray):
    shape = ...  # type: Tuple[int]


class __TensorLike(__ArrayLike):
    ...


class __HasLen(metaclass=ABCMeta):
    @abstractmethod
    def __len__(self) -> int: ...


# Type Aliases.
LT = TypeVar('LT', bound=__HasLen)  # Length type.
Array = TypeVar('Array', bound=__ArrayLike)  # Array type.
Tensor = TypeVar('Tensor', bound=__TensorLike)  # Tensor type.
URL = AnyStr

# Image & Caption Typing info.
Caption = Union[str, List[str], List[List[str]]]
CaptionInt = Union[int, List[int], List[List[int]]]
AnyCaption = TypeVar('AnyCaption', Caption, CaptionInt)


################################################################################################
# +--------------------------------------------------------------------------------------------+
# | Downloader: For fetching resources from the internet & extracting compressed files.
# +--------------------------------------------------------------------------------------------+
################################################################################################
class Downloader(metaclass=ABCMeta):
    """Downloader: For fetching resources from the internet & extracting compressed files.

    Methods:
        @staticmethod
        def get_source(url: str, query_dict: dict = ...):
            Retrieve the source code of a given URL.

        @staticmethod
        def maybe_download(url: str, download_dir: Optional[str] = None,
                           extract: Optional[bool] = False,
                           overwrite: Optional[bool] = False) -> str:
            Download and extract the data if it doesn't already exist.

        @staticmethod
        def maybe_extract(file: str, extract_dir: Optional[str] = None,
                          overwrite: Optional[bool] = False) -> str:
            Extracts downloaded files if it hasn't already been extracted.
    """

    @staticmethod
    def get_source(url: URL, query_dict: Dict[str, str] = ...):
        """Retrieve the source code of a given URL.

    Args:
        url (URL): Target URL.
        query_dict (Dict[str, str]): Key value pair to be constructed
            for query string.

    Returns:
        str: Decoded source code of the give URL.
    """

    @staticmethod
    def maybe_download(url: URL, download_dir: Optional[str] = None,
                       extract: Optional[bool] = False,
                       overwrite: Optional[bool] = False) -> str:
        """Download and extract the data if it doesn't already exist.

        Notes:
            Assumes the url is a zip or tar-ball file.

        Arguments:
            url (URL) -- Internet URL for the tar-file to download.
                e.g: "http://nlp.stanford.edu/data/glove.6B.zip"

            download_dir (str, optional) -- Directory to download files.
                e.g: "datasets/GloVe/" (default {'downloads'})

            extract (bool, optional) -- If set to `True` compressed files are extracted automatically.
                (default {False})

            overwrite (bool, optional) -- Force download even if the file already exists.
                (default {False})

        Returns:
            str: Filename if `extract==False`, otherwise `extract_dir` is returned.
        """

    @staticmethod
    def maybe_extract(file: AnyStr, extract_dir: Optional[str] = None,
                      overwrite: Optional[bool] = False) -> str:
        """Extracts downloaded files if it hasn't already been extracted.

        Args:
            file (AnyStr): Path to a compressed file.
            extract_dir (str, optional): Defaults to None. Inferred from `file`.
            overwrite (bool, optional): Defaults to False.

        Returns:
            str - Path where file was extracted.
        """


################################################################################################
# +--------------------------------------------------------------------------------------------+
# | File: File utility class for working with directories & files.
# +--------------------------------------------------------------------------------------------+
################################################################################################
class File(metaclass=ABCMeta):
    """File Utility class for working with directories & files.

    Methods:
        @staticmethod
        def make_dirs(path: str, verbose: Optional[int] = 0) -> None:
            Create Directory if it doesn't exist.

        @staticmethod
        def get_dirs(path: str, exclude: Optional[Iterable[str]] = None,
                     optimize: Optional[bool] = False) -> Union[Generator[str], List[str]]:
            Retrieve all directories in a given path.

        @staticmethod
        def get_files(path: str, exclude: Optional[Iterable[str]] = None,
                      optimize: Optional[bool] = False) -> Union[Generator[str], List[str]]:
            Retrieve all files in a given path.

        @staticmethod
        def listdir(path: str, exclude: Optional[Iterable[str]] = None,
                    dirs_only: Optional[bool] = False, files_only: Optional[bool] = False,
                    optimize: Optional[bool] = False) -> Union[Generator[str], List[str]]:
            Retrieve files/directories in a given path.

        @staticmethod
        def join(path: str, *paths: Optional[Any]) -> str:
            Join two or more paths together.
    """

    @staticmethod
    def make_dirs(path: AnyStr, verbose: Optional[int] = 0) -> None:
        """Create Directory if it doesn't exist.

        Args:
            path (AnyStr): Directory/directories to be created.
            verbose (bool, optional): Defaults to 0. 0 turns of logging,
                while 1 gives feedback on creation of director(y|ies).

        Example:
            ```python
            >>> path = File.join("path/to", "be/created/")
            >>> File.make_dirs(path, verbose=1)
            INFO  |  "path/to/be/created/" has been created.
            ```
        """

    @staticmethod
    def remove(path: AnyStr, verbose: Optional[int] = 0) -> None:
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

    @staticmethod
    def get_dirs(path: AnyStr, exclude: Optional[Iterable[AnyStr]] = None,
                 optimize: Optional[bool] = False) -> Union[Generator[AnyStr], List[AnyStr]]:
        """Retrieve all directories in a given path.

        Args:
            path (AnyStr): Base directory of directories to retrieve.
            exclude (Iterable[AnyStr], optional): Defaults to None. List of paths to
                remove from results.
            optimize (bool, optional): Defaults to False. Return an generator object,
                to prevent loading all directories in memory, otherwise: return results
                as a normal list.

        Raises:
            FileNotFoundError: `path` was not found.

        Returns:
            Union[Generator[AnyStr], List[AnyStr]]: Generator expression if optimization is turned on,
                otherwise list of directories in given path.
        """

    @staticmethod
    def get_files(path: AnyStr, exclude: Optional[Iterable[AnyStr]] = None,
                  optimize: Optional[bool] = False) -> Union[Generator[AnyStr], List[AnyStr]]:
        """Retrieve all files in a given path.

        Args:
            path (AnyStr): Base directory of files to retrieve.
            exclude (Iterable[AnyStr], optional): Defaults to None. List of paths to
                remove from results.
            optimize (bool, optional): Defaults to False. Return an generator object,
                to prevent loading all directories in memory, otherwise: return results
                as a normal list.

        Raises:
            FileNotFoundError: `path` was not found.

        Returns:
            Union[Generator[AnyStr], List[AnyStr]]: Generator expression if optimization is turned on,
                otherwise list of files in given path.
        """

    @staticmethod
    def listdir(path: AnyStr, exclude: Optional[Iterable[AnyStr]] = None,
                dirs_only: Optional[bool] = False, files_only: Optional[bool] = False,
                optimize: Optional[bool] = False) -> Union[Generator[AnyStr], List[AnyStr]]:
        """Retrieve files/directories in a given path.

        Args:
            path (AnyStr): Base directory of path to retrieve.
            exclude (Iterable[AnyStr], optional): Defaults to None. List of paths to
                remove from results.
            dirs_only (bool, optional): Defaults to False. Return only directories in `path`.
            files_only (bool, optional): Defaults to False. Return only files in `path`.
            optimize (bool, optional): Defaults to False. Return an generator object,
                to prevent loading all directories in memory, otherwise: return results
                as a normal list.

        Raises:
            FileNotFoundError: `path` was not found.

        Returns:
            Union[Generator[AnyStr], List[AnyStr]]: Generator expression if optimization is turned on,
                otherwise list of directories in given path.
        """

    @staticmethod
    def join(path: AnyStr, *paths: Optional[Union[Iterable[AnyStr], AnyStr]]) -> AnyStr:
        """Join two or more paths together.

        Args:
            path (AnyStr): Base path. Starting point.
            *paths (Union[Iterable[AnyStr], AnyStr]): List of paths to be joined to `path`.

        Returns:
            AnyStr: Joined path.
        """

    @staticmethod
    def exists(path: AnyStr) -> bool:
        """Test whether a path exists.

        Args:
            path (str): Path to test.

        Returns:
            bool - Returns False for broken symbolic links, True if path exists.
        """

    @staticmethod
    def is_file(path: AnyStr) -> bool:
        """Test whether a path is a regular file.

        Args:
            path (str): Path to test.

        Returns:
            bool - Return true if the pathname refers
                to an existing regular file.
        """

    @staticmethod
    def is_dir(path: AnyStr) -> bool:
        """Test whether a path is an existing directory.

        Args:
            path (str): Path to test.

        Returns:
            bool - Return true if the pathname refers
                to an existing directory.
        """

    @staticmethod
    def rel_path(path: AnyStr, start: AnyStr = None) -> AnyStr:
        """Return a relative version of a path.

        Args:
            path (str): An absolute path.
            start (str): Where to start relativity.
                Uses current dir if not given.

        Returns:
            str - Relative path from `start`.
        """

    @staticmethod
    def abs_path(path: AnyStr) -> AnyStr:
        """Return the absolute version of a path.

        Args:
            path (str): Path.

        Returns:
            str - Empty path must return current working directory.
                Bad path returns unchanged.
        """

    @staticmethod
    def basename(path: AnyStr) -> AnyStr:
        """Returns the final component of a pathname.

        Args:
            path (AnyStr): Path name.

        Returns:
            AnyStr - Base name of the given path.
        """

    @staticmethod
    def dirname(path: AnyStr) -> AnyStr:
        """Returns the directory component of a pathname.

        Args:
            path (AnyStr): Path name.

        Returns:
            AnyStr - Directory of a given file.
        """

    @staticmethod
    def filename(path: AnyStr) -> AnyStr:
        """Returns the final component of a pathname without extension.

        Args:
            path (str): Path name.

        Returns:
            AnyStr - File name of the given path without extension.
        """

    @staticmethod
    def ext(path: AnyStr) -> AnyStr:
        """Returns extension of a give path.

        Args:
            path (AnyStr): Path name.

        Examples:
            ```python
            >>> # For files.
            >>> path = 'path/to/file.ext'
            >>> ext = File.ext(path)
            >>> assert(ext, 'ext')
            >>>
            >>> # For directories.
            >>> path = 'path/to/directory'
            >>> ext = File.ext(path)
            >>> assert(ext, '')
            ```

        Returns:
            AnyStr - Extension of path.
        """


################################################################################################
# +--------------------------------------------------------------------------------------------+
# | Log: Generic log class, for logging messages and monitoring progress.
# +--------------------------------------------------------------------------------------------+
################################################################################################
class Log(metaclass=ABCMeta):
    """Generic log class, for logging messages and monitoring progress.

    Methods:
         @staticmethod
        def setLevel(level: int) -> None:
            Set log level.

        @staticmethod
        def debug(*args: Any, **kwargs: Any) -> None:
            Debug logger - for debugging purposes.

        @staticmethod
        def info(*args: Any, **kwargs: Any) -> None:
            Info logger - for information & related messages.

        @staticmethod
        def warn(*args: Any, **kwargs: Any) -> None:
            Warn logger - for warnings & related messages.

        @staticmethod
        def error(*args: Any, **kwargs: Any) -> None:
            Error logger - for error related messages.

        @staticmethod
        def critical(*args: Any, **kwargs: Any) -> None:
            Critical logger - for critical log messages.

        @staticmethod
        def exception(*args: Any, **kwargs: Any) -> None:
            Exception logger - for exception related messages.

        @staticmethod
        def fatal(*args: Any, code: Optional[int] = -1, **kwargs: Any) -> None:
            Logs critical message and halts execution.

        @staticmethod
        def log(*args: Any, verbose: Optional[int] = 1, **kwargs: Any) -> None:
            Logger based on configured log level.

        @staticmethod
        def progress(count: int, max_count: int) -> None:
            Prints task progress *(in %)*.

        @staticmethod
        def report_hook(block_no: SupportsInt,
                        read_size: Union[SupportsBytes, SupportsInt],
                        file_size: Union[SupportsBytes, SupportsBytes]) -> None:
            Calculates download progress of downloaded files.


    Attributes:
        _logger (Logger): File logger configuration.
        level (int): Log level configuration.
        Level (IntEnum): Possible log level options.
    """

    """File logger configuration."""
    _logger = ...  # type: Logger

    """Log level configuration."""
    level = ...  # type: int

    """Possible log level options."""
    Level = ...  # type: IntEnum

    @staticmethod
    def setLevel(level: Type[Log.Level]) -> None:
        """Set log level.

        Args:
            level (Type[Log.Level]): A valid log level. See `Log.Level` for possible options.

        Returns:
            None
        """

    @staticmethod
    def debug(*args: Any, **kwargs: Any) -> None:
        """Debug logger - for debugging purposes.

        Args:
            *args (Any): List of arguments to be printed.

        Keyword Args:
            See `logging.log` for keyword arguments.

        See Also:
            `Log.info` - Info logger.
            `Log.error` - Error logger.
            `Log.warn` - Warning logger.
            `Log.log` - Based on `Log.level`.
            `Log.critical` - Critical logger.
            `Log.fatal` - Fatal logger & halt.
            `Log.exception` - Exception logger.

        Returns:
            None
        """

    @staticmethod
    def info(*args: Any, **kwargs: Any) -> None:
        """Info logger - for information & related messages.

        Args:
            *args (Any): List of arguments to be printed.

        Keyword Args:
            See `logging.log` for keyword arguments.

        See Also:
            `Log.debug` - Debug logger.
            `Log.warn` - Warning logger.
            `Log.error` - Error logger.
            `Log.log` - Based on `Log.level`.
            `Log.critical` - Critical logger.
            `Log.fatal` - Fatal logger & halt.
            `Log.exception` - Exception logger.

        Returns:
            None
        """

    @staticmethod
    def warn(*args: Any, **kwargs: Any) -> None:
        """Warn logger - for warnings & related messages.

        Args:
            *args (Any): List of arguments to be printed.

        Keyword Args:
            See `logging.log` for keyword arguments.

        See Also:
            `Log.info` - Info logger.
            `Log.debug` - Debug logger.
            `Log.error` - Error logger.
            `Log.log` - Based on `Log.level`.
            `Log.critical` - Critical logger.
            `Log.fatal` - Fatal logger & halt.
            `Log.exception` - Exception logger.

        Returns:
            None
        """

    @staticmethod
    def error(*args: Any, **kwargs: Any) -> None:
        """Error logger - for error related messages.

        Args:
            *args (Any): List of arguments to be printed.

        Keyword Args:
            See `logging.log` for keyword arguments.

        See Also:
            `Log.info` - Info logger.
            `Log.debug` - Debug logger.
            `Log.warn` - Warning logger.
            `Log.log` - Based on `Log.level`.
            `Log.critical` - Critical logger.
            `Log.fatal` - Fatal logger & halt.
            `Log.exception` - Exception logger.

        Returns:
            None
        """

    @staticmethod
    def critical(*args: Any, **kwargs: Any) -> None:
        """Critical logger - for critical log messages.

        Args:
            *args (Any): List of arguments to be printed.

        Keyword Args:
            See `logging.log` for keyword arguments.

        See Also:
            `Log.info` - Info logger.
            `Log.debug` - Debug logger.
            `Log.error` - Error logger.
            `Log.warn` - Warning logger.
            `Log.log` - Based on `Log.level`.
            `Log.fatal` - Fatal logger & halt.
            `Log.exception` - Exception logger.

        Returns:
            None
        """

    @staticmethod
    def exception(*args: Any, **kwargs: Any) -> None:
        """Exception logger - for exception related messages.

        Args:
            *args (Any): List of arguments to be printed.

        Keyword Args:
            See `logging.log` for keyword arguments.

        See Also:
            `Log.info` - Info logger.
            `Log.debug` - Debug logger.
            `Log.warn` - Warning logger.
            `Log.error` - Error logger.
            `Log.log` - Based on `Log.level`.
            `Log.critical` - Critical logger.
            `Log.fatal` - Fatal logger & halt.

        Returns:
            None
        """

    @staticmethod
    def fatal(*args: Any, code: Optional[int] = -1, **kwargs: Any) -> None:
        """Logs critical message and halts execution.

        Args:
            *args (Any): List of arguments to be printed.
            code (int, optional): Defaults to 1. Exit code.

        Keyword Args:
            See `logging.log` for keyword arguments.

        See Also:
            `Log.info` - Info logger.
            `Log.debug` - Debug logger.
            `Log.error` - Error logger.
            `Log.warn` - Warning logger.
            `Log.log` - Based on `Log.level`.
            `Log.critical` - Critical logger.
            `Log.exception` - Exception logger.

        Returns:
            None
        """

    @staticmethod
    def log(*args: Any, verbose: Optional[int] = 1, **kwargs: Any) -> None:
        """Logger based on configured log level.

        Args:
            *args (Any): List of arguments to be printed.
            verbose (int, optional): Defaults to 1. Verbosity level.

        Keyword Args:
            See `logging.log` for keyword arguments.

        See Also:
            `Log.info` - Info logger.
            `Log.debug` - Debug logger.
            `Log.error` - Error logger.
            `Log.warn` - Warning logger.
            `Log.critical` - Critical logger.
            `Log.fatal` - Fatal logger & halt.
            `Log.exception` - Exception logger.

        Returns:
            None
        """

    @staticmethod
    def pretty(args: Any, stream: BinaryIO[bytes] = None, indent: int = 1,
               width: int = 80, depth: int = None, *, compact: bool = False):
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

    @staticmethod
    def progress(count: int, max_count: int) -> None:
        """Prints task progress *(in %)*.

        Args:
            count {int}: Current progress so far.
            max_count {int}: Total progress length.

        See Also:
            `Log.report_hook` - Calculates download progress of downloaded files.
        """

    @staticmethod
    def report_hook(block_no: SupportsInt,
                    read_size: Union[SupportsBytes, SupportsInt],
                    file_size: Union[SupportsBytes, SupportsBytes]) -> None:
        """Calculates download progress of downloaded files.

        Args:
            block_no (SupportsInt): Current download state.
            read_size (Union[SupportsBytes, SupportsInt]): Current downloaded size.
            file_size (Union[SupportsBytes, SupportsInt]): Total file size.

        See Also:
            `Log.progress` - Prints task progress *(in %)*.

        Returns:
            None.
        """


################################################################################################
# +--------------------------------------------------------------------------------------------+
# | Cache: For saving objects and converting numpy objects to pickle.
# +--------------------------------------------------------------------------------------------+
################################################################################################
class Cache(metaclass=ABCMeta):
    """For saving objects and converting numpy objects to pickle.

    Methods:
        @staticmethod
        def cache(cache_path: str, fn: Callable,
                  use_numpy: Optional[bool] = False, verbose: Optional[int] = 1,
                  *args: Any, **kwargs: Any) -> Any:
            Cache-wrapper for a numpy array or object.

        @staticmethod
        def cache_numpy(cache_path: str, fn: Callable,
                        verbose: Optional[int] = 1,
                        *args: Any, **kwargs: Any) -> Any:
            Cache-wrapper for a function or class.

        @staticmethod
        def convert_numpy2pickle(in_path: str, out_path: str) -> None:
            Convert a numpy-file to pickle-file.
    """

    @staticmethod
    def cache(cache_path: AnyStr, fn: Callable[..., Any],
              use_numpy: Optional[bool] = False, verbose: Optional[int] = 1,
              *args: Any, **kwargs: Any) -> Any:
        """Cache-wrapper for a numpy array or object.

        Notes:
            If the cache-file exists then the data is reloaded and
            returned, otherwise the function is called and the result
            is saved to cache. The fn-argument can also be a class
            instead, in which case an object-instance is created and
            saved to the cache-file.

        Args:
            cache_path (AnyStr): File-path for the cache-file.
            fn (Callable[..., Any]): Function or class to be called.
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

    @staticmethod
    def cache_numpy(cache_path: AnyStr, fn: Callable[..., Any],
                    verbose: Optional[int] = 1,
                    *args: Any, **kwargs: Any) -> Any:
        """Cache-wrapper for a function or class.

        Notes:
            If the cache-file exists then the data is reloaded and
            returned, otherwise the function is called and the result
            is saved to cache. The fn-argument can also be a class
            instead, in which case an object-instance is created and
            saved to the cache-file.

        Args:
            cache_path (AnyStr): File-path for the cache-file.
            fn (Callable[..., Any]): Function or class to be called.
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

    @staticmethod
    def convert_numpy2pickle(in_path: AnyStr, out_path: AnyStr) -> None:
        """Convert a numpy-file to pickle-file.

        Notes:
            The first version of the cache-function used numpy for
            saving the data. Instead of re-calculating all the data,
            you can just convert the cache-file using this function.

        Args:
            in_path (AnyStr): Input file in numpy-format written using numpy.save().
            out_path (AnyStr): Output file written as a pickle-file.

        Returns:
            Nothing.
        """
