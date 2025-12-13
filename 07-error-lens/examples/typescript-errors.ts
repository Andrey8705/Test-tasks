// ❌ Примеры ошибок TypeScript, которые подсветит Error Lens

// Ошибка типа
const num: number = "string"; // ❌ Type 'string' is not assignable to type 'number'

// Отсутствующее свойство
interface User {
  name: string;
  email: string;
}

const user: User = {
  name: "Alice"
  // ❌ Property 'email' is missing
};

// Неправильный тип аргумента
function greet(name: string): string {
  return `Hello, ${name}`;
}

greet(123); // ❌ Argument of type 'number' is not assignable to parameter of type 'string'

// Неопределённое свойство
const obj = { foo: "bar" };
console.log(obj.baz); // ❌ Property 'baz' does not exist on type '{ foo: string }'

// Nullable ошибки
function getValue(): string | null {
  return null;
}

const result = getValue();
console.log(result.toUpperCase()); // ❌ Object is possibly 'null'
