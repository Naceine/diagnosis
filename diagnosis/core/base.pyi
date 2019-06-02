"""Base class for diagnosis.

   @author
     Victor I. Afolabi
     Artificial Intelligence & Software Engineer.
     Email: javafolabi@gmail.com
     GitHub: https://github.com/victor-iyiola

   @project
     File: base.pyx
     Created on 2nd June, 2019 @ 12:27 PM.

   @license
     BSD-3 Clause license.
     Copyright (c) 2018. Victor I. Afolabi. All rights reserved.
"""

from abc import ABCMeta
from typing import Any, Dict, Iterable, List, Optional, Union


################################################################################################
# +--------------------------------------------------------------------------------------------+
# | Run mode: Tran, test, validation.
# +--------------------------------------------------------------------------------------------+
################################################################################################
class Mode(metaclass=ABCMeta):
    """Mode represents various data & model processing phase.

    Attributes:
        TEST (str) - Test phase: To evaluate how a model performs on unseen data.
        TRAIN (str) - Training phase: To train a model on labelled samples.
        PREDICT (str) - Prediction phase: To predict new unseen data.
        VALIDATE (str) - Validation phase: To evaluate how a model performs during training.
        INFERENCE (str) - For production level prediction.
    """

    __class__ = ...  # type: type
    __module__ = ...  # type: str
    __doc__ = ...  # type: Optional[str]
    __dict__ = ...  # type: Dict[str, Any]
    __slots__ = ...  # type: Union[str, Iterable[str]]

    """TEST (str) - Test phase: To evaluate how a model performs on unseen data."""
    TEST = ...  # type: str

    """TRAIN (str) - Training phase: To train a model on labelled samples."""
    TRAIN = ...  # type: str

    """PREDICT (str) - Prediction phase: To predict new unseen data."""
    PREDICT = ...  # type: str

    """VALIDATE (str) - Validation phase: To evaluate how a model performs during training."""
    VALIDATE = ...  # type: str

    """INFERENCE (str) - For production level prediction."""
    INFERENCE = ...  # type: str


################################################################################################
# +--------------------------------------------------------------------------------------------+
# | Base: Base class for all classes.
# +--------------------------------------------------------------------------------------------+
################################################################################################
class Base(object, metaclass=ABCMeta):
    """Abstract Base Class for all objects.

    Methods:
        def __init__(self, *args: Any, **kwargs: Any) -> None: ...

        def __repr__(self) -> str: ...

        def __str__(self) -> str: ...

        def __format__(self, format_spec: Optional[str]) -> str: ...

        def _log(self, *args: Any, level: Optional[str] = 'debug', **kwargs: Any) -> None: ...

        def _get_args(self) -> List[Any]: ...

        def _get_kwargs(self) -> Dict[str, Any]: ...

    Attributes:
        verbose (int, optional) - Defaults to 1. Verbosity level.
        name (str, optional) - Defaults to self.__class__.__name__ i.e sub-class name.
            Useful for debugging or caching instances of classes.
    """

    __class__ = ...  # type: type
    __module__ = ...  # type: str
    __doc__ = ...  # type: Optional[str]
    __dict__ = ...  # type: Dict[str, Any]
    __slots__ = ...  # type: Union[str, Iterable[str]]

    # Properties.
    """Verbosity level. Defaults to 1."""
    verbose = ...  # type: Optional[int]

    """Useful for debugging or caching instances of classes."""
    name = ...  # type: Optional[str]

    def __init__(self, *args: Any, **kwargs: Any) -> None: ...

    def __repr__(self) -> str: ...

    def __str__(self) -> str: ...

    def __format__(self, format_spec: Optional[str]) -> str: ...

    def _log(self, *args: Any, level: Optional[str] = 'debug', **kwargs: Any) -> None:
        """Convenient Class logger method.

        Args:
            *args (Any): Arguments to be logged.
            level (str, optional): Defaults to debug. Log level.
            **kwargs (Any, optional): Other keyword arguments to be
                passed into logging.`${level}`(**kwargs).

        Returns:
            None
        """

    def _get_args(self) -> List[Any]:
        """Returns class positional arguments.

        Returns:
            List[Any] - List of object's positional arguments.
        """

    def _get_kwargs(self) -> Dict[str, Any]:
        """Returns class keyword arguments.

        Returns:Ob
            Dict[str, Any] - Objects keyword arguments.
        """


# noinspection PyUnresolvedReferences
class Attr(dict):
    """Get attributes.

    Examples:
        ```python
        >>> d = Attr({'foo':3})
        >>> d['foo']
        3
        >>> d.foo
        3
        >>> d.bar
        Traceback (most recent call last):
        ...
        AttributeError: 'Attr' object has no attribute 'bar'

        Works recursively

        >>> d = Attr({'foo':3, 'bar':{'x':1, 'y':2}})
        >>> isinstance(d.bar, dict)
        True
        >>> d.bar.x
        1

        Bullet-proof

        >>> Attr({})
        {}
        >>> Attr(d={})
        {}
        >>> Attr(None)
        {}
        >>> d = {'a': 1}
        >>> Attr(**d)
        {'a': 1}

        Set attributes

        >>> d = Attr()
        >>> d.foo = 3
        >>> d.foo
        3
        >>> d.bar = {'prop': 'value'}
        >>> d.bar.prop
        'value'
        >>> d
        {'foo': 3, 'bar': {'prop': 'value'}}
        >>> d.bar.prop = 'newer'
        >>> d.bar.prop
        'newer'


        Values extraction

        >>> d = Attr({'foo':0, 'bar':[{'x':1, 'y':2}, {'x':3, 'y':4}]})
        >>> isinstance(d.bar, list)
        True
        >>> from operator import attrgetter
        >>> map(attrgetter('x'), d.bar)
        [1, 3]
        >>> map(attrgetter('y'), d.bar)
        [2, 4]
        >>> d = Attr()
        >>> d.keys()
        []
        >>> d = Attr(foo=3, bar=dict(x=1, y=2))
        >>> d.foo
        3
        >>> d.bar.x
        1

        Still like a dict though

        >>> o = Attr({'clean':True})
        >>> o.items()
        [('clean', True)]

        And like a class

        >>> class Flower(Attr):
        ...     power = 1
        ...
        >>> f = Flower()
        >>> f.power
        1
        >>> f = Flower({'height': 12})
        >>> f.height
        12
        >>> f['power']
        1
        >>> sorted(f.keys())
        ['height', 'power']
        ```
    """

    def __init__(self, d: Dict[str, Any] = None, **kwargs: Any) -> None: ...

    def __setattr__(self, name: str, value: Any) -> None: ...

    __setitem__ = __setattr__
