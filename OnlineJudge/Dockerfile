FROM python

WORKDIR  ./

COPY HelloWorld.py  ./

CMD [ "python","HelloWorld.py" ]

FROM java

WORKDIR ./

COPY HelloWorld.java  ./

RUN javac HelloWorld.java

CMD ["java", "HelloWorld"]