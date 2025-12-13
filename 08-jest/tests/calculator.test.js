const { add, subtract, multiply, divide } = require('../src/calculator');

describe('Calculator', () => {
  describe('add', () => {
    test('should add two positive numbers', () => {
      expect(add(2, 3)).toBe(5);
    });

    test('should add negative numbers', () => {
      expect(add(-1, -1)).toBe(-2);
    });
  });

  describe('subtract', () => {
    test('should subtract two numbers', () => {
      expect(subtract(5, 3)).toBe(2);
    });
  });

  describe('multiply', () => {
    test('should multiply two numbers', () => {
      expect(multiply(3, 4)).toBe(12);
    });
  });

  describe('divide', () => {
    test('should divide two numbers', () => {
      expect(divide(10, 2)).toBe(5);
    });

    test('should throw error when dividing by zero', () => {
      expect(() => divide(10, 0)).toThrow('Division by zero');
    });
  });
});
