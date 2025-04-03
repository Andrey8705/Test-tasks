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
        value={searchTerm}
        onChange={handleSearchChange}
        className="w-[1120px] h-[48px] mb-4 p-2 border border-gray-300 rounded"
      />
      <div className="w-[357px] h-[314px] gap-[24px] rounded-[16px] p-[24px] flex flex-col items-start justify-start bg-[#F5F5F5]">
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
