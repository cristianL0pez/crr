FROM python:3.9

# 
WORKDIR /crr

# 
COPY ./ /crr/

# 
RUN pip install --no-cache-dir --upgrade -r /crr/requirements.txt

COPY ./app /crr/app

# 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]