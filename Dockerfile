FROM gcr.io/cloudjlb-container-devops/base-python 
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt 
RUN pip install gunicorn

ENTRYPOINT ["gunicorn"]
CMD ["-w","1","-b","0.0.0.0:5000","--threads","1","makememe:app","--access-logfile","/dev/stdout","--error-logfile","/dev/stdout"]
