"""Демонстрация Indent Rainbow для Python с глубокой вложенностью."""

def process_data(data):
    """Обработка данных с множественными уровнями вложенности."""
    for item in data:
        if item['active']:
            if item['type'] == 'user':
                for role in item['roles']:
                    if role == 'admin':
                        for permission in item['permissions']:
                            if permission == 'write':
                                print(f"User {item['name']} has write access")
                            else:
                                print(f"Permission: {permission}")
                    else:
                        print(f"Role: {role}")
            else:
                print(f"Type: {item['type']}")
        else:
            print("Inactive item")

class NestedExample:
    """Класс с вложенными методами."""

    def level_one(self):
        """Уровень 1."""
        if True:
            def level_two():
                """Уровень 2."""
                if True:
                    def level_three():
                        """Уровень 3."""
                        if True:
                            print("Deep nesting!")
                    level_three()
            level_two()
