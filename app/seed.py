import asyncio
from sqlalchemy import text
from .core.database import AsyncLocalSession
from .core.security import hash_password


async def seed():
    async with AsyncLocalSession() as db:
        
        await db.execute(text("""
            INSERT INTO roles (name, description) VALUES
            ('admin', 'Полный доступ ко всем ресурсам'),
            ('moderator', 'Чтение и изменение, но не удаление'),
            ('user', 'Только чтение')
            ON CONFLICT (name) DO NOTHING;
        """))

        await db.execute(text("""
            INSERT INTO permissions (resource, action) VALUES
            ('products', 'read'),
            ('products', 'create'),
            ('products', 'update'),
            ('products', 'delete'),
            ('orders', 'read'),
            ('orders', 'create'),
            ('orders', 'update'),
            ('orders', 'delete')
            ON CONFLICT (resource, action) DO NOTHING;
        """))

        await db.execute(text("""
            INSERT INTO role_permissions (role_id, permission_id)
            SELECT r.id, p.id FROM roles r, permissions p
            WHERE r.name = 'admin'
            ON CONFLICT DO NOTHING;
        """))

        await db.execute(text("""
            INSERT INTO role_permissions (role_id, permission_id)
            SELECT r.id, p.id FROM roles r
            JOIN permissions p ON p.resource IN ('products', 'orders')
                AND p.action IN ('read', 'create', 'update')
            WHERE r.name = 'moderator'
            ON CONFLICT DO NOTHING;
        """))

        await db.execute(text("""
            INSERT INTO role_permissions (role_id, permission_id)
            SELECT r.id, p.id FROM roles r
            JOIN permissions p ON p.action = 'read'
            WHERE r.name = 'user'
            ON CONFLICT DO NOTHING;
        """))

        await db.execute(text(f"""
            INSERT INTO users (name, surname, patronymic, email, password, role_id, is_active)
            SELECT 'Иван', 'Иванов', 'Иванович', 'admin@test.com',
                '{hash_password("admin1234")}',
                (SELECT id FROM roles WHERE name = 'admin'), true
            WHERE NOT EXISTS (SELECT 1 FROM users WHERE email = 'admin@test.com');
        """))

        await db.execute(text(f"""
            INSERT INTO users (name, surname, patronymic, email, password, role_id, is_active)
            SELECT 'Пётр', 'Петров', 'Петрович', 'moderator@test.com',
                '{hash_password("moder1234")}',
                (SELECT id FROM roles WHERE name = 'moderator'), true
            WHERE NOT EXISTS (SELECT 1 FROM users WHERE email = 'moderator@test.com');
        """))

        await db.execute(text(f"""
            INSERT INTO users (name, surname, patronymic, email, password, role_id, is_active)
            SELECT 'Сергей', 'Сергеев', 'Сергеевич', 'user@test.com',
                '{hash_password("user1234")}',
                (SELECT id FROM roles WHERE name = 'user'), true
            WHERE NOT EXISTS (SELECT 1 FROM users WHERE email = 'user@test.com');
        """))

        await db.commit()
        print("База данных заполнена тестовыми данными")


if __name__ == "__main__":
    asyncio.run(seed())