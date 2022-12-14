import jwt
import psycopg2
from flask import Flask, request

DB = psycopg2.connect('postgresql://postgres:postgres@db/postgres')
app = Flask('notepad')


KEY_FOR_JWT = 'IncursoIncursoIncurso'


def jwt_validation(user_jwt):
    # Function to validate JWT
    user_id = jwt.decode(user_jwt, KEY_FOR_JWT, algorithms=["HS256"])
    key_user_id = list(user_id.keys())[0]
    cur = DB.cursor()

    sql = """
        SELECT id FROM users WHERE id = %s;
    """
    cur.execute(sql, (key_user_id,))
    row = cur.fetchone()

    if row[0] is None:
        return True
    else:
        return False


@app.route('/api/notepad/registration', methods=['POST'])
def registration_of_a_new_user():
    # Recieves login and password to registrate a new user
    json_args = request.json
    login = json_args['login']
    password = json_args['password']

    sql = """
        SELECT date_of_creation FROM users WHERE login = %s;
    """
    cur = DB.cursor()
    cur.execute(sql, (login,))
    row = cur.fetchone()

    if row is None:
        sql = """
            INSERT INTO users (login, password)
            VALUES (%s, %s)
            ON CONFLICT (login)
            DO NOTHING;
        """
        cur.execute(sql, (login, password))
        DB.commit()
        cur.close()
        return {
            'status': 'successefully registered',
            'login': login,
        }
    else:
        cur.close()
        return {
            'status': 'login is alredy taken',
        }


@app.route('/api/notepad/login', methods=['POST'])
def login():
    # Login page. Recieves password and login
    # Returns JWT
    json_args = request.json
    login = json_args['login']
    password = json_args['password']

    sql = """
        SELECT id FROM users WHERE login = %s AND password = %s;
    """
    cur = DB.cursor()
    cur.execute(sql, (login, password,))
    row = cur.fetchone()
    cur.close()

    if row is None:

        return {
            'status': 'wrong login or password',
        }
    else:

        generated_jwt = jwt.encode(
            {row[0]: password}, KEY_FOR_JWT, algorithm='HS256')

        return {
            'jwt': generated_jwt,
        }


@ app.route('/api/notepad', methods=['POST'])
def create_or_update_notepad():
    # Notepad redaction page
    json_args = request.json
    name = json_args['name']
    text = json_args['text']
    jwt = json_args['jwt']

    if jwt_validation(jwt) is True:
        return {
            'status': 'Forbidden'
        }, 403

    cur = DB.cursor()

    sql = """
        INSERT INTO notepad (name, text)
        VALUES (%s, %s)
        ON CONFLICT (name)
        DO
            UPDATE SET text = EXCLUDED.text,
                updated_at = now()
        RETURNING id;
    """

    cur.execute(sql, (name, text))
    row_id = cur.fetchone()[0]
    sql = """
        SELECT id, name, text, updated_at FROM notepad WHERE id = %s
    """
    cur.execute(sql, (row_id,))
    DB.commit()
    row = cur.fetchone()
    cur.close()

    return {
        'id': row[0],
        'name': row[1],
        'text': row[2],
        'updated_at': row[3],
    }


@ app.route('/api/notepad/<notepad_id>', methods=['GET'])
def get_notepad(notepad_id):

    json_args = request.json
    jwt = json_args['jwt']

    if jwt_validation(jwt) is True:
        return {
            'status': 'Forbidden'
        }, 403

    sql = """
        SELECT id, name, text, updated_at FROM notepad WHERE id = %s
    """
    cur = DB.cursor()
    cur.execute(sql, (int(notepad_id),))
    row = cur.fetchone()
    cur.close()

    if row:
        return {
            'id': row[0],
            'name': row[1],
            'text': row[2],
            'updated_at': row[3],
        }

    return {
        'error': 'Not found',
    }, 404


@app.route('/api/notepad/delete/<notepad_id>', methods=['POST'])
def delete_notepad(notepad_id):
    # Recieves id and then deletes the note from DB with that id
    print('at least we got here')
    json_args = request.json

    print('at least we got here')
    jwt = json_args['jwt']

    if jwt_validation(jwt) is True:
        return {
            'status': 'Forbidden'
        }, 403

    print('at least we got here3', notepad_id)

    sql = """
        DELETE FROM notepad WHERE id = %s
    """
    cur = DB.cursor()
    cur.execute(sql, (int(notepad_id),))
    cur.close()
    print()
    return {}


def init_db():
    cur = DB.cursor()

    # sql = """ DROP TABLE users CASCADE"""

    sql = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL NOT NULL PRIMARY KEY,
        login TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        date_of_creation TIMESTAMP DEFAULT current_timestamp
    )
    """

    cur.execute(sql)

    # sql = """ DROP TABLE notepad"""

    sql = """
    CREATE TABLE IF NOT EXISTS notepad (
        id SERIAL NOT NULL,
        name TEXT NOT NULL UNIQUE,
        text TEXT NOT NULL,
        updated_at TIMESTAMP DEFAULT current_timestamp,
        author TEXT REFERENCES users (login)
    )
    """
    cur.execute(sql)
    DB.commit()
    cur.close()


if __name__ == '__main__':
    init_db()
    app.run(debug=False)
