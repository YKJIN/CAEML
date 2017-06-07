FROM python:2.7


RUN apt-get update && \
apt-get install -y curl && \
apt-get install -y tcl8.5 tk8.5 && \
apt-get -y --no-install-recommends install \
    ca-certificates && \
apt-get install -y libglu1-mesa


RUN gpg --keyserver ha.pool.sks-keyservers.net --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4
RUN curl -o /usr/local/bin/gosu -SL "https://github.com/tianon/gosu/releases/download/1.4/gosu-$(dpkg --print-architecture)" \
    && curl -o /usr/local/bin/gosu.asc -SL "https://github.com/tianon/gosu/releases/download/1.4/gosu-$(dpkg --print-architecture).asc" \
    && gpg --verify /usr/local/bin/gosu.asc \
    && rm /usr/local/bin/gosu.asc \
    && chmod +x /usr/local/bin/gosu

#install code-aster
RUN apt-get update
RUN apt-get install -y net-tools
RUN apt-get install -y libglu1-mesa

#install code-aster prerequisites here


RUN ["/bin/bash", "-c", "mkdir -p /tmp/salome && \
 cd /tmp/salome && \
 curl -SL http://www.code-aster.org/FICHIERS/SALOME-MECA-2016-LGPL-1.tgz | tar xvz && \
 ./SMECA_V2016_LGPL.run <<< $'/opt/salome\nN\n' && \
 rm SMECA_V2016_LGPL.run"]

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

COPY code_aster.py /usr/local/bin/code_aster.py
RUN chmod +x /usr/local/bin/code_aster.py

COPY pvbatch.py /usr/local/bin/pvbatch.py
RUN chmod +x /usr/local/bin/pvbatch.py

ENTRYPOINT [ "/usr/local/bin/entrypoint.sh"]

CMD ["/bin/bash"]

