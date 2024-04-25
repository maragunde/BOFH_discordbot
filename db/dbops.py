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