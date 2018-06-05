FROM centos:6
RUN sed --expression '/tsflags=nodocs/d' --in-place /etc/yum.conf
COPY epel.repo /etc/yum.repos.d/
RUN yum --assumeyes install @buildsys-build rpmdevtools python2-sh; \
    yum clean all
COPY plugin.py /
ENTRYPOINT ["/usr/bin/python"]
CMD ["/plugin.py"]
