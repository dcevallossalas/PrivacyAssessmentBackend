FROM alpine:3.22.0
RUN apk update
RUN apk add --no-cache python3 py3-pip
RUN pip3 install flask==2.2.5 --break-system-packages
RUN pip3 install requests==2.32.3 --break-system-packages
RUN pip3 install pypdf==5.7.0 --break-system-packages
RUN chmod 777 /dev
WORKDIR /home/alpine
COPY service.py /home/alpine/service.py
CMD ["python3", "/home/alpine/service.py"]
