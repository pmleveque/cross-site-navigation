# -*- coding: utf-8 -*-
from fabric.api import task, local, prompt
import settings
import os


z = 'http://googleappengine.googlecode.com/files/google_appengine_1.8.8.zip'


def sdk(*args):
    p = os.path.expanduser('~/.gae/google_appengine')
    if not os.path.isdir(p):
        local('mkdir -p ~/.gae; cd ~/.gae; wget -c %s && unzip *.zip' % z)
    return os.path.join(p, *args)


def appcfg(*args):
    return 'echo "%s" | %s -q --passin -e %s %s' % (
        settings.CSE_PASSWORD,
        sdk('appcfg.py'),
        settings.CSE_EMAIL,
        ' '.join(list(args)),
    )


@task
def serve():
    """serve the application"""
    local(sdk('dev_appserver.py') + ' app.yaml')


@task
def inc_version():
    """inc application version"""
    version = local('grep -E "^version:" app.yaml', capture=True)
    version = version.split(':')[1].strip()
    old_version = version
    version = [int(i) for i in version.split('-')]
    version[-1] += 1
    version = '-'.join([str(i) for i in version])
    versions = (old_version, version)
    if prompt('Inc version from %s to %s' % versions, default='n') == 'y':
        local("sed -i -e 's/%s/%s/' app.yaml" % versions)


@task
def deploy():
    """deploy the application"""
    local(appcfg('update', '.'))
