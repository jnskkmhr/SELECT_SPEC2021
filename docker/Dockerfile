FROM python:3.7 
WORKDIR /workspace 
LABEL maintainer = "Junnosuke Kamohara junjun.k2012@gmail.com"

RUN apt-get update  
RUN apt-get upgrade
RUN apt-get install -y sudo  
RUN apt-get install -y git 
# RUN sudo apt-get install python3-dev
# RUN sudo apt-get install libevent-dev
RUN sudo apt install -y python3-venv

CMD ["/bin/bash"]