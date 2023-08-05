from abc import ABC, abstractmethod
from typing import Any, Callable, Generic, Optional, Protocol, TypeVar


T = TypeVar("T")

class DescriptorProtocol(Protocol, Generic[T]):
    def __get__(self, obj: Optional[object], cls: type[object]) -> T:
        ...
    
    def __set__(self, obj: Optional[object], value: T) -> None:
        ...
    
    def __delete__(self, obj: Optional[object]) -> None:
        ...

    @property
    def name(self) -> str:
        ...


class Descriptor(Generic[T], DescriptorProtocol[T], ABC):
    class AccessError(Exception):
        pass

    def __set_name__(self, owner: type, name: str):
        self._name = name

    @abstractmethod
    def _object_get(self, obj: object) -> T:
        raise NotImplementedError

    @abstractmethod
    def _class_get(self, cls: type[object]) -> T:
        raise NotImplementedError

    @abstractmethod
    def _set(self, obj: object, value: T) -> None:
        raise NotImplementedError

    @abstractmethod
    def _delete(self, obj: object) -> None:
        raise NotImplementedError

    def __get__(self, obj: Optional[object], cls: type[object]) -> T:
        if obj == None:
            try:
                return self._class_get(cls)
            except AttributeError:
                raise AttributeError(f"'{cls.__name__}' object has no attribute '{self._name}'") from None
            except self.AccessError:
                raise AttributeError(f"unreadable attribute '{self._name}'")
        else:
            try:
                return self._object_get(obj)
            except AttributeError:
                raise AttributeError(f"type object '{cls.__name__}' has no attribute '{self._name}'") from None
            except self.AccessError:
                raise AttributeError(f"unreadable attribute '{self._name}'")

    def __set__(self, obj: object, value: T):
        try:
            self._set(obj, value)
        except self.AccessError:
            raise AttributeError(f"can't set attribute '{self._name}'")

    def __delete__(self, obj: object):
        try:
            self._delete(obj)
        except AttributeError:
            raise AttributeError(self._name)
        except self.AccessError:
            raise AttributeError(f"can't delete attribute '{self._name}'")

    @property
    def name(self):
        return self._name


class Value(Generic[T], Descriptor[T]):
    def __init__(self) -> None:
        super().__init__()

    def __set_name__(self, owner: type, name: str):
        super().__set_name__(owner, name)
        self._value_attribute_name = "_Value__" + name

    
    def _object_get(self, obj: object) -> T:
        return getattr(obj, self._value_attribute_name)

    def _class_get(self, cls: type[object]) -> T:
        return getattr(cls, self._value_attribute_name)

    def _set(self, obj: object, value: T) -> None:
        setattr(obj, self._value_attribute_name, value)

    def _delete(self, obj: object) -> None:
        delattr(obj, self._value_attribute_name)

class Restrict(Generic[T], Descriptor[T]):
    def __init__(self, descriptor: DescriptorProtocol[T], get: bool = True, set: bool = False, delete: bool = False, class_get: bool = False):
        self._descriptor = descriptor
        self._get_allowed = get
        self._set_allowed = set
        self._delete_allowed = delete
        self._class_get_allowed = class_get

    def _object_get(self, obj: object) -> T:
        if not self._get_allowed:
            raise self.AccessError
        return self._descriptor.__get__(obj, type(obj))

    def _set(self, obj: Optional[object], value: T) -> None:
        if not self._set_allowed:
            raise self.AccessError
        self._descriptor.__set__(obj, value)

    def _delete(self, obj: Optional[object]) -> None:
        if not self._delete_allowed:
            raise self.AccessError
        self._descriptor.__delete__(obj)

    def _class_get(self, cls: type[object]) -> T:
        if not self._class_get_allowed:
            raise self.AccessError
        return self._descriptor.__get__(None, cls)


class Property(Generic[T], Descriptor[T]):
    __getter: Optional[Callable[[Any], T]]
    __setter: Optional[Callable[[Any, T], None]]
    __deleter: Optional[Callable[[Any], None]]
    __class_getter: Optional[Callable[[Any], T]]

    def __init__(self, getter: Optional[Callable[[Any], T]] = None, setter: Optional[Callable[[Any, T], None]] = None, deleter: Optional[Callable[[Any], None]] = None, class_getter: Optional[Callable[[Any], T] | classmethod[T]] = None):
        self.__getter = getter
        self.__setter = setter
        self.__deleter = deleter

        if isinstance(class_getter, classmethod):
            self.__class_getter = class_getter.__func__
        else:
            self.__class_getter = class_getter

    @property
    def __isabstractmethod__(self) -> bool:
        functions = (self.__getter, self.__setter, self.__deleter, self.__class_getter)
        for func in functions:
            if hasattr(func, "__isabstractmethod__") and getattr(func, "__isabstractmethod__"):
                return True
        return False

    def _object_get(self, obj: object) -> T:
        if self.__getter:
            return self.__getter(obj)
        raise self.AccessError

    def _set(self, obj: object, value: T) -> None:
        if self.__setter:
            self.__setter(obj, value)
        raise self.AccessError

    def _delete(self, obj: object) -> None:
        if self.__deleter:
            self.__deleter(obj)
        raise self.AccessError

    def _class_get(self, cls: type[object]) -> T:
        if self.__class_getter:
            self.__class_getter(cls)
        raise self.AccessError

    def getter(self, f: Optional[Callable[[Any], T]]):
        self.__getter = f

    def setter(self, f: Optional[Callable[[Any, T], None]]):
        self.__setter = f

    def deleter(self, f: Optional[Callable[[Any], None]]):
        self.__deleter = f

    def class_getter(self, f: Optional[Callable[[Any], T] | classmethod[T]]):
        if isinstance(f, classmethod):
            self.__class_getter = f.__func__
        else:
            self.__class_getter = f