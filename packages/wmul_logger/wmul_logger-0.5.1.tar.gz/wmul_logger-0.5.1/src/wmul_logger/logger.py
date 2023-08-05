"""
@Author = 'Mike Stanley'

Logging wrapper.

============ Change Log ============
2022-May-06 = Changed License from MIT to GPLv2.

2017-Aug-18 = Created.

              Moved logging from Utilities to here.

============ License ============
Copyright (c) 2017, 2022 Michael Stanley

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
import logging
import logging.handlers
import sys

_loggers = {}
_queue_handler_loggers = {}


DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL


def get_logger(log_name=__name__):
    log = _loggers.get(log_name)
    if log:
        return log
    else:
        return setup_logger(log_name=log_name)


def setup_logger(file_name=None, log_level=logging.WARNING, log_name=__name__):
    this_logger = logging.getLogger(log_name)
    log_formatter = logging.Formatter(
        fmt="%(asctime)s | [%(levelname)s]\t[%(threadName)s]: %(module)s: %(funcName)s -> %(message)s"
    )
    stdout_handler = logging.StreamHandler(
        stream=sys.stdout
    )
    stdout_handler.setFormatter(log_formatter)

    if file_name:
        file_handler = logging.handlers.RotatingFileHandler(
            filename=file_name,
            maxBytes=1_048_576,
            backupCount=5
        )
        file_handler.setFormatter(log_formatter)
        file_handler.setLevel(log_level)
        this_logger.addHandler(file_handler)

        stdout_handler.setLevel(logging.WARNING)
    else:
        stdout_handler.setLevel(log_level)

    this_logger.addHandler(stdout_handler)
    this_logger.setLevel(logging.DEBUG)

    _loggers[log_name] = this_logger

    return this_logger


def run_queue_listener_logger(logging_queue, file_name=None, log_level=logging.WARNING):
    log_formatter = logging.Formatter(
        fmt="%(asctime)s | [%(levelname)s]\t[%(threadName)s]: %(module)s: %(funcName)s -> %(message)s"
    )
    stdout_handler = logging.StreamHandler(
        stream=sys.stdout
    )
    stdout_handler.setFormatter(log_formatter)

    if file_name:
        file_handler = logging.handlers.RotatingFileHandler(
            filename=file_name,
            maxBytes=1_048_576,
            backupCount=5
        )
        file_handler.setFormatter(log_formatter)
        file_handler.setLevel(log_level)
        stdout_handler.setLevel(logging.WARNING)
        handlers = [file_handler, stdout_handler]
    else:
        stdout_handler.setLevel(log_level)
        handlers = [stdout_handler]

    ql = logging.handlers.QueueListener(logging_queue, *handlers, respect_handler_level=True)
    ql.start()

    def stop_queue_listener():
        ql.stop()
    return stop_queue_listener


def get_queue_handler_logger(logging_queue=None, log_name=__name__):
    log = _queue_handler_loggers.get(log_name)
    if log:
        return log
    else:
        if logging_queue:
            return setup_queue_handler_logger(logging_queue=logging_queue, log_name=log_name)
        else:
            raise ValueError(f"No logger has been initialized with this name: {log_name}, and no queue was "
                             f"provided for the initialization of a logger with this name.")


def setup_queue_handler_logger(logging_queue, log_name=__name__):
    this_logger = logging.getLogger(log_name)
    this_logger.setLevel(DEBUG)
    queue_handler = logging.handlers.QueueHandler(logging_queue)
    this_logger.addHandler(queue_handler)
    _queue_handler_loggers[log_name] = this_logger

    return this_logger
