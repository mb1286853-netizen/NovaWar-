import aiosqlite
import json

DB_NAME = "data/zone.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.executescript('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                zp INTEGER DEFAULT 10000,
                gem INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,
                exp INTEGER DEFAULT 0,
                power INTEGER DEFAULT 100,
                miner_level INTEGER DEFAULT 1,
                miner_claim INTEGER DEFAULT 0,
                last_free_box INTEGER DEFAULT 0,
                fighters TEXT DEFAULT '{}',
                drones TEXT DEFAULT '{}',
                missiles TEXT DEFAULT '{}',
                defenses TEXT DEFAULT '{}',
                league TEXT DEFAULT 'مبتدی'
            );
        ''')
        await db.commit()

async def get_user(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            if not row:
                return None
            keys = [d[0] for d in cursor.description]
            user = dict(zip(keys, row))
            for k in ['fighters','drones','missiles','defenses']:
                user[k] = json.loads(user[k]) if user[k] else {}
            return user['last_free_box'] = user['last_free_box'] or 0
            return user

async def create_user(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
        await db.commit()

async def update_user(user_id, **kwargs):
    async with aiosqlite.connect(DB_NAME) as db:
        sets, values = [], []
        for k, v in kwargs.items():
            sets.append(f"{k}=?")
            values.append(json.dumps(v, ensure_ascii=False) if isinstance(v, (dict,list)) else v)
        values.append(user_id)
        await db.execute(f"UPDATE users SET {', '.join(sets)} WHERE user_id=?", values)
        await db.commit()
