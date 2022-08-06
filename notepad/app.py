import psycopg2
from flask import Flask, request

DB = psycopg2.connect('postgresql://postgres:postgres@db/postgres')
app = Flask('notepad')
DB_PARODY = {}


@app.route('/api/notepad', methods=['POST'])
def create_or_update_notepad():
    json_args = request.json
    name = json_args['name']
    text = json_args['text']

    sql = """
        INSERT INTO notepad (name, text)
        VALUES (%s, %s)
        ON CONFLICT (name)
        DO
            UPDATE SET text = EXCLUDED.text,
                updated_at = now()
        RETURNING id;
    """
    cur = DB.cursor()
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


@app.route('/api/notepad/<notepad_id>', methods=['GET'])
def get_notepad(notepad_id):

    sql = """
        SELECT id, name, text, updated_at FROM notepad WHERE id = %s
    """
    cur = DB.cursor()
    cur.execute(sql, (int(notepad_id),))
    row = cur.fetchone()
    cur.close()
    print(row)
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


def init_db():
    sql = """
    CREATE TABLE IF NOT EXISTS notepad (
        id SERIAL NOT NULL,
        name TEXT NOT NULL UNIQUE,
        text TEXT NOT NULL,
        updated_at TIMESTAMP DEFAULT current_timestamp
    )
    """
    cur = DB.cursor()
    cur.execute(sql)
    DB.commit()
    cur.close()


@app.route('/api/notepad/delete/<notepad_id>', methods=['GET'])
def delete_notepad(notepad_id):

    sql = """
        DELETE FROM notepad WHERE id = %s
    """
    cur = DB.cursor()
    cur.execute(sql, (int(notepad_id),))
    cur.close()
    print()
    return {}


if __name__ == '__main__':
    init_db()
    app.run(debug=False)
