import pytest

from tests.plugins.constants import default_upload
from tests.plugins.upload_to_s3 import upload_file_to_s3_by_job_id

pytest_plugins = "tests.examples.examples_report_plugin", "tests.plugins.bokeh_server", "tests.plugins.jupyter_notebook", "tests.plugins.webserver"


def pytest_addoption(parser):
    parser.addoption(
        "--upload", dest="upload", action="store_true", default=default_upload, help="upload test artefacts to S3"
    )
    parser.addoption(
        "--log-file", dest="log_file", metavar="path", action="store", default='examples.log', help="where to write the complete log"
    )


def pytest_sessionfinish(session, exitstatus):
    try_upload = session.config.option.upload
    seleniumreport = session.config.option.htmlpath
    is_slave = hasattr(session.config, 'slaveinput')
    if try_upload and seleniumreport and not is_slave:
        upload_file_to_s3_by_job_id(seleniumreport)


@pytest.yield_fixture(scope="session")
def log_file():
    with open(pytest.config.option.log_file, 'w') as f:
        yield f
