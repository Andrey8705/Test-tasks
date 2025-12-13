// Демонстрация Indent Rainbow для JavaScript

function processUsers(users) {
  users.forEach(user => {
    if (user.active) {
      if (user.role === 'admin') {
        user.permissions.forEach(permission => {
          if (permission.type === 'write') {
            permission.resources.forEach(resource => {
              console.log(`${user.name} can write to ${resource}`);
            });
          }
        });
      }
    }
  });
}

// Глубокая вложенность с promises
fetch('/api/users')
  .then(response => {
    if (response.ok) {
      return response.json();
    } else {
      throw new Error('Failed to fetch');
    }
  })
  .then(data => {
    data.forEach(user => {
      if (user.active) {
        console.log(user.name);
      }
    });
  })
  .catch(error => {
    console.error(error);
  });
