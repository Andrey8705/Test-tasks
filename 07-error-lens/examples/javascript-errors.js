// ❌ Примеры ошибок, которые подсветит Error Lens

// Синтаксическая ошибка
const x = ; // ❌ Error: Unexpected token ;

// Неиспользуемая переменная
const unusedVar = 42; // ⚠️ Warning: 'unusedVar' is declared but never used

// Неопределённая переменная
console.log(undefinedVar); // ❌ Error: 'undefinedVar' is not defined

// Нестрогое сравнение
if (x == 5) { } // ⚠️ Warning: Use '===' instead of '=='

// Отсутствующий return
function getValue() {
  const value = 42;
  // ⚠️ Warning: Function declared as returning value but has no return statement
}

// console.log в коде
console.log('Debug message'); // ⚠️ Warning: Unexpected console statement
