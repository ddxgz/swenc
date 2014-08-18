from swift.common.swob import Request, HTTPException
from swift.common.utils import split_path, get_logger




DEBUG = 1


class Encryptor(object):
    def encryting(self):
        pass


class SwiftEncryptionMiddleware(object):
    """
    Middleware for encrypting object upload to swift
    """
    def __init__(self, app, conf):
        # app is the final application
        self.app = app
        self.conf = conf
        self.logger = get_logger(conf, log_route='encryption')
 
    def __call__(self, env, start_response):
        """
        WSGI entry point
        """
        req = Request(env)
        try:
            vrs, account, container, obj = req.split_path(4, 4, True)
            if DEBUG:
                print('obj:%s' % obj)
        except ValueError:
            return self.app(env, start_response)
        try:
            if env['REQUEST_METHOD'] == "PUT":
                # Read the object content and enc_key in memory 
                # encrypt the object with the enc_key
                content = env['wsgi.input'].read()
                if content:
                    return Response(status=403,
                                body="content %s detected" % content,
                                content_type="text/plain")(env, start_response)
                else:
                    return Response(status=403,
                                body="content not detected",
                                content_type="text/plain")(env, start_response)
                if DEBUG:
                    print(content)
                #encryptor = Encryptor()
                content = content + "yyyyyyyyyyyyyyyyy"
            # Maybe add the decrytion process later 
            #elif env['REQUEST_METHOD'] == "GET":
        except HTTPException as err_resp:
            return err_resp(env, start_response)

        return self.app(env, start_response)


def filter_factory(global_conf, **local_conf):
    """Returns a WSGI filter app for use with paste.deploy."""
    conf = global_conf.copy()
    conf.update(local_conf)
    #register_swift_info('encryption', account_acls=True)

    def enc_filter(app):
        return SwiftEncryptionMiddleware(app, conf)
    return enc_filter