from lxml import etree
from backend.utils.pingdom import generate_pingdom_xml


def test_generate_pingdom_xml():
    status = "OK"
    code = 200
    pingdom_xml_string = generate_pingdom_xml(status, code)
    root = etree.fromstring(pingdom_xml_string)
    statusses = list(root.iter("status"))
    response_times = list(root.iter("response_time"))
    # Test if the root has the correct tag
    assert root.tag == "pingdom_http_custom_check"
    # Test if there is exactly 1 status child in the xml
    assert len(statusses) == 1
    # Test if the status tag contains the expected value
    assert statusses[0].text == status
    # Test if there is exactly 1 response_time child in the xml
    assert len(response_times) == 1
    # Test if the response_time child contains the expect value
    assert response_times[0].text == str(code)
