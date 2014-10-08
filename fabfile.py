import os
from timeit import reindent
from fabric.colors import green
from fabric.context_managers import *
from fabric.contrib.files import contains, exists
from fabric.decorators import task
from fabric.operations import *
from fabric.state import env
from fabric.tasks import execute
from fabtools import require
from fabtools.python import virtualenv as python_virtualenv


@task
def dev():
    env.host_string = 'jianguo.o-value.com'
    env.path = '/var/deploy/jianguo'
    env.activate = 'source ' + env.path + '/virt-python/bin/activate'
    env.depot = 'git@github.com:shuoli84/jianguo.git'
    env.depot_name = 'jianguo'
    env.branch = 'master'
    env.no_apt_update = True
    env.user = "lishuo"


def new_virtualenv():
    require.python.virtualenv(os.path.join(env.path, 'env'))

@contextmanager
def virtualenv():
    with python_virtualenv(os.path.join(env.path, 'env')):
        yield

@task
def install_nginx():
    with hide("output"):
        if not contains('/etc/apt/sources.list', 'nginx'):
            sudo('echo "deb http://ppa.launchpad.net/nginx/stable/ubuntu $(lsb_release -cs) main" >> /etc/apt/sources.list')
            sudo('apt-key adv --keyserver keyserver.ubuntu.com --recv-keys C300EE8C')
            sudo("apt-get update")

        require.deb.package('nginx')
        put("vender/nginx_util/*",  "/usr/bin/", use_sudo=True, mode="770")

@task
def init():
    """
    Setup the server for the first time
    :return:
    """

    banner("init")
    with show("output"):
        if not env.get('no_apt_update'):
            sudo('apt-get update')

        require.directory(env.path, mode="777", use_sudo=True)
        require.directory('/var/run/jianguo/', owner='www-data', group='www-data', mode='770', use_sudo=True)
        require.directory('/var/log/jianguo/', owner='www-data', group='www-data', mode='770', use_sudo=True)
        require.directory('/var/log/supervisord/', owner='www-data', group='www-data', mode='770', use_sudo=True)
        require.directory('/var/run/supervisord/', owner='www-data', group='www-data', mode='770', use_sudo=True)
        require.directory('~/.ssh', mode='700')
        put('deployment', '~/.ssh/id_rsa')
        run('chmod 600 ~/.ssh/id_rsa')

        require.deb.packages([
            'gcc', 'python-all-dev', 'libpq-dev', 'libjpeg-dev', 'libxml2-dev', 'libxslt1-dev', 'libmysqlclient-dev',
            'libfreetype6-dev', 'libevent-dev'
        ])
        require.python.pip(version="1.0")

        new_virtualenv()

        me = run('whoami')
        sudo('adduser %s www-data' % me)

        install_nginx()

@task
def check_out():
    banner("check out")
    require.git.command()
    with cd(env.path):
        if not exists(os.path.join(env.path, env.depot_name)):
            print green('Git folder not there, create it')
            run("git clone %s" % env.depot)
            sudo("chmod 777 %s" % env.depot_name)
            with cd(env.depot_name):
                run("git checkout %s" % env.branch)
        else:
            with cd(env.depot_name):
                with settings(warn_only=True):
                    run('git reset --hard HEAD')
                    run('git remote set-url origin %s' % env.depot)

                    result = run('git show-ref --verify --quiet refs/heads/%s' % env.branch)
                    if result.return_code > 0:
                        run('git fetch origin %s:%s' % (env.branch, env.branch))
                        run("git checkout %s" % env.branch)
                    else:
                        run('git checkout %s' % env.branch)
                        run('git pull origin %s' % env.branch)


@task
def config_webserver():
    banner("config web server")
    with virtualenv():
        with cd(os.path.join(env.path, env.depot_name)):
            require.python.requirements('requirements.txt', index='http://pypi.douban.com/simple')

            with hide('output'):
                print green('Collect static files')

                require.directory('/var/static/jianguo', use_sudo=True)
                sudo('cp -r publish/static/* /var/static/jianguo/')
                sudo('rm -r publish')
                if exists('/var/wsgi/jianguo-backup'):
                    sudo('rm -r /var/wsgi/jianguo-backup')
                if exists('/var/wsgi/jianguo'):
                    sudo('mv /var/wsgi/jianguo /var/wsgi/jianguo-backup')

                sudo('mkdir -p /var/wsgi/jianguo')
                sudo('cp -r . /var/wsgi/jianguo')
                sudo('chgrp -R www-data /var/wsgi/jianguo')
                sudo('chown -R www-data /var/wsgi/jianguo')

            with cd('/var/wsgi/jianguo'):
                # use --noinput to prevent create super user. When super user created, then a profile object needs
                # to be created, at that point, that table is not created yet. Then it crashes.
                with hide('output'):
                    run("python manage.py syncdb --noinput")
                run("python manage.py migrate")

                run('supervisorctl restart gunicorn')

                put('nginx.conf', '/etc/nginx/sites-available/jianguo.conf', use_sudo=True)
                with settings(warn_only=True):
                    sudo('nginx_dissite default')

                sudo('nginx_ensite jianguo.conf')

@task
def deploy():
    execute(init)
    execute(check_out)
    execute(config_webserver)
    banner('Deploy Succeeded. Go Home!')


def banner(message):
    host_string = "%s (%s)" % (message, env.host_string)

    print green(reindent("""
    #########################################################################
    ## %s
    #########################################################################
    """ % host_string, 0))


