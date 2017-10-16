FROM alpine
RUN apk add --no-cache bash py2-pip \
	&& pip2 install --upgrade pip 
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt 
RUN pip install gunicorn

ENTRYPOINT ["gunicorn"]
CMD ["-w","1","-b","0.0.0.0:5000","--threads","1","makememe:app","--access-logfile","/dev/stdout","--error-logfile","/dev/stdout"]
