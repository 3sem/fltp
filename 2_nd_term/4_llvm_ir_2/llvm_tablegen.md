**TableGen** — это декларативный язык описания данных и генератор кода, используемый в LLVM для автоматизации создания частей компилятора, особенно связанных с целевыми архитектурами (инструкции, регистры, расписания). Рассмотрим его детально:

---

### 1. **Назначение TableGen**
- Генерация **машинно-зависимых** частей компилятора:
  - Наборы инструкций (ISA)
  - Регистры процессора
  - Параметры планирования (latency, throughput)
  - ABI-правила
- Преобразует декларативные описания в **C++ код** (через утилиту `llvm-tblgen`).

---

### 2. **Синтаксис и грамматика**
TableGen использует **декларативный стиль** с элементами ООП.

#### Базовые конструкции:
```tablegen
// 1. Классы (абстрактные шаблоны)
class Instruction {
  string AsmString = "";
  list<dag> Pattern = [];
}

// 2. Определения (конкретные сущности)
def ADD : Instruction {
  let AsmString = "add $dst, $src1, $src2";
  let Pattern = [(set GR32:$dst, (add GR32:$src1, GR32:$src2))];
}

// 3. Мультиклассы (группы определений)
multiclass LogicOps<string opcode> {
  def _"rr" : Instruction<...>;
  def _"ri" : Instruction<...>;
}

// 4. Наследование
class BinaryInst : Instruction {
  bits<4> opcode;
  dag operands;
}
```

#### Типы данных:
| Тип          | Пример                     |
|--------------|---------------------------|
| `bit`        | `bits<5> opcode = 0b10101`|
| `int`        | `int Latency = 3`         |
| `string`     | `string Asm = "mov"`      |
| `list`       | `list<Register> Regs`     |
| `dag`        | `(add R0, R1)`           |

---

### 3. **Как генерируется код**
Процесс включает 3 этапа:

#### 1) Описание целевой архитектуры
```tablegen
// ARM.td
def ARM : Target {
  let InstructionSet = ARMInsts;
  let Registers = [R0, R1, R2, ...];
}

def R0 : Register<"r0"> { let Encoding = 0b000; }
```

#### 2) Генерация C++ кода
Запуск утилиты:
```bash
llvm-tblgen -gen-instr-info ARM.td -o ARMGenInstrInfo.inc
```

#### 3) Интеграция в LLVM
Сгенерированный файл `ARMGenInstrInfo.inc` включается в:
```cpp
// ARMInstrInfo.cpp
#include "ARMGenInstrInfo.inc"

void ARMInstrInfo::anchor() {} 
```

---

### 4. **Пример: Генерация инструкции**
#### Исходное описание:
```tablegen
class AddI<bits<4> op, string asm> : Instruction {
  bits<4> opcode = op;
  string AsmString = asm;
  let Pattern = [(set GR32:$dst, (add GR32:$src1, GR32:$src2))];
}

def ADD : AddI<0b1000, "add $dst, $src1, $src2">;
```

#### Сгенерированный код (фрагмент):
```cpp
// ARMGenInstrInfo.inc
const MCInstrDesc ARMInsts[] = {
  { 0b1000, "add", 0, 3, ... }
};
```

---

### 5. **Ключевые операторы**
| Оператор      | Пример                     | Значение                     |
|---------------|----------------------------|------------------------------|
| `let`         | `let isReturn = 1;`        | Переопределение поля         |
| `def`         | `def SUB : Instruction;`   | Создание экземпляра          |
| `multiclass`  | `multiclass LogicOps<...>` | Группа определений           |
| `foreach`     | `foreach i = 0-3 in ...`   | Генерация вариантов          |
| `dag`         | `(set R0, (add R1, R2))`   | Дерево операций              |

---

### 6. **Реальный пример из LLVM**
#### Описание регистров x86:
```tablegen
def AL : X86Reg<"al", 0, [RAX]> { let SubRegIndices = [sub_8bit]; }
def AH : X86Reg<"ah", 4, [RAX]> { let SubRegIndices = [sub_8h]; }
```

#### Генерирует:
- Таблицы регистров
- Методы доступа в `X86RegisterInfo.cpp`
- Данные для анализатора ассемблера

---

### 7. **Как работает сопоставление инструкций**
TableGen преобразует DAG-паттерны в **автомат**:
```tablegen
def : Pat<(add GR32:$src1, 0), (MOV32rr $src1)>;
```
Эта запись создает:
1. Код для сопоставления IR-узла `add` с нулём
2. Генерацию `MOV` вместо `ADD`

---

### 8. **Ограничения TableGen**
- **Нет Тьюринг-полноты**: Нельзя писать произвольную логику
- **Строгая типизация**: Ошибки в типах обнаруживаются на этапе генерации
- **Отладка**: Сложно трассировать преобразования

---

### 9. **Инструменты для работы**
1. **Просмотр вывода**:
   ```bash
   llvm-tblgen -print-records ARM.td
   ```
2. **Генерация документации**:
   ```bash
   llvm-tblgen -gen-asm-doc -o ARMAsmDocs.txt
   ```

---

### Итог
TableGen — это **DSL для описания машинно-зависимых данных** LLVM, который:
- Использует **декларативную грамматику** с классами и мультиклассами
- Генерирует **таблицы и C++ код** через шаблоны
- Позволяет **однократно описать** ISA и автоматизировать поддержку новых архитектур

Пример полного цикла для новой инструкции:
```tablegen
// 1. Описание
class VEXT<bits<4> op, string asm> : SIMDInst {
  let Opcode = op;
  let AsmString = asm;
}

// 2. Генерация
def VEXTq16 : VEXT<0b1010, "vext $dst, $src1, $src2, $imm">;

// 3. Использование в коде
// В ARMAsmParser.cpp:
case ARM::VEXTq16: emitVEXTInstruction(...); break;
```
