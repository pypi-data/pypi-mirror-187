"""
@Author = 'Mike Stanley'

Test cases for multiprocess logging.

============ Change Log ============
2022-May-06 = Changed License from MIT to GPLv2.

2018-Sep-04 = Created.

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
import multiprocessing
import wmul_logger


def test_multiprocess_logging(tmpdir):
    log_file = tmpdir.join("logfile.log")

    logging_queue = multiprocessing.Queue()

    stop_logger = wmul_logger.run_queue_listener_logger(
        logging_queue=logging_queue,
        file_name=log_file,
        log_level=wmul_logger.DEBUG
    )

    logger = wmul_logger.get_queue_handler_logger(logging_queue=logging_queue)

    critical_message = "This is a critical log message."
    error_message = "This is a error log message."
    warning_message = "This is a warning log message."
    info_message = "This is a info log message."
    debug_message = "This is a debug log message."

    logger.critical(critical_message)
    logger.error(error_message)
    logger.warning(warning_message)
    logger.info(info_message)
    logger.debug(debug_message)

    stop_logger()

    log_contents = log_file.read()

    assert critical_message in log_contents
    assert error_message in log_contents
    assert warning_message in log_contents
    assert info_message in log_contents
    assert debug_message in log_contents
