from functools import partial
from inspect import iscoroutinefunction as is_async
from typing import (
    get_args, get_origin,
    Union, Annotated, Any, Type, Callable, Iterable, List, Mapping, ForwardRef
)

from pydantic import validate_arguments
import orjson as json

from pyservices.signals import service_signals, endpoint_signals


class _Dependency:
    """
    """

    new: bool = False
    new_recursive: bool = False
    args: Union[Iterable, None] = None
    kwargs: Union[Mapping, None] = None

    def mutate(
        self,
        new: bool = None,
        new_recursive: bool = None,
        args: Union[Iterable, None] = None,
        kwargs: Union[Mapping, None] = None
    ) -> '_Dependency':
        mutated = _Dependency()
        mutated.new = self.new if new is None else new
        mutated.new_recursive = self.new_recursive if new_recursive is None else new_recursive
        mutated.args = self.args if args is None else args
        mutated.kwargs = self.kwargs if kwargs is None else kwargs
        return mutated

    __call__ = mutate

    def __str__(
        self
    ) -> str:
        output = 'Depend'
        if self.new:
            output += ' new'
        if self.new_recursive:
            output += ' new_recursive'
        if self.args:
            output += ' args'
        if self.kwargs:
            output += ' kwargs'
        return output


Depend = _Dependency()


class _ServiceEndpoint:

    service_class: Type
    method: Callable
    _async_method: bool
    _json_output: bool

    def __init__(
        self,
        service_class: Type,
        method: Callable,
        validate_payload: bool = True,
        json_output: bool = True,
    ):
        self.service_class = service_class
        self._async_method = is_async(method)
        if validate_payload:
            self.method = validate_arguments(method)
        else:
            self.method = method
        self._json_output = json_output

    async def call(
        self,
        *args: Iterable,
        **kwargs: Mapping
    ) -> Any:
        """
        """
        await service_signals.fire('begin')
        try:
            instance = await initialize(self.service_class)
        except Exception as e:
            await service_signals.fire('catch', e)
            raise e
        await service_signals.fire('end')
        await endpoint_signals.fire('begin')
        try:
            if self._async_method:
                output = await self.method(instance, *args, **kwargs)
            else:
                output = self.method(instance, *args, **kwargs)
        except Exception as e:
            await endpoint_signals.fire('catch', e)
            raise e
        await endpoint_signals.fire('end')
        if self._json_output:
            return json.dumps(output)
        return output

    __call__ = call


def get_class_methods(
    klass
) -> List[Callable]:
    """
    Return user defined class methods as list
    """
    class_attributes = [getattr(klass, a) for a in dir(klass) if a.startswith('_') is False]
    return [m for m in class_attributes if callable(m)]


class ServiceNotFound(Exception):
    """
    """


def hash_class(
    klass: Union[Type, ForwardRef, str]
) -> str:
    if isinstance(klass, ForwardRef) and klass.__forward_is_class__:
        return klass.__forward_arg__
    if isinstance(klass, str):
        return klass
    return klass.__name__


class __ServiceRegistry:

    __registry = {}

    def get(
        self,
        service_annotation: Union[Type, ForwardRef, str]
    ) -> Type:
        """
        Raises:
            - ServiceNotFound
        """
        service_hash = hash_class(service_annotation)
        service_class = self.__registry.get(service_hash, None)
        if service_class is None:
            raise ServiceNotFound()
        return service_class

    def set(
        self,
        klass
    ) -> None:
        """
        """
        service_hash = hash_class(klass)
        self.__registry[service_hash] = klass


service_registry = __ServiceRegistry()


def make_service(
    klass
):
    service_registry.set(klass)
    for method in get_class_methods(klass):
        method.as_endpoint = partial(_ServiceEndpoint, klass, method)


def service(
    klass
):
    def wrap(klass):
        make_service(klass)
        return klass
    if klass is None:
        return wrap
    return wrap(klass)


async def initialize(
    service_class: Union[ForwardRef, str, Type],
    __already_initialized: Mapping = None,
    __path: List[Type] = None,
):
    """
    """
    if __already_initialized is None:
        __already_initialized = {}

    # Creates new list of service classes
    # if __path is None:
    #     __path = [service_class]
    # else:
    #     __path = __path + [service_class]

    # initializes class
    service_class = service_registry.get(service_class)
    root_instance = service_class()
    root_class_hash = hash_class(service_class)
    __already_initialized[root_class_hash] = root_instance

    if not hasattr(root_instance, '__annotations__'):
        # set default attribute __annotations__
        root_instance.__annotations__ = {}

    for child_service_name, v in root_instance.__annotations__.items():
        if get_origin(v) is not Annotated:
            continue

        try:
            child_class, dependency = get_args(v)
        except Exception:
            continue

        if not isinstance(dependency, _Dependency):
            # annotated value is not instance of _Dependency
            continue

        child_class_hash = hash_class(child_class)

        if dependency.new:
            # initialize (again) only this dependency
            child_instance = None
            child_already_initialized = __already_initialized
        elif dependency.new_recursive:
            # reset initialized instances
            child_instance = None
            child_already_initialized = {}
        else:
            # get already initialized instance
            child_instance = __already_initialized.get(child_class_hash, None)
            child_already_initialized = __already_initialized

        if child_instance is None:
            # otherwise initialize it recursively
            child_instance = await initialize(child_class, child_already_initialized, __path)
            child_already_initialized[child_class_hash] = child_instance

        # set child service as attribute
        setattr(root_instance, child_service_name, child_instance)

    # print(__path, 'initialized')
    return root_instance

