from flask import Flask, render_template, request, jsonify
import sys
import io
import contextlib

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run_code():
    data = request.get_json()
    code = data.get("code", "")
    user_input = data.get("input", "")
    
    input_stream = io.StringIO(user_input)
    output_stream = io.StringIO()

    try:
        with contextlib.redirect_stdout(output_stream), contextlib.redirect_stderr(output_stream):
            sys.stdin = input_stream
            exec(code, {})
    except Exception as e:
        output_stream.write(str(e))
    finally:
        sys.stdin = sys.__stdin__  # Reset stdin

    return jsonify({"output": output_stream.getvalue()})

if __name__ == '__main__':
    app.run(debug=True)
