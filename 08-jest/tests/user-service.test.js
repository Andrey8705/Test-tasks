const { fetchUser, createUser } = require('../src/user-service');

// Mock fetch
global.fetch = jest.fn();

describe('UserService', () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  describe('fetchUser', () => {
    test('should fetch user successfully', async () => {
      const mockUser = { id: 1, name: 'Alice' };
      fetch.mockResolvedValue({
        ok: true,
        json: async () => mockUser,
      });

      const user = await fetchUser(1);
      expect(user).toEqual(mockUser);
      expect(fetch).toHaveBeenCalledWith('https://api.example.com/users/1');
    });

    test('should throw error if user not found', async () => {
      fetch.mockResolvedValue({ ok: false });

      await expect(fetchUser(999)).rejects.toThrow('User not found');
    });
  });

  describe('createUser', () => {
    test('should create user', async () => {
      const newUser = { name: 'Bob', email: 'bob@example.com' };
      const createdUser = { id: 2, ...newUser };

      fetch.mockResolvedValue({
        ok: true,
        json: async () => createdUser,
      });

      const result = await createUser(newUser);
      expect(result).toEqual(createdUser);
    });
  });
});
