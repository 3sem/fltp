## аллокация регистров в LLVM

 В инфраструктуре LLVM этот процесс реализуется через набор алгоритмов, которые применяются в зависимости от целей оптимизации и особенностей целевой архитектуры.

### Этапы аллокации регистров

Процесс аллокации регистров в LLVM состоит из нескольких этапов:

1. **Анализ живых диапазонов (live range analysis)**:
   Определяются интервалы жизни каждой переменной, то есть участки кода, в которых переменная активно используется. Эти интервалы называются живыми диапазонами.

2. **Построение графа интерференций (interference graph)**:
   Строится граф, где каждая вершина представляет переменную, а рёбра соединяют пары переменных, которые не могут находиться в одном регистре одновременно (интерферентные переменные).

3. **Раскраска графа (graph coloring)**:
   Задача сводится к назначению цветов (регистров) вершинам графа так, чтобы смежные вершины имели разные цвета. Если количество регистров ограничено, некоторые переменные могут быть временно выгружены в память (процесс называется spilling).

4. **Спиллинг (spilling)**:
   Переменные, которым не хватило регистров, сохраняются в стековую память. Затем, когда эти переменные снова понадобятся, они загружаются обратно в регистр.

### Алгоритмы аллокации регистров в LLVM

LLVM поддерживает несколько алгоритмов аллокации регистров. Исторически это:

1. **Linear Scan Register Allocation**:
   Простой и быстрый алгоритм, который сканирует живые диапазоны переменных последовательно и назначает регистры в порядке их появления. Однако он не учитывает структуру графа интерференций и может приводить к неоптимальному использованию регистров.

2. **Graph Coloring Register Allocation**:
   Более сложный и эффективный алгоритм, основанный на раскраске графа интерференций. Граф строится на основе живых диапазонов, и задача сводится к поиску такой раскраски, при которой смежные вершины имеют разные цвета. Если граф нельзя раскрасить заданным количеством цветов, происходит спиллинг.

3. **Iterated Register Coalescing**:
   Улучшенная версия алгоритма графовой окраски, которая дополнительно пытается объединить смежные вершины (коалесцировать), чтобы уменьшить количество необходимых регистров.

4. **PBQP Register Allocation**:
   Алгоритм, использующий псевдобулевы методы квадратичной оптимизации для решения задачи аллокации регистров. Он стремится найти оптимальное решение, учитывая ограничения на ресурсы и зависимости между переменными.

В настоящее время -- алгоритмов 6:


1. Linear Scan Register Allocation (-regalloc=linear-scan)
2. Local Register Allocation (-regalloc=local)
3. Simple Register Allocation (-regalloc=simple)
4. Basic Register Allocation (-regalloc=basic)
5. Greedy Register Allocation (-regalloc=greedy)
6. PBQP Register Allocation (-regalloc=pbqp)

### Пример использования LLC

Рассмотрим пример использования команды `llc` для получения информации о работе алгоритмов аллокации регистров. Предположим, у нас есть следующий фрагмент кода на языке С:

```c
int foo(int a, int b) {
    return a + b;
}
```

Этот код можно перевести в LLVM IR с помощью команды `clang`, а затем обработать с помощью `llc`. Для этого создадим файл `test.c` с содержимым:

```bash
clang -S -emit-llvm test.c -o test.ll
llc -march=x86-64 -O3 -stats -o output.s test.ll
```

В результате выполнения `llc` будет создан файл `output.s` с ассемблерным кодом, а также выведена статистика выполнения различных этапов компиляции, включая аллокацию регистров. Вот пример части вывода:

```bash
...
--- Pass execution timing summary ---
 Total Execution Time: 0.145 seconds (0.135 user, 0.010 sys)
   ---Total time in passes: 0.144 seconds---
   Individual pass timings (all times are in milliseconds):
      Name            Time     CPU time (self)   Impl.   Calls        Objects
      ============   =======   ===============   =====   ======   ==============
      regalloc       15.600    14.200            C++     1           34567
      sched          18.000    19.800            C++     1           24561
      sccp           7.400     8.900             C++     1           13279
      loop-vectorize 31.200    32.700            C++     1           45678
      ...
```

на этап аллокации регистров (`regalloc`) было потрачено около 15 миллисекунд.

### выбор алгоритма в LLC
1. linear-scan:
Простой алгоритм линейного сканирования, который просматривает живые диапазоны переменных и назначает регистры по мере их появления. Быстр, но может привести к неоптимальной аллокации.
2. local:
Локальная аллокация регистров, применяемая внутри одной базовой блока (Basic Block). Этот метод хорошо подходит для небольших фрагментов кода.
3. simple:
Базовый алгоритм, похожий на линейное сканирование, но с улучшенными эвристиками для уменьшения числа спиллов (выгрузки переменных в память).
4. basic:
Алгоритм графовой окраски, более сложный и точный, но медленнее предыдущих. Использует графовые структуры для поиска оптимальной аллокации регистров.
5. greedy:
Жадный алгоритм, основанный на принципе жадного выбора регистра с учетом приоритета и стоимости спилла.
6. pbqp:
Алгоритм псевдо-булевой оптимизации, который пытается найти глобально оптимальное решение задачи аллокации регистров.

Давление на регистры — это степень использования регистров процессора программой. Чем меньше регистров используется для хранения переменных и промежуточных результатов, тем ниже давление на регистры. Давление на регистры важно учитывать, потому что оно влияет на эффективность выполнения программы: если программа исчерпала доступные регистры, ей приходится сохранять значения в памяти, что снижает производительность.

### Example:
```cpp
#include <stdio.h>

int sum_and_product(int a, int b, int c) {
    int d = a * b;
    int e = c * d;
    int f = a + b + c;
    return e + f;
}
```
Скомпилируем код в LLVM IR с помощью clang:

clang -S -emit-llvm example.c -o example.ll

и затем в ассемблер:

llc -march=x86-64 -O3 -regalloc=linear-scan -o linear_scan.s example.ll

давайте проанализируем, какой из подходов приводит к меньшему давлению на регистры.

1. **Linear Scan Register Allocation**:
   ```asm
   movl	%edi, %ecx              ; Сохраняем значение a в регистр ecx
   imull	%esi, %ecx              ; Умножаем a на b и сохраняем результат в ecx
   movl	%edx, %ebx              ; Сохраняем значение c в регистр ebx
   imull	%ecx, %ebx              ; Умножаем c на результат умножения a*b и сохраняем в ebx
   addl	%edi, %esi              ; Добавляем a к b и сохраняем результат в esi
   addl	%edx, %esi              ; Добавляем c к сумме a+b и сохраняем результат в esi
   addl	%ebx, %esi              ; Суммируем результат предыдущего умножения с результатом сложений
   movl	%esi, %eax              ; Возвращаем результат
   retq
   ```

   Здесь задействовано три регистра: `%ecx`, `%ebx` и `%esi`. Это показывает умеренное давление на регистры, поскольку регистры используются для хранения промежуточных результатов и итогового значения.

2. **Basic Register Allocation**:
   ```asm
   movl	%edi, %eax              ; Сохраняем значение a в eax
   imull	%esi, %eax              ; Умножаем a на b и сохраняем результат в eax
   movl	%edx, %ecx              ; Сохраняем значение c в ecx
   imull	%eax, %ecx              ; Умножаем c на результат умножения a*b и сохраняем в ecx
   addl	%edi, %esi              ; Добавляем a к b и сохраняем результат в esi
   addl	%edx, %esi              ; Добавляем c к сумме a+b и сохраняем результат в esi
   addl	%ecx, %esi              ; Суммируем результат предыдущего умножения с результатом сложений
   movl	%esi, %eax              ; Возвращаем результат
   retq
   ```

   Здесь задействуются всего два регистра: `%eax` и `%esi`. Это уменьшает давление на регистры по сравнению с линейным сканированием, так как используется меньшее количество регистров для той же самой работы.

3. **PBQP Register Allocation**:
   ```asm
   movl	%edi, %eax              ; Сохраняем значение a в eax
   imull	%esi, %eax              ; Умножаем a на b и сохраняем результат в eax
   movl	%edx, %ecx              ; Сохраняем значение c в ecx
   imull	%eax, %ecx              ; Умножаем c на результат умножения a*b и сохраняем в ecx
   addl	%edi, %esi              ; Добавляем a к b и сохраняем результат в esi
   addl	%edx, %esi              ; Добавляем c к сумме a+b и сохраняем результат в esi
   addl	%ecx, %esi              ; Суммируем результат предыдущего умножения с результатом сложений
   movl	%esi, %eax              ; Возвращаем результат
   retq
   ```

   Результат аналогичен базовому аллокатору: два регистра используются для всех операций. Следовательно, давление на регистры такое же низкое, как и в случае с базовым методом.
