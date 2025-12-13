// Файл с историей коммитов для демонстрации GitLens
// Попробуйте:
// 1. Наведите курсор на строку - увидите автора и дату
// 2. Нажмите на аннотацию GitLens - откроется история
// 3. Ctrl+Shift+P → "GitLens: Show File History"

function calculateTotal(items) {
  // Эта строка добавлена в первом коммите
  let total = 0;

  // Эта строка изменена во втором коммите
  for (const item of items) {
    total += item.price * item.quantity;
  }

  // Эта строка добавлена в третьем коммите
  return total;
}

// Новая функция из четвёртого коммита
function applyDiscount(total, discount) {
  return total * (1 - discount / 100);
}

module.exports = { calculateTotal, applyDiscount };
