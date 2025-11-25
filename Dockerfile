FROM python:3.11-slim

# ?묒뾽 ?붾젆?좊━ ?ㅼ젙
WORKDIR /app

# ?쒖뒪???섏〈???ㅼ튂
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Python ?섏〈???ㅼ튂
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ?좏뵆由ъ??댁뀡 ?뚯씪 蹂듭궗
COPY web_vocab_app.py .
COPY templates/ templates/
COPY static/ static/

# JSON ?뚯씪 珥덇린??(?뚯씪???놁뼱??鍮뚮뱶媛 ?섎룄濡?
# ?깆씠 ?먮룞?쇰줈 ?앹꽦?섏?留? 鍮??뚯씪濡?珥덇린?뷀븯???ㅻ쪟 諛⑹?
RUN echo '{}' > vocabulary.json && echo '{}' > quiz_stats.json

# ?ы듃 ?섍꼍 蹂??(Railway媛 ?먮룞?쇰줈 ?ㅼ젙)
# Railway??PORT ?섍꼍 蹂?섎? ?먮룞?쇰줈 ?ㅼ젙?섎?濡?ENV濡?湲곕낯媛믩쭔 ?ㅼ젙
ENV PORT=5000

# ?ы듃 ?몄텧 (?숈쟻 ?ы듃 ?ъ슜)
EXPOSE 5000

# Gunicorn?쇰줈 Flask ???ㅽ뻾
# Railway??PORT ?섍꼍 蹂?섎? ?덉쟾?섍쾶 泥섎━
# exec form ???shell form???ъ슜?섏뿬 ?섍꼍 蹂???뺤옣 蹂댁옣
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 2 --threads 2 --timeout 120 web_vocab_app:app"]
