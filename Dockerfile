FROM docker.mycloudand.me/jessie

RUN DEBIAN_FRONTEND=noninteractive \
    apt-get -q update && \
    apt-get install -y maven python-lxml

RUN useradd -m mvnbuilder && \
    mkdir -p /home/mvnbuilder/.m2
ADD settings.xml /home/mvnbuilder/.m2/settings.xml
RUN chown -R mvnbuilder /home/mvnbuilder/.m2

ADD Dockerfile.child /Dockerfile.child
ADD pom-gen.py /pom-gen.py
ADD pom-gen.sh /pom-gen.sh

ENV JAVA_HOME /usr/lib/jvm/java-7-openjdk-amd64/jre

# Execute without dependencies to download+cache maven plugins
RUN POM_DEPS="" /pom-gen.sh

CMD /pom-gen.sh
