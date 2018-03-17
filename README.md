# drone-rpmbuild

Drone plugin to build RPM packages.

The plugin script is a Python 2/3 script that is compatible with RHEL, CentOS, and Fedora.

## Build

Dockerfiles for each distro are in separate branches.

* RHEL 6: `docker build --pull --tag rpmbuild:el6 'https://github.com/carlwgeorge/drone-rpmbuild.git#el6'`
* RHEL 7: `docker build --pull --tag rpmbuild:el7 'https://github.com/carlwgeorge/drone-rpmbuild.git#el7'`
* CentOS 6: `docker build --pull --tag rpmbuild:c6 'https://github.com/carlwgeorge/drone-rpmbuild.git#c6'`
* CentOS 7: `docker build --pull --tag rpmbuild:c7 'https://github.com/carlwgeorge/drone-rpmbuild.git#c7'`

# Usage

- [plugin usage](USAGE.md#plugin-usage)
- [direct usage](USAGE.md#direct-usage)
