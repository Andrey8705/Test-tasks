describe('Math operations', () => {
  describe('Addition', () => {
    test('adds 1 + 2 to equal 3', () => {
      expect(1 + 2).toBe(3);
    });

    test('adds negative numbers', () => {
      expect(-1 + -1).toBe(-2);
    });
  });

  describe('Subtraction', () => {
    test('subtracts 5 - 2 to equal 3', () => {
      expect(5 - 2).toBe(3);
    });
  });

  describe('Multiplication', () => {
    test('multiplies 3 * 4 to equal 12', () => {
      expect(3 * 4).toBe(12);
    });
  });
});
