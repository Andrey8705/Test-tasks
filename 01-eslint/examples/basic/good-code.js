// ✅ ХОРОШИЙ КОД - Исправленная версия после применения ESLint

// Исправление 1: Использование const/let вместо var
const userName = 'John';
let age = 25;

// Исправление 2: Удалена неиспользуемая переменная

// Исправление 3: Удалён console.log (или оставлен с предупреждением)

// Исправление 4: Использование === для строгого сравнения
function checkAge(userAge) {
  if (userAge === 18) {
    return 'Adult';
  }
  return 'Not adult';
}

// Исправление 5: const для переменных, которые не переназначаются
const PI = 3.14159;

// Исправление 6: Точка с запятой добавлена
const greeting = 'Hello, World!';

// Исправление 7: Одинарные кавычки
const message = 'This uses single quotes';

// Исправление 8: Без trailing запятых
const colors = [
  'red',
  'green',
  'blue'
];

// Исправление 9: Правильные отступы (2 пробела)
function goodIndentation() {
  const x = 1;
  const y = 2;
  const z = 3;
  return x + y + z;
}

// Исправление 10: Пробелы вокруг стрелки
const multiply = (a, b) => a * b;

// Исправление 11: Максимум 1 пустая строка
const example = 'proper empty lines';

// Исправление 12: Пробел перед блоком
function withSpace() {
  return true;
}

// Исправление 13: Без пробелов внутри скобок
const sum = (1 + 2);

// Исправление 14: Пробелы вокруг операторов
const result = 10 + 20;

// Исправление 15: debugger удалён

// Экспорт
module.exports = {
  userName,
  checkAge,
  PI,
  greeting,
  colors,
  multiply,
  goodIndentation
};
