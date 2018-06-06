#!/usr/bin/env python

"""
drone rpmbuild plugin

PLUGIN_SPEC             path to spec file
PLUGIN_SOURCES          path to sources directory
PLUGIN_DEFINE           extra definitions
PLUGIN_WITH             bcond_with flags
PLUGIN_WITHOUT          bcond_without flags
PLUGIN_REPOS            additional repos to build with
"""

from __future__ import print_function
from glob import glob
import json
import os
import shutil
import sys

import pycurl
import sh


# these should always be set inside drone
try:
    repo_name = os.environ['DRONE_REPO_NAME']
except KeyError:
    raise SystemExit('DRONE_REPO_NAME: environment variable not set')

try:
    workspace = os.environ['DRONE_WORKSPACE']
except KeyError:
    raise SystemExit('DRONE_WORKSPACE: environment variable not set')


# chown the workspace
sh.sudo.chown('--recursive', 'drone:drone', workspace)


# set the spec file path, fallback to {repo_name}.spec
spec = os.path.join(workspace, os.environ.get('PLUGIN_SPEC', '{0}.spec'.format(repo_name)))

if not os.path.isfile(spec):
    raise SystemExit('{0}: file not found'.format(spec))


# set the sources path, fallback to {workspace}
try:
    sources = os.path.join(workspace, os.environ['PLUGIN_SOURCES'])
except KeyError:
    sources = workspace

if not os.path.isdir(sources):
    raise SystemExit('{0}: directory not found'.format(sources))


# macro definitions
definitions = {
    '_topdir': workspace,
    '_sourcedir': sources,
    '_specdir': os.path.dirname(spec)
}

plugin_define = os.environ.get('PLUGIN_DEFINE')
if plugin_define:
    try:
        definitions.update(json.loads(plugin_define))
    except ValueError:
        raise SystemExit('{0}: could not parse as json'.format(plugin_define))


# conditionals
bcond_withs = []
plugin_with = os.environ.get('PLUGIN_WITH')
if plugin_with:
    bcond_withs.extend(plugin_with.split(','))

bcond_withouts = []
plugin_without = os.environ.get('PLUGIN_WITHOUT')
if plugin_without:
    bcond_withouts.extend(plugin_without.split(','))


# add additional repos
plugin_repos = os.environ.get('PLUGIN_REPOS')
if plugin_repos:
    for url in plugin_repos.split(','):
        base = os.path.basename(url)
        if not base.endswith('.repo'):
            raise SystemExit('{0}: does not end with ".repo"')
        destination = os.path.join('/etc/yum.repos.d', base)
        with open(destination, 'wb') as f:
            curl = pycurl.Curl()
            curl.setopt(curl.URL, url)
            curl.setopt(curl.WRITEDATA, f)
            curl.perform()
            curl.close()


print('==> get sources')
sys.stdout.flush()
sh.spectool('--get-files', '--directory', sources, spec, _fg=True)


print('==> build SRPM')
sys.stdout.flush()
rpmbuild = sh.rpmbuild.bake('-bs')
for definition in definitions.items():
    rpmbuild = rpmbuild.bake('--define', ' '.join(definition))
for bcond_with in bcond_withs:
    rpmbuild = rpmbuild.bake('--with', bcond_with)
for bcond_without in bcond_withouts:
    rpmbuild = rpmbuild.bake('--without', bcond_without)
rpmbuild(spec, _fg=True)
rpm_files = [glob(os.path.join(workspace, 'SRPMS', '*.src.rpm'))[0]]


print('==> install build requirements')
sys.stdout.flush()
if sh.which('dnf'):
    sh.sudo.dnf.builddep('--assumeyes', rpm_files[0], _fg=True)
else:
    sh.sudo('yum-builddep', '--assumeyes', rpm_files[0], _fg=True)


print('==> build RPMs')
sys.stdout.flush()
rpmbuild = sh.rpmbuild.bake('-bb')
for definition in definitions.items():
    rpmbuild = rpmbuild.bake('--define', ' '.join(definition))
for bcond_with in bcond_withs:
    rpmbuild = rpmbuild.bake('--with', bcond_with)
for bcond_without in bcond_withouts:
    rpmbuild = rpmbuild.bake('--without', bcond_without)
rpmbuild(spec, _fg=True)
rpm_files.extend(glob(os.path.join(workspace, 'RPMS', '*', '*.rpm')))


# clean up
for rpm_file in rpm_files:
    shutil.move(rpm_file, workspace)
shutil.rmtree(os.path.join(workspace, 'BUILD'))
shutil.rmtree(os.path.join(workspace, 'BUILDROOT'))
shutil.rmtree(os.path.join(workspace, 'RPMS'))
shutil.rmtree(os.path.join(workspace, 'SRPMS'))
