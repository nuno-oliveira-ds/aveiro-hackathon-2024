FROM python:3.9 as mobility

EXPOSE 8080

COPY . .
RUN pip install -r requirements.txt

ENTRYPOINT ["sh", "run.sh"]