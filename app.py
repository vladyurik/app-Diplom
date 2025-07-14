from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None

    if request.method == 'POST':
        try:
            a = float(request.form.get('a'))
            b = float(request.form.get('b'))
            op = request.form.get('op')

            if op == 'add':
                result = a + b
            elif op == 'sub':
                result = a - b
            elif op == 'mul':
                result = a * b
            elif op == 'div':
                if b == 0:
                    error = 'Деление на ноль невозможно'
                else:
                    result = a / b
            else:
                error = 'Неизвестная операция'

        except Exception as e:
            error = f'Ошибка: {str(e)}'

    return render_template('index.html', result=result, error=error)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
