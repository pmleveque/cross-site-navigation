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


def appcfg(cmd):
    return 'echo "%s" | %s -q --passin -e %s %s .' % (
        settings.CSE_PASSWORD,
        sdk('appcfg.py'),
        settings.CSE_EMAIL,
        cmd,
    )


@task
def serve():
    """serve the application"""
    local(sdk('dev_appserver.py') + ' app.yaml')


@task
def deploy():
    """deploy the application"""
    if prompt('Increase version ?', default='n') == 'y':
        versions = local(appcfg('list_versions'), capture=True)
        versions = versions.split('[', 1)[1].split(',')
        versions = [v.strip() for v in versions]
        version = list(reversed([v for v in versions if v[0].isdigit()]))[0]
        old_version = version
        version = [int(i) for i in version.split('-')]
        version[-1] += 1
        version = '-'.join([str(i) for i in version])
        local("sed -i -e 's/%s/%s/' app.yaml" % (old_version, version))
