# Plugin Usage

By default, the plugin will build `${DRONE_WORKSPACE}/${DRONE_REPO_NAME}.spec`, using `${DRONE_WORKSPACE}` as the RPM sources directory.

```yaml
pipeline:
  build:
    image: rpmbuild:el7
```

Specify an alternate paths (relative to `${DRONE_WORKSPACE}`) for the spec file and/or sources directory:

```diff
 pipeline:
   build:
     image: rpmbuild:el7
+    spec: SPECS/beef.spec
+    sources: SOURCES
```

Define RPM macros for the build:

```diff
 pipeline:
   build:
     image: rpmbuild:el7
+    define:
+      vendor: Beef Project
```

Add RPM `--with`/`--without` flags to the build:

```diff
 pipeline:
   build:
     image: rpmbuild:el7
+    with:
+      - feature1
+      - feature2
+    without:
+      - feature3
```

Add additional yum repositories during the build:

```diff
 pipeline:
   build:
     image: rpmbuild:el7
+    repos:
+      - https://example.com/example.repo
```

# Direct Usage

By default, the plugin will build `${DRONE_WORKSPACE}/${DRONE_REPO_NAME}.spec`, using `${DRONE_WORKSPACE}` as the RPM sources directory.

```
docker run --rm \
  -e DRONE_REPO_NAME=beef \
  -e DRONE_WORKSPACE=/tmp/beef \
  rpmbuild:el7
```

Specify an alternate paths (relative to `${DRONE_WORKSPACE}`) for the spec file and/or sources directory:

```diff
 docker run --rm \
   -e DRONE_REPO_NAME=beef \
   -e DRONE_WORKSPACE=/tmp/beef \
+  -e PLUGIN_SPEC=SPECS/beef.spec \
+  -e PLUGIN_SOURCES=SOURCES \
   rpmbuild:el7
```

Define RPM macros for the build:

```diff
 docker run --rm \
   -e DRONE_REPO_NAME=beef \
   -e DRONE_WORKSPACE=/tmp/beef \
+  -e PLUGIN_DEFINE='{"vendor":"Beef Project"}' \
   rpmbuild:el7
```

Add RPM `--with`/`--without` flags to the build:

```diff
 docker run --rm \
   -e DRONE_REPO_NAME=beef \
   -e DRONE_WORKSPACE=/tmp/beef \
+  -e PLUGIN_WITH=feature1,feature2 \
+  -e PLUGIN_WITHOUT=feature3 \
   rpmbuild:el7
```

Add additional yum repositories during the build:

```diff
 docker run --rm \
   -e DRONE_REPO_NAME=beef \
   -e DRONE_WORKSPACE=/tmp/beef \
+  -e PLUGIN_REPOS=https://example.com/example.repo \
   rpmbuild:el7
```
