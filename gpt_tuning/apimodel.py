import openai
from dotenv import load_dotenv
import os

load_dotenv()

# API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")

# 모델 목록 가져오기
models = openai.models.list()

# 모델 목록 출력
for model in models.data:  # 수정: 'data' 속성 사용
    # Available model: model.id
    pass
