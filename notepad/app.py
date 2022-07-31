from flask import Flask, request

DB_PARODY = {}

app = Flask('notepad')


@app.route('/api/notepad', methods=['POST'])
def create_or_update_notepad():
    json_args = request.json
    name = json_args['name']
    text = json_args['text']

    created = True
    if name in DB_PARODY:
        created = False

    DB_PARODY[name] = text
    return {
        'name': name,
        'text': text,
        'status': 'created' if created else 'updated'
    }


@app.route('/api/notepad/<name>', methods=['GET'])
def get_notepad(name):
    if name not in DB_PARODY:
        return {
            'error': 'Not found',
        }, 404

    return {
        'name': name,
        'text': DB_PARODY[name],
    }


if __name__ == '__main__':
    app.run(debug=True)
