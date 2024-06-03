from datetime import datetime
import sqlite3


# FUNCION PARA AGREGAR USUARIOS A LA DB CUANDO SE UNEN A DISCORD
async def agregarusuario(username, user_id):
    FechaActual = datetime.now()

    # Conecta a la base y trae los usuarios
    databaseusers = sqlite3.connect('db/discordusrs.db')
    cursor = databaseusers.cursor()

    try:
        cursor.execute("INSERT INTO usuarios (username, user_id, karma, karmagiven) VALUES (?, ?, 0, 0)", (username, user_id))

        # Log
        print(FechaActual)
        print("USER DB FUNCTION: Nuevo ususario agregado")

    except sqlite3.IntegrityError:
        print(FechaActual)
        print("USER DB FUNCITON: Error. Usuario ya existe en la base")
        
    databaseusers.commit()
    databaseusers.close()


# FUNCION ONE TIME ONLY PARA AGREGAR A TODOS LOS USUARIOS A LA DB CUANDIO INICIA EL BOT
async def sincronizarUsuarios(all_members):
    FechaActual = datetime.now()
    databaseusers = sqlite3.connect('db/discordusrs.db')
    cursor = databaseusers.cursor()
    for member in all_members:
        try:
            cursor.execute("INSERT INTO usuarios (username, user_id, karma, karmagiven) VALUES (?, ?, 0, 0)", (member.name, member.id))

            # Log
            with open('db/dblog.txt', "a") as f:
                f.write(f"{FechaActual} - USER DB FUNCTION: Nuevo ususario agregado {member.name} - {member.id} \n")

        except sqlite3.IntegrityError:
            with open('db/dblog.txt', "a") as f:
                f.write(f"{FechaActual} - USER DB FUNCITON: Error. Usuario ya existe en la base \n")

    databaseusers.commit()
    databaseusers.close()