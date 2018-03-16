# drone-rpmbuild

Drone plugin to build RPM packages.

The plugin script is a Python 2/3 script that is compatible with RHEL, CentOS, and Fedora.

## Build

Checkout the desired branch and then build the image.

```
git checkout el7
docker build --pull --tag rpmbuild:el7 .
```

# Usage

- [plugin usage](USAGE.md#plugin-usage)
- [direct usage](USAGE.md#direct-usage)
