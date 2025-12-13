// TypeScript пример с ESLint (@typescript-eslint)
// Для использования нужно добавить в .eslintrc.json:
// {
//   "parser": "@typescript-eslint/parser",
//   "plugins": ["@typescript-eslint"],
//   "extends": ["plugin:@typescript-eslint/recommended"]
// }

// ✅ Правильное использование типов
interface User {
  id: number;
  name: string;
  email: string;
  role: 'admin' | 'user' | 'guest';
}

// ✅ Типизированная функция
function getUserById(id: number): User | null {
  const users: User[] = [
    { id: 1, name: 'Alice', email: 'alice@example.com', role: 'admin' },
    { id: 2, name: 'Bob', email: 'bob@example.com', role: 'user' }
  ];

  return users.find(user => user.id === id) || null;
}

// ✅ Generic функция
function firstElement<T>(arr: T[]): T | undefined {
  return arr[0];
}

// ✅ Type guards
function isAdmin(user: User): user is User & { role: 'admin' } {
  return user.role === 'admin';
}

// ✅ Enum вместо magic strings
enum UserRole {
  Admin = 'admin',
  User = 'user',
  Guest = 'guest'
}

// ✅ Использование readonly
interface Config {
  readonly apiUrl: string;
  readonly timeout: number;
}

const config: Config = {
  apiUrl: 'https://api.example.com',
  timeout: 5000
};

// ✅ Async/await с правильными типами
async function fetchUser(id: number): Promise<User | null> {
  try {
    const response = await fetch(`/api/users/${id}`);
    const data: User = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching user:', error);
    return null;
  }
}

// ✅ Class с типизацией
class UserService {
  private users: User[] = [];

  addUser(user: User): void {
    this.users.push(user);
  }

  getUser(id: number): User | undefined {
    return this.users.find(u => u.id === id);
  }

  getAllAdmins(): User[] {
    return this.users.filter(isAdmin);
  }
}

// Экспорт
export { User, getUserById, firstElement, UserRole, UserService };
