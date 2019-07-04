#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

__author__ = 'Sergei S. https://makeitwork.cz'
__copyright__ = '(c)'
__license__ = 'MIT'
__version__ = '0.1.1'

import cherrypy
import requests
import os
import pwd
import grp
import yaml
import logging
import datetime

default_timeout = 5

logger = logging.getLogger('cctv-proxy')

try:
    yaml.warnings({'YAMLLoadWarning': False})
except:
    pass


class CCTVProxy:

    def __init__(self, config):
        self.config = config
        dir_me = os.path.realpath(os.path.dirname(os.path.realpath(__file__)))
        self.nocam = config.get('nocam', dir_me + '/nocam.jpg')
        self.debug = False

    @cherrypy.expose
    def ci(self, **kwargs):
        """
        param _id is used to select camera

        param _return: "raw" will return raw camera reply on errors, "test"
        will test camera and return OK instesad of image (or FAILED)

        other params are passed to camera as-is.
        """
        try:
            cam = kwargs.get('_id')
            del kwargs['_id']
        except:
            self._log('bad request, no camera id specified')
            raise cherrypy.HTTPError(400)
        try:
            cam_host = self.config['cams'][cam]
        except:
            self._log('camera id unknown: {}'.format(cam))
            raise cherrypy.HTTPError(404)
        try:
            cam_uri = self.config['uri']
        except:
            cam_uri = 'axis-cgi/jpg/image.cgi'
        ret = kwargs.get('_return')
        if '_return' in kwargs:
            del kwargs['_return']
        url = 'http://{}/{}'.format(cam_host, cam_uri)
        http_login = self.config.get('login')
        http_password = self.config.get('password')
        opts = {}
        if http_login and http_password:
            opts = {
                'auth': requests.auth.HTTPBasicAuth(http_login, http_password)
            }
        try:
            result = requests.get(
                url,
                params=kwargs,
                timeout=self.config.get('timeout', default_timeout),
                **opts)
            if not result.ok:
                if ret == 'raw':
                    cherrypy.serving.response.status = result.status_code
                else:
                    raise Exception('Camera HTTP code {}'.format(
                        result.status_code))
            self._log(url)
            if ret == 'test':
                return 'OK'
            else:
                cherrypy.serving.response.headers['Content-Type'] = 'image/jpeg'
                return result.content
        except Exception as e:
            if self.debug:
                import traceback
                print(traceback.format_exc())
            self._log(url + ' - FAILED')
            if ret == 'raw':
                raise cherrypy.HTTPError(message=str(e))
            elif ret == 'test':
                return 'FAILED'
            else:
                cherrypy.serving.response.headers['Content-Type'] = 'image/jpeg'
                return open(self.nocam, 'rb')

    def _log(self, msg, logfunc=logger.debug):
        logfunc('{} CCTVProxy {}'.format(
            datetime.datetime.now().strftime('%Y-%M-%D %H:%M:%S'), msg))


def main():
    import argparse
    _me = 'CCTV Proxy version %s' % __version__

    ap = argparse.ArgumentParser(description=_me)

    ap.add_argument(
        '-D', '--debug', help='Debug mode', action='store_true', default=False)
    ap.add_argument(
        '-f',
        '--config-file',
        help='Configuration file',
        default='/usr/local/etc/cctv_proxy.yml')

    try:
        import argcomplete
        argcomplete.autocomplete(ap)
    except:
        pass

    a = ap.parse_args()

    config = yaml.load(open(a.config_file))

    if not a.debug:
        cherrypy.config.update({
            'environment': 'production',
            'log.screen': False,
            'log.access_file': '',
            'log.error_file': ''
        })
        cherrypy.log.access_log.propagate = False
        cherrypy.log.error_log.propagate = False
    else:
        logging.basicConfig(level=logging.DEBUG)

    cherrypy.server.unsubscribe()
    server1 = cherrypy._cpserver.Server()
    server1.socket_port = config.get('bind-port', 8781)
    server1._socket_host = config.get('bind-host', '127.0.0.1')
    server1.thread_pool = config.get('pool', 30)
    server1.subscribe()

    W = CCTVProxy(config)

    W.debug = a.debug

    cherrypy.tree.mount(W, '/')

    my_uid = pwd.getpwnam(config.get('user', 'nobody')).pw_uid
    if my_uid == 0:
        raise Exception('Can not work under root')

    my_gid = grp.getgrnam(config.get('group', 'nogroup')).gr_gid

    pid_file = config.get('pid', '/tmp/cctv_proxy.pid')

    open(pid_file, 'w').write(str(os.getpid()))

    cherrypy.engine.start()

    if my_uid != os.getuid():
        try:
            os.setgid(my_gid)
            os.setuid(my_uid)
        except:
            logging.warning('Can not set UID/GID on process')

    cherrypy.engine.block()


if __name__ == '__main__':
    main()
