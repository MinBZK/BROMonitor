def generate_pingdom_xml(status, code):
    return """<pingdom_http_custom_check>
    <status>{status}</status>
    <response_time>{code}</response_time>
    </pingdom_http_custom_check>""".format(status=status, code=code)
