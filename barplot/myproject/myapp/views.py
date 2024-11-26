# myapp/views.py
from django.http import HttpResponse
from django.views import View
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
import nltk
from nltk.corpus import stopwords
import re
from io import BytesIO
import base64

import pandas as pd

import matplotlib as mpl


# import matplotlib.font_manager as fm
# from shapely.geometry import Point
mpl.rcParams['font.family'] = 'Malgun Gothic'
mpl.rcParams['axes.unicode_minus'] = False


nltk.download('stopwords')

def clean_text(text):
    text = re.sub(r'[^\w\s]', '', text)
    text = text.lower()
    return text

class WordFrequencyChart(View):
    def get(self, request):
        qna_texts = [
            "최고가 되기 위해서 금융결제원은 국내 다양한 금융 관련 서비스를 지원하는 최고의 기업입니다.",
            "이런 여러 서비스 운영에 있어 중요한 것은 사용자에게 적절한 UI의 표출, 그리고 효율적인 데이터 처리를 통한 빠른 속도 제공입니다.",
            "저는 이를 배우기 위해 매일 진행 중인 알고리즘 풀이 외에도 기존에 공부했던 JSP에 대해 조금 더 파악하고, spring에 활용하기 전에 배우기 위해 관련 학원에 다니며 공부하였고, 여러 예제를 사용한 Spring 프로젝트를 진행했습니다."
        ]
        
        all_text = " ".join(qna_texts)
        clean_data = clean_text(all_text)
        words = clean_data.split()
        
        stop_words = set(stopwords.words('english'))
        words_filtered = [word for word in words if word not in stop_words]
        
        word_counts = Counter(words_filtered)
        
        df = pd.DataFrame(word_counts.items(), columns=['Word', 'Frequency'])
        df = df.sort_values(by='Frequency', ascending=False).head(10)
        
        plt.figure(figsize=(10, 6))
        plt.bar(df['Word'], df['Frequency'], color='skyblue')
        plt.xlabel('단어')
        plt.ylabel('빈도 수')
        plt.title('가장 많이 나온 단어 Top 10')
        plt.xticks(rotation=45)

        # 그래프를 이미지로 저장
        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        
        return HttpResponse(f'<img src="data:image/png;base64,{image_base64}" />')
