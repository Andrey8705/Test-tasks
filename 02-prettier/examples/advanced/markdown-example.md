# Демонстрация Prettier для Markdown

## Форматирование таблиц

| Название   | Описание                  | Статус |
| ---------- | ------------------------- | ------ |
| Prettier   | Форматировщик кода        | ✅     |
| ESLint     | Линтер для JavaScript     | ✅     |
| TypeScript | Типизированный JavaScript | ✅     |

## Списки

- Первый элемент
- Второй элемент
  - Вложенный элемент 1
  - Вложенный элемент 2
- Третий элемент

1. Нумерованный список
2. Второй пункт
3. Третий пункт

## Код

```javascript
const formatCode = (code) => {
  return prettier.format(code, {
    parser: 'babel',
    semi: true,
    singleQuote: true,
  });
};
```

## Ссылки

[Prettier Documentation](https://prettier.io/docs/en/index.html)
