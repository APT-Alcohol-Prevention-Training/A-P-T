import openai
from dotenv import load_dotenv
load_dotenv()
import os

# API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")

# 모델 목록 가져오기
models = openai.models.list()

# 모델 목록 출력
for model in models['data']:  # 모델 데이터를 반복
    print(model['id'])
