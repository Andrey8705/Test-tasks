module.exports = {
  // Окружение тестирования
  testEnvironment: 'node',

  // Паттерн для поиска тестов
  testMatch: ['**/tests/**/*.test.js'],

  // Coverage
  collectCoverage: false,
  coverageDirectory: 'coverage',
  collectCoverageFrom: [
    'src/**/*.js',
    '!src/**/*.test.js',
  ],

  // Подробный вывод
  verbose: true,

  // Очистка моков между тестами
  clearMocks: true,

  // Таймаут для тестов
  testTimeout: 5000,
};
