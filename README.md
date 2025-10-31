# Registrar

**Универсальный регистратор функций с автоматическим UID для Python**

Легковесная система регистрации и управления функциями с уникальными идентификаторами. Хорошо подходит для для плагинов, команд, пайплайнов и диспетчеризации.

## Особенности

- **Универсальный** - регистрируйте любые функции и callable-объекты
- **Автоматические UID** - генерация уникальных идентификаторов через `MyID`
- **Синглтон-пулы** - глобальные именованные пулы функций
- **Множественные способы регистрации** - декораторы, прямое присваивание
- **Dict-интерфейс** - работайте как со словарем: `[]`, `in`, `keys()`, `items()`
- **Защита от дубликатов** - предотвращение повторной регистрации

## Установка
### Способ 1: Установка из репозитория (требуется Git)
```bash
pip install git+https://github.com/Sam-Strand/registrar.git
```

### Способ 2: Установка готового пакета (без Git)
```bash
pip install https://github.com/Sam-Strand/registrar/releases/download/v1.0.0/registrar-1.0.0-py3-none-any.whl
```

## Быстрый старт
```python
from registrar import Registrar

# Создаем пулы
math_ops = Registrar('math')
startup_tasks = Registrar('startup')

# Регистрация с автоматическим UID
@math_ops.register()
def add(a, b):
    return a + b

# Регистрация с кастомным UID
@math_ops.register('multiply')
def multiply(a, b):
    return a * b

# Прямое присваивание
math_ops['power'] = lambda a, b: a ** b

# Использование
result = math_ops['add'](2, 3)  # 5
result = math_ops['multiply'](4, 5)  # 20
