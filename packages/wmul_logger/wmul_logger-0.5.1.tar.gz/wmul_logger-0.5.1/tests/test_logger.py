"""
@Author = 'Mike Stanley'

Test cases for wmul_logger.logger

============ Change Log ============
2022-May-06 = Changed License from MIT to GPLv2.

2018-Apr-16 = Created.

============ License ============
Copyright (c) 2018, 2022 Michael Stanley

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""
import pytest
from collections import namedtuple


def test_uninitialized__logger_is_none():
    """The field _logger should be None before setup or get is called."""
    import wmul_logger.logger as wl
    assert not wl._loggers


def test_initialized__logger_is_not_none():
    """After setup_logger is called, _logger should no longer be None."""
    import wmul_logger.logger as wl
    wl.setup_logger()
    assert wl._loggers


def test_get_logger_returns_a_logger():
    """
    Running get_logger when there is not already a logger should return a logger. _logger should be None before the
    method is called and not None after.
    """
    import wmul_logger.logger as wl
    l = wl.get_logger()
    assert bool(l)
    assert wl._loggers


def test_get_logger_returns_same_logger():
    """Multiple calls to get_logger should return the same logger."""
    import wmul_logger
    log1 = wmul_logger.get_logger()
    log2 = wmul_logger.get_logger()
    assert log1 is log2


def test_setup_logger_returns_a_logger():
    """A call to setup_logger should return a logger."""
    import wmul_logger
    log = wmul_logger.setup_logger()
    assert log


def test_setup_logger_returns_same_logger():
    """Multiple calls to setup_logger with no arguments should return the same logger."""
    import wmul_logger
    log1 = wmul_logger.setup_logger()
    log2 = wmul_logger.setup_logger()
    assert log1 is log2


def test_setup_logger_and_get_logger_return_same_logger():
    """Calling setup_logger and then get_logger should return the same logger."""
    import wmul_logger
    log1 = wmul_logger.setup_logger()
    log2 = wmul_logger.get_logger()
    assert log1 is log2


def test_get_logger_and_setup_logger_return_same_logger():
    """Calling get_logger and then setup_logger should return the same logger."""
    import wmul_logger
    log2 = wmul_logger.get_logger()
    log1 = wmul_logger.setup_logger()
    assert log1 is log2


def test_critical_log_message_goes_to_stdout(capsys):
    """
    GIVEN that setup_logger is called without arguments.
    WHEN a CRITICAL log message is created.
    THEN the log message goes to stdout.
    """
    import wmul_logger
    log1 = wmul_logger.setup_logger()
    critical_message = "This is a critical test message."
    log1.critical(critical_message)
    out, err = capsys.readouterr()
    assert critical_message in out


def test_non_critical_log_message_does_not_go_to_stdout(capsys, standard_messages):
    """
    GIVEN that setup_logger is called with a out arguments.
    WHEN an INFO or lesser log message is created.
    THEN the log message does not go to stdout.
    """
    import wmul_logger
    log1 = wmul_logger.setup_logger()
    log1.info(standard_messages.info_message)
    out, err = capsys.readouterr()
    assert standard_messages.info_message not in out


@pytest.fixture(scope="function")
def standard_messages():
    s_m = namedtuple(
        "Standard_Messages",
        [
            "critical_message",
            "error_message",
            "warning_message",
            "info_message",
            "debug_message"
        ]
    )
    return s_m(
        critical_message="This is a critical test message.",
        error_message="This is an error test message.",
        warning_message="This is a warning test message.",
        info_message="This is an info test message.",
        debug_message="This is a debug test message."
    )


def test_setup_logger_with_level(standard_messages, capsys):
    """
    GIVEN that setup_logger is called with a level argument of 2.
    WHEN an INFO or greater log message is created.
    THEN the log message goes to stdout.
    """
    import wmul_logger
    log1 = wmul_logger.setup_logger(log_level=20)

    log1.critical(standard_messages.critical_message)
    log1.error(standard_messages.error_message)
    log1.warning(standard_messages.warning_message)
    log1.info(standard_messages.info_message)
    log1.debug(standard_messages.debug_message)

    out, err = capsys.readouterr()

    expected = [
        standard_messages.critical_message,
        standard_messages.error_message,
        standard_messages.warning_message,
        standard_messages.info_message
    ]

    for expec in expected:
        assert expec in out

    assert standard_messages.debug_message not in out


def test_setup_logger_with_log_name(tmpdir, capsys, standard_messages):
    """
    GIVEN that setup_logger is called with a log name arg.
    WHEN a CRITICAL log entry is made.
    THEN the log message goes to the file and to stdout.
    """
    import wmul_logger
    log_file_name = tmpdir.join("logfile.txt")
    log1 = wmul_logger.setup_logger(file_name=log_file_name)
    log1.critical(standard_messages.critical_message)

    log_contents = log_file_name.read()
    stdout, err = capsys.readouterr()

    assert standard_messages.critical_message in log_contents
    assert standard_messages.critical_message in stdout


def test_setup_logger_with_log_name_and_level_only_warning_and_above_goes_to_stdout(tmpdir, capsys,
                                                                                    standard_messages):
    """
    GIVEN that setup_logger is called with a log name arg and a level less than WARNING.
    WHEN a WARNING or higher log entry is made.
    THEN the log message goes to the file and to stdout.
    WHEN a lesser entry is made
    THEN the log message only goes to the file.
    """
    import wmul_logger
    log_file_name = tmpdir.join("logfile.txt")
    log1 = wmul_logger.setup_logger(file_name=log_file_name, log_level=10)

    log1.critical(standard_messages.critical_message)
    log1.error(standard_messages.error_message)
    log1.warning(standard_messages.warning_message)
    log1.info(standard_messages.info_message)
    log1.debug(standard_messages.debug_message)

    log_contents = log_file_name.read()
    stdout, err = capsys.readouterr()

    assert standard_messages.critical_message in log_contents
    assert standard_messages.error_message in log_contents
    assert standard_messages.warning_message in log_contents
    assert standard_messages.info_message in log_contents
    assert standard_messages.debug_message in log_contents

    assert standard_messages.critical_message in stdout
    assert standard_messages.error_message in stdout
    assert standard_messages.warning_message in stdout
    assert standard_messages.info_message not in stdout
    assert standard_messages.debug_message not in stdout


def test_setup_logger_with_different_names_returns_different_loggers():
    # GIVEN that setup_logger is called twice with two different log names
    # THEN The loggers that are returned are not the same
    import wmul_logger
    log1 = wmul_logger.setup_logger(log_name="Foo")
    log2 = wmul_logger.setup_logger(log_name="Bar")
    assert log1 is not log2


def test_loggers_with_different_names_and_file(tmpdir, standard_messages):
    # GIVEN two loggers with different names, Foo set to CRITICAL, and Bar set to WARNING.
    # WHEN Foo is logged Error,
    # THEN nothing is emitted to stdout.
    # WHEN Bar is logged Error,
    # THEN it is emitted to stdout.
    import wmul_logger
    foo_file = tmpdir.join("foo.log")
    bar_file = tmpdir.join("bar.log")
    foo = wmul_logger.setup_logger(file_name=foo_file, log_level=50, log_name="Foo")
    bar = wmul_logger.setup_logger(file_name=bar_file, log_level=30, log_name="Bar")
    foo_error = standard_messages.error_message + "Foo "
    bar_error = standard_messages.error_message + "Bar "
    foo.error(foo_error)
    bar.error(bar_error)

    foo_file_contents = foo_file.read()
    bar_file_contents = bar_file.read()

    assert foo_error not in foo_file_contents
    assert bar_error in bar_file_contents


def test_setup_logger_and_get_logger_return_same_logger_with_same_name():
    # GIVEN that setup_logger is called with a name,
    # WHEN get_logger is called with the same name,
    # THEN the loggers are the same.
    import wmul_logger
    log1 = wmul_logger.setup_logger(log_name="foo")
    log2 = wmul_logger.get_logger(log_name="foo")

    assert log1 is log2
