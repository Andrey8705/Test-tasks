// ❌ ПЛОХОЙ КОД - Примеры распространённых ошибок, которые найдёт ESLint

// Ошибка 1: Использование var вместо const/let
var userName = 'John';
var age = 25;

// Ошибка 2: Неиспользуемая переменная
var unusedVariable = 'This is never used';

// Ошибка 3: console.log в коде
console.log('Debug message');

// Ошибка 4: Использование == вместо ===
function checkAge(userAge) {
  if (userAge == 18) {  // Нестрогое сравнение
    console.log('Adult');
  }
}

// Ошибка 5: Переменная, которую можно сделать const
let PI = 3.14159;  // Никогда не переназначается

// Ошибка 6: Отсутствие точки с запятой
const greeting = 'Hello, World!'

// Ошибка 7: Двойные кавычки вместо одинарных
const message = "This should use single quotes";

// Ошибка 8: Лишние trailing запятые
const colors = [
  'red',
  'green',
  'blue',
];

// Ошибка 9: Неправильные отступы
function badIndentation() {
   const x = 1;
  const y = 2; // Несогласованные отступы
    const z = 3;
}

// Ошибка 10: Отсутствие пробелов вокруг стрелки
const multiply=(a,b)=>a*b;

// Ошибка 11: Множественные пустые строки



const example = 'too many empty lines above';

// Ошибка 12: Нет пробела перед блоком
function noSpace(){
  return true;
}

// Ошибка 13: Пробелы внутри скобок
const sum = ( 1 + 2 );

// Ошибка 14: Нет пробелов вокруг операторов
const result=10+20;

// Ошибка 15: debugger в коде
debugger;

// Экспорт для примера
module.exports = { userName, checkAge, PI };
