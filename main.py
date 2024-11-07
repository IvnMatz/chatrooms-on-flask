from flask import Flask, render_template, session, redirect, url_for
from flask_socketio import SocketIO, send
import pyodbc
from postRoutes import routesbp

app = Flask(__name__)
socketio = SocketIO(app)
app.register_blueprint(routesbp)
app.secret_key = "NobodyPrayForMe"

server = '(localdb)\\MainServer'  
database = 'RegChat'

conn_str = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

# ROUTES --------

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for("login"))
    else:
        return redirect(url_for("chatrooms"))

#LOGIN AND REGISTER ROUTES --------------------------

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('pwrd', None)
    session.pop('id', None)
    session.pop('color', None)
    return redirect(url_for('index'))

#CHAT ROUTES -----------------------------------------

@app.route('/chatrooms')
def chatrooms():
    if 'username' not in session:
        return redirect(url_for("login"))
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute(f"select chatroom.* from chatroom join membersCR on membersCR.id_chat=chatroom.id_chat where membersCR.id_user={session['id']}")
        returnedChats = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        return str(e)

    return render_template('chatroom.html', chats=returnedChats, user=session)

@app.route('/chat/<chat_id>')
def chat(chat_id):
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * from membersCR where id_user={int(session['id'])} and id_chat={int(chat_id)}")
        ifexists = cursor.fetchall()
        if ifexists == False:
            cursor.close()
            conn.close()
            return redirect('index')
        cursor.execute(f"SELECT chatname from chatroom where id_chat = {int(chat_id)}")
        chatname = cursor.fetchall()
        chatname = chatname[0][0]
    except Exception as e:
        return str(e)
    return render_template('chat.html', chatname=chatname, chatid=chat_id)

@socketio.on('message')
def handle_message(msg):
    print(f'Message received: {msg}')
    message = {
        'username' : session['username'],
        'message' : str(msg.get("msg")),
        'channel' : int(msg.get("channel")),
        'colorU' : session['color']
    }
    send(message, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)