import log

LOG = log.get_logger()

ALLOWED_ORIGINS = ['http://localhost:8000', 'http://127.0.0.1:8000', 'http://localhost:9528',
                   'http://127.0.0.1:9528','http://localhost:9528/', 'http://152.69.226.2:9528']  # Or load this from a config file


class CORSMiddleware(object):
    def __init__(self):
        super().__init__()
        LOG.debug('CORSMiddleware Init')

    async def process_request(self, request, response):
        origin = request.get_header('Origin')
        if origin in ALLOWED_ORIGINS:
            response.set_header('Access-Control-Allow-Origin', origin)
            response.set_header('Access-Control-Allow-Headers', '*')
            response.set_header('Access-Control-Allow-Credentials', 'true')
