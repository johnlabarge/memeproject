FROM alpine
RUN apk add --no-cache bash py2-pip \
	&& pip2 install --upgrade pip 
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt 
