FROM python:3.7 
WORKDIR /workspace 
LABEL maintainer = "Junnosuke Kamohara junjun.k2012@gmail.com"

RUN apt-get update  
RUN apt-get upgrade
RUN apt-get install -y sudo  
RUN apt-get install -y git 
RUN sudo apt-get install python3-dev
RUN sudo apt-get install libevent-dev

CMD ["/bin/bash"]