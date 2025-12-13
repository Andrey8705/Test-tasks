// React компонент с ESLint правилами (eslint-plugin-react)
// Для использования нужно добавить в .eslintrc.json:
// {
//   "extends": ["plugin:react/recommended", "plugin:react-hooks/recommended"],
//   "plugins": ["react", "react-hooks"]
// }

import React, { useState, useEffect, useCallback } from 'react';
import PropTypes from 'prop-types';

// ✅ Правильный функциональный компонент
function UserCard({ user, onUpdate }) {
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    name: user.name,
    email: user.email
  });

  // ✅ useEffect с зависимостями
  useEffect(() => {
    console.log('User changed:', user.id);
    setFormData({
      name: user.name,
      email: user.email
    });
  }, [user.id, user.name, user.email]);

  // ✅ useCallback для оптимизации
  const handleSubmit = useCallback((e) => {
    e.preventDefault();
    onUpdate(user.id, formData);
    setIsEditing(false);
  }, [user.id, formData, onUpdate]);

  // ✅ Обработчик события
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  // ✅ Условный рендеринг
  if (isEditing) {
    return (
      <form onSubmit={handleSubmit} className="user-card">
        <input
          type="text"
          name="name"
          value={formData.name}
          onChange={handleChange}
          required
        />
        <input
          type="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          required
        />
        <button type="submit">Save</button>
        <button type="button" onClick={() => setIsEditing(false)}>
          Cancel
        </button>
      </form>
    );
  }

  return (
    <div className="user-card">
      <h3>{user.name}</h3>
      <p>{user.email}</p>
      <button onClick={() => setIsEditing(true)}>Edit</button>
    </div>
  );
}

// ✅ PropTypes для валидации пропсов
UserCard.propTypes = {
  user: PropTypes.shape({
    id: PropTypes.number.isRequired,
    name: PropTypes.string.isRequired,
    email: PropTypes.string.isRequired
  }).isRequired,
  onUpdate: PropTypes.func.isRequired
};

// ✅ Компонент-список с key
function UserList({ users, onUpdateUser }) {
  return (
    <div className="user-list">
      {users.map(user => (
        <UserCard
          key={user.id}
          user={user}
          onUpdate={onUpdateUser}
        />
      ))}
    </div>
  );
}

UserList.propTypes = {
  users: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number.isRequired,
      name: PropTypes.string.isRequired,
      email: PropTypes.string.isRequired
    })
  ).isRequired,
  onUpdateUser: PropTypes.func.isRequired
};

export { UserCard, UserList };
