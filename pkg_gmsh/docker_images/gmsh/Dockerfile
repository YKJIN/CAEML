FROM ubuntu

RUN apt-get update

RUN apt-get install -y \
    build-essential \
    ca-certificates \
    gcc \
    git \
    libpq-dev \
    make \
    pkg-config \
    python3 \
    python3-dev \
    python3-pip \
    aria2 \
    && apt-get autoremove -y \
    && apt-get clean

RUN apt-get install -y curl libglu1-mesa
RUN apt-get install -y libxcursor1 libxft-dev libxinerama1 libxrender-dev libsm6

RUN mkdir -p /tmp &&\
 curl -SL http://gmsh.info/bin/Linux/gmsh-svn-Linux64.tgz |\
 tar -xzC  /tmp &&\
 cp /tmp/gmsh-2.16.0-svn-Linux/bin/gmsh /usr/bin &&\
 rm -r /tmp


RUN gpg --keyserver ha.pool.sks-keyservers.net --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4
RUN curl -o /usr/local/bin/gosu -SL "https://github.com/tianon/gosu/releases/download/1.4/gosu-$(dpkg --print-architecture)" \
    && curl -o /usr/local/bin/gosu.asc -SL "https://github.com/tianon/gosu/releases/download/1.4/gosu-$(dpkg --print-architecture).asc" \
    && gpg --verify /usr/local/bin/gosu.asc \
    && rm /usr/local/bin/gosu.asc \
    && chmod +x /usr/local/bin/gosu

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

ADD scripts /scripts

ENTRYPOINT [ "/usr/local/bin/entrypoint.sh"]

CMD ["/bin/bash"]