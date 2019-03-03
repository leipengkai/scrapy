from mitmproxy import ctx

def request(flow):
    request = flow.request
    info = ctx.log.info
    warn = ctx.log.warn

    # warn(dir(request))

    info(request.url)

    info(str(request.headers))

    info(str(request.cookies))

    info(request.host)

    info(str(request.port))