// ✅ ОТФОРМАТИРОВАННЫЙ КОД - После применения Prettier

const user = {
  name: 'John',
  age: 30,
  email: 'john@example.com',
  isActive: true,
};

function calculateSum(a, b, c, d, e, f, g) {
  return a + b + c + d + e + f + g;
}

const longArray = [
  1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
];

const obj = {
  prop1: 'value1',
  prop2: 'value2',
  prop3: 'value3',
  prop4: 'value4',
  prop5: 'value5',
};

if (user.age > 18) {
  console.log('Adult');
} else {
  console.log('Minor');
}

const arrowFunc = (param) => {
  return param * 2;
};

const promise = fetch('/api/data')
  .then((response) => response.json())
  .then((data) => console.log(data))
  .catch((error) => console.error(error));

const complexObject = {
  users: [
    { id: 1, name: 'Alice', roles: ['admin', 'user'] },
    { id: 2, name: 'Bob', roles: ['user'] },
  ],
  settings: { theme: 'dark', language: 'en', notifications: true },
};
