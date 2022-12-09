
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import config
import sqlite3

connect = sqlite3.connect('users.db')
cur  = connect.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users(
    username VARCHAR(255),
    id INTEGER,
    chat_id INTEGER
    );
    """)
connect.commit()

connect_admin = sqlite3.connect('admin.db')
curr  = connect_admin.cursor()
curr.execute("""CREATE TABLE IF NOT EXISTS admin(
    id INTEGER
    );
    """)
connect_admin.commit()

bot = Bot(config.token)
dp = Dispatcher(bot, storage=MemoryStorage())



@dp.message_handler(commands=["start"])
async def start(message : types.Message):
    cur  = connect.cursor()
    cur.execute(f"SELECT id FROM users WHERE  id  == {message.from_user.id};")
    result = cur.fetchall()
    if result ==[]:
        cur.execute(f"INSERT INTO users VALUES ('{message.from_user.username}', {message.from_user.id}, {message.chat.id});")
    connect.commit()
    await message.answer(f"Салам,{message.from_user.full_name} .Менин атым умар.\nМен жөнүндө көбүрөөк билгиңиз келсе, басыңыз: /help ")


@dp.message_handler(commands=["users"])
async def start(message : types.Message):
    cur  = connect.cursor()
    cur.execute("SELECT * FROM users;")
    res = cur.fetchall()

    cur1  = connect_admin.cursor()
    cur1.execute("SELECT * FROM admin;")

    result = cur1.fetchall()
    for user in result:
        if message.from_user.id in user:
            if res !=[]:
                await message.answer(res)
            else:
                await message.answer("тизме бош")
        else:
            await message.answer("Сиздин укугуңуз жок")

class AdminState(StatesGroup):
    admin = State()

@dp.message_handler(commands=["add_admin"])
async def start(message : types.Message):
    cur1  = connect_admin.cursor()
    cur1.execute("SELECT * FROM admin;")
    result = cur1.fetchall()
    for user in result:
        
        if message.from_user.id in user:
            
            await message.answer('Кириңиз id админ: ')
            await AdminState.admin.set()
    else:
        await message.answer("Сиздин укугуңуз жок....")
        
@dp.message_handler(state=AdminState.admin)
async def admin_add(message : types.Message,):
    cur_admin  = connect_admin.cursor()
    res = message.text.split()
    
    cur_admin = cur_admin.execute(f"INSERT INTO admin (id) VALUES ('{res[0]}');")
    connect_admin.commit()
    

executor.start_polling(dp)