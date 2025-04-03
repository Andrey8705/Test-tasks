import React, { useState, useEffect } from 'react';

interface User {
  id: number;
  name: string;
  email: string;
}

const UserList: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]); // Состояние списка пользователей
  const [searchTerm, setSearchTerm] = useState<string>(''); // Состояние строки поиска
  const [filteredUsers, setFilteredUsers] = useState<User[]>([]); // Состояние отфильтрованных пользователей

  // Отправляю запрос на бэкенд, получаю список пользователей
  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await fetch('http://127.0.0.1:3000');
        const data = await response.json();
        setUsers(data); // Сохраняем пользователей в состояние
        setFilteredUsers(data); // По дефолту отображаем всех пользователей
      } catch (error) {
        console.error('Ошибка при получении пользователей:', error); 
      }
    };

    fetchUsers();
  }, []);

  // Фильтрую пользователей по строке поиска
  useEffect(() => {
    if (searchTerm) {
      const filtered = users.filter(user =>
        user.name.toLowerCase().includes(searchTerm.toLowerCase())
      );
      setFilteredUsers(filtered);
    } else {
      setFilteredUsers(users); // Если строка поиска пустая, вывожу всех пользователей
    }
  }, [searchTerm, users]);

  // Обработчик изменения строки поиска
  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
  };

  return (
    <div>
      <input
        type="text"
        placeholder="Поиск по имени"
        value={searchTerm}
        onChange={handleSearchChange}
        className="mb-4 p-2 border border-gray-300 rounded"
      />
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {filteredUsers.map(user => (
          <div key={user.id} className="border p-4 rounded shadow-md">
            <h3 className="text-lg font-semibold">{user.name}</h3>
            <p>{user.email}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default UserList;
