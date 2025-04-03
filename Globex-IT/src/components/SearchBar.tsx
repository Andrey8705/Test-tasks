import React from 'react';

interface SearchBarProps {
  searchTerm: string;
  onSearchChange: (term: string) => void;
}

const SearchBar: React.FC<SearchBarProps> = ({ searchTerm, onSearchChange }) => {
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onSearchChange(e.target.value); // Передаем новое значение в родительский компонент
  };

  return (
    <div className="mb-4">
      <input
        type="text"
        placeholder="Поиск по имени"
        value={searchTerm}
        onChange={handleInputChange}
        className="p-2 w-full border border-gray-300 rounded"
      />
    </div>
  );
};

export default SearchBar;
