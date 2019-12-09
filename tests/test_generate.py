import os

import mock
import pytest

from rancher_config_volume import generate
from tests import mocks

test_arguments = [
    ("config/app", "config/app"),
    ("/config/app", "config/app"),
    ("/config/app/", "config/app"),
    ("config/app/", "config/app"),
    ("my/config/certificate", "my/config/certificate"),
    ("    old/config/certificate", "old/config/certificate"),
    ("    new/config/certificate     ", "new/config/certificate"),
    ("    current/config/certificate", "current/config/certificate"),
]

success_cases = [
    ("config/0-success", "/config/app/config.yaml", "/config/app", "content\n"),
    ("config/1-success-two", "/my/new/config/test.json", "/my/new/config", "{}\n"),
]


def setup_mock_server(mock_name):
    mock_port = mocks.get_free_port()
    mocks.start_mock_server(mock_port, mock_name)
    return mock_port


@pytest.mark.parametrize("test_input, expected", test_arguments)
def test_get_arg_success(test_input, expected):
    with mock.patch('sys.argv', ["file_name", test_input]):
        generator = generate.Generator()
        generator.get_command()
        assert generator.command == expected


def test_get_arg_failure():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        with mock.patch('sys.argv', ["file_name"]):
            generate.Generator().get_command()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


def test_get_config_path():
    mock_name = "config/0-success"
    port = setup_mock_server("test")
    os.environ["RANCHER_RUN_FOREVER"] = "false"
    os.environ["RANCHER_METADATA_HOST"] = "localhost:{}".format(port)
    with mock.patch('sys.argv', ["file_name", mock_name]):
        generator = generate.Generator()
        result = generator.get_config_path(mock_name)
        assert result == "/config/app/config.yaml"


def test_get_config_content():
    mock_name = "config/0-success"
    port = setup_mock_server("test")
    os.environ["RANCHER_RUN_FOREVER"] = "false"
    os.environ["RANCHER_METADATA_HOST"] = "localhost:{}".format(port)
    with mock.patch('sys.argv', ["file_name", mock_name]):
        generator = generate.Generator()
        result = generator.get_config_content(mock_name)
        assert result == "content\n"


@mock.patch("os.makedirs")
@pytest.mark.parametrize("mock_name, path, makedir_path, content", success_cases)
def test_execute_case_0(mock_makedirs, mock_name, path, makedir_path, content):
    # Happy path
    port = setup_mock_server("test")
    os.environ["RANCHER_RUN_FOREVER"] = "false"
    os.environ["RANCHER_METADATA_HOST"] = "localhost:{}".format(port)
    with mock.patch('sys.argv', ["file_name", mock_name]):
        mock_open = mock.mock_open()
        with mock.patch("builtins.open", mock_open, create=True):
            generator = generate.Generator()
            generator.execute()

            mock_makedirs.assert_called_with(makedir_path, exist_ok=True)
            mock_open.assert_called_once_with(path, "w")
            handle = mock_open()
            handle.write.assert_called_once_with(content)


def test_execute_case_1():
    # Host cannot be found, should exit
    mock_name = "config/0-success"
    os.environ["RANCHER_RUN_FOREVER"] = "false"
    os.environ["RANCHER_METADATA_HOST"] = "none"
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        with mock.patch('sys.argv', ["file_name", mock_name]):
            generator = generate.Generator()
            generator.execute()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


def test_execute_case_2():
    # 404 config key cannot be found, should exit
    mock_name = "config/2-404-key"
    port = setup_mock_server("test")
    os.environ["RANCHER_METADATA_HOST"] = "localhost:{}".format(port)
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        with mock.patch('sys.argv', ["file_name", mock_name]):
            generator = generate.Generator()
            generator.execute()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


def test_execute_case_3():
    # 500 error, should exit
    mock_name = "config/3-500-error"
    port = setup_mock_server("test")
    os.environ["RANCHER_METADATA_HOST"] = "localhost:{}".format(port)
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        with mock.patch('sys.argv', ["file_name", mock_name]):
            generator = generate.Generator()
            generator.execute()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
