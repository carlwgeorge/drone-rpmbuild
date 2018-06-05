FROM centos:7
RUN sed --expression '/tsflags=nodocs/d' --in-place /etc/yum.conf
RUN sed --expression 's/\(%dist \.el7\)\.centos/\1/' /etc/rpm/macros.dist
COPY epel.repo /etc/yum.repos.d/
RUN yum --assumeyes install @buildsys-build rpmdevtools python2-sh; \
    yum clean all
COPY plugin.py /
ENTRYPOINT ["/usr/bin/python"]
CMD ["/plugin.py"]
