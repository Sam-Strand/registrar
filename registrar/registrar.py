from typing import Dict, Callable, TypeVar, Any, List
try:
    from my_id import MyID as get_uid
except ImportError:
    import uuid
    get_uid = uuid.uuid4
    
T = TypeVar('T')

class Registrar:
    '''
    Универсальный регистратор функций. Без указания имени функции регистрируются с автоматическим uid.
    '''
    
    _global_pools: Dict[str, 'Registrar'] = {}
    
    def __new__(cls, name: str) -> 'Registrar':
        '''Всегда возвращаем существующий пул или создаем новый'''
        if name in cls._global_pools:
            return cls._global_pools[name]
        else:
            instance = super().__new__(cls)
            cls._global_pools[name] = instance
            return instance
    
    def __init__(self, name: str) -> None:
        if not hasattr(self, 'name'):
            self.name = name
            self._function_pool: Dict[str, Callable[..., Any]] = {}
    
    def register(self, uid: str = None) -> Callable[[T], T]:
        '''
        Декоратор для регистрации функции.
        
        Args:
            uid: Опциональный идентификатор. Если None - генерируется uid.
        '''
        def decorator(func: T) -> T:
            actual_uid = uid or get_uid()
            if actual_uid in self._function_pool:
                raise KeyError(f"Функция '{actual_uid}' уже была добавлена '{self.name}'")
            self._function_pool[actual_uid] = func
            return func
        return decorator
    
    def __getitem__(self, uid: str) -> Callable[..., Any]:
        '''Обращение к функциям через registrar['uid']'''
        if uid not in self._function_pool:
            raise KeyError(f"Функция '{uid}' не существует '{self.name}'")
        return self._function_pool[uid]
    
    def __setitem__(self, uid: str, func: Callable[..., Any]) -> None:
        '''Регистрация функций через registrar['uid'] = func'''
        if uid in self._function_pool:
            raise KeyError(f"Функция '{uid}' уже была добавлена '{self.name}'")
        self._function_pool[uid] = func
    
    def __contains__(self, uid: str) -> bool:
        '''Проверка наличия функции'''
        return uid in self._function_pool
    
    @property
    def functions(self) -> List[Callable[..., Any]]:
        '''Получить список всех функций'''
        return list(self._function_pool.values())
    
    @classmethod
    def register_to(cls, pool_name: str, uid: str = None) -> Callable[[T], T]:
        '''Декоратор для прямой регистрации в указанный пул'''
        def decorator(func: T) -> T:
            pool = Registrar(pool_name)
            return pool.register(uid)(func)
        return decorator
    
    def keys(self):
        return self._function_pool.keys()
    
    def values(self):
        return self._function_pool.values()
    
    def items(self):
        return self._function_pool.items()
    
    def __repr__(self) -> str:
        return f"Registrar(name='{self.name}', functions={len(self._function_pool)})"


if __name__ == '__main__':
    # Создаем пулы через конструктор - всегда получаем существующий или создаем новый
    startup = Registrar('startup')
    math = Registrar('math')
    
    # 1. Регистрация функций
    @startup.register()
    def db_init():
        print("   🗄️ База данных готова")
        return "db_ok"
    
    @math.register('sum')
    def sum(a, b):
        return a + b
    
    @Registrar.register_to('math', 'multiply')
    def multiply(a, b):
        return a * b
    
    # 2. Проверка, что повторное создание возвращает тот же пул
    math2 = Registrar('math')
    print(f"Это один и тот же объект: {math is math2}")
    print(f"Количество функций в math2: {len(list(math2.keys()))}")
    
    # 3. Использование функций
    print("\nИспользование:")
    print(f"   math['sum'](2, 3) = {math['sum'](2, 3)}")
    print(f"   math['multiply'](4, 5) = {math['multiply'](4, 5)}")
    
    # 4. Прямое присваивание
    math['power'] = lambda a, b: a ** b
    print(f"   math['power'](2, 3) = {math['power'](2, 3)}")
    
    # 5. Проверка наличия
    print(f"\nПроверка: 'sum' в math: {'sum' in math}")
    print(f"Проверка: 'divide' в math: {'divide' in math}")
    
    # 6. Итерация по функциям
    print("\nВсе функции math:")
    for func in math.values():
        print(f"   {func.__name__}")
    
    # 7. Запуск startup
    print("\nStartup задачи:")
    for uid, func in startup.items():
        result = func()
        print(f"   {uid}: {result}")
