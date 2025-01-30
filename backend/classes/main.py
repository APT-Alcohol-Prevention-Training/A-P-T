# main.py
from app import app

if __name__ == '__main__':
    # Flask 서버 실행
    app.run(host='0.0.0.0', port=8000)
