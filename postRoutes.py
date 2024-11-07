from flask import Blueprint, request, session, jsonify
import pyodbc

routesbp = Blueprint('rutas', __name__)

server = '(localdb)\\MainServer'  
database = 'RegChat'

conn_str = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

# USER ROUTES ----------

@routesbp.route("/register-new-user", methods=['POST'])
def registerN():
    Nusername = request.form['username']
    Npassword = request.form['password']

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute(f"INSERT into users values(\'{Nusername}\', \'{Npassword}\')")
        cursor.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        return str(e)

    return jsonify({'message' : 'registered'})

@routesbp.route("/log-in-account", methods=['POST'])
def loginAc():
    username = request.form['username']
    password = request.form['password']

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * from users where username=\'{username}\' and passw=\'{password}\'")
        returnedUser = cursor.fetchall()
        cursor.close()
        conn.close()
        
        if returnedUser:
            session['username'] = returnedUser[0][1]
            session['pwrd'] = returnedUser[0][2]
            session['id'] = returnedUser[0][0]
        else:
            return jsonify({'message' : 'wrongCred'})
    except Exception as e:
        return str(e)
    print(session)
    return jsonify({'message' : 'logged'})

@routesbp.route('/create-new-chat', methods=['POST'])
def Cchat():
    name = request.form['chatname']
    user1 = request.form['id_memb']
    user2 = session['id']

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO chatroom values(\'{name}\')")
        cursor.commit()
        cursor.execute("select max(id_chat) from chatroom")
        MaxID = cursor.fetchall()
        MaxID = MaxID[0][0]
        cursor.execute(f"INSERT into membersCR values({int(user1)}, {int(MaxID)}, \'member\')")
        cursor.commit()
        cursor.execute(f"INSERT INTO membersCR values({int(user2)}, {int(MaxID)}, \'member\')")
        cursor.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        return str(e)
    return jsonify({'message' : 'chat created'})