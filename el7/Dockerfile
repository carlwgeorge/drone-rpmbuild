FROM registry.access.redhat.com/rhel7
RUN sed --expression '/tsflags=nodocs/d' --in-place /etc/yum.conf
RUN sed --expression 's|^enabled=1|enabled=0|' --in-place /etc/yum/pluginconf.d/search-disabled-repos.conf
RUN yum --disablerepo '*' repolist; \
    yum-config-manager --disable '*'; \
    yum-config-manager --enable rhel-7-server{,-optional,-extras}-rpms; \
    yum clean all
COPY epel.repo /etc/yum.repos.d/
RUN yum --assumeyes install @buildsys-build rpmdevtools python2-sh; \
    yum clean all
COPY plugin.py /
ENTRYPOINT ["/usr/bin/python"]
CMD ["/plugin.py"]
