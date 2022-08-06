# DATA HACK
## Кейс 2. Генератор Фейковый Данных для Сложных Запросов
### Информация про различные виды полей

Название класса | Его описание
---|---
SparkField | *абстрактный класс*, на основе которого строятся всевозможные виды полей 
Range |базовый класс для IntegerRange и FloatRange
IntegerRange | класс для генерации рандомного целого числа от start до stop
FloatRange | класс для генерации рандомного вещественного числа от start до stop
Constant | класс для генерации констант
StringRange | класс для генерации строк с заданным алфавитом длины от from_length до to_length
StringLen | класс для генерации строк с заданным алфавитом с фиксированной длиной
Select | класс для генерации чисел и строк из заданного набора значений
Mask | базовый класс для IntegerMask и StringMask
IntegerMask | класс для генерации чисел с помощью масок
StringMask | класс для генерации строк с помощью масок
Time | базовый класс для Date и Timestamp
Date | класс для генерации данных типа date
Timestamp | класс для генерации данных типа timestamp

### Про поля настройки в config.json для различных датаклассов

#### Ключи для настройки IntegerRange, FLoatRange

Ключ | Описание
---|---
start, stop | диапазон значений [start, stop], в рамках которых происходит генерация значений чисел

#### Ключи для настройки Constant

Ключ | Описание
---|---
value | значение константы

#### Ключи для настройки StringRange

Ключ | Описание
---|---
from_length, to_length | диапазог значений [from_length, to_length], в рамках которых происходит генерация длины строки
alphabet | строка символов (алфавит), из которых генерируется строка

#### Ключи для настройки StringLen

Ключ | Описание
---|---
length | длина генерируемой строки
alphabet | строка символов (алфавит), из которых генерируется строка

#### Ключи для настройки Select

Ключ | Описание
---|---
select | множество (сет) символов, из которых мы собираем строку/число

#### Ключи для настройки IntegerMask, StringMask

Ключ | Описание
---|---
mask | строка, которая описывает маску. # отвечает за произвольный символ. Пример: "12fds###s"
alphabet | строка символов (алфавит), из которых генерируются буквы на место символа # в маске

#### Ключи для настройки Date

Ключ | Описание
---|---
start_year, start_month, start_day | дата date(start_year, start_month, start_day), начиная с которой происходит генерация дат
stop_year, stop_month, stop_day | дата date(end_year, end_month, end_day), заканчивая которой происходит генерация дат

#### Ключи для настройки TimeStamp

Ключ | Описание
---|---
start_year, start_month, start_day, start_hour, start_minute | время метка datetime(start_year, start_month, start_day, start_hour, start_minute), начиная с которой происходит генерация временных меток
stop_year, stop_month, stop_day, stop_hour, stop_minute | время метка datetime(end_year, end_month, end_day, end_hour, end_minute), заканчивая которой происходит генерация временных меток
