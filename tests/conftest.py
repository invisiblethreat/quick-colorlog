"""
Pytest configuration for quick-colorlog tests.

This file contains shared fixtures and configuration for all tests.
"""

import logging

import pytest

from quick_colorlog import reset_colors


@pytest.fixture(autouse=True)
def clean_logging_state():
    """
    Automatically clean logging state before and after each test.

    This fixture ensures that each test starts with a clean logging state
    and doesn't interfere with other tests.
    """
    # Setup: Clean state before test
    _reset_all_logging()

    yield  # Run the test

    # Teardown: Clean state after test
    _reset_all_logging()


def _reset_all_logging():
    """Reset all logging state to a clean state."""
    # Reset our colorized logging
    reset_colors()

    # Clear all handlers from root logger
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
        handler.close()

    # Reset root logger level
    root_logger.setLevel(logging.WARNING)

    # Clear any named loggers that might have been created
    # Note: Python's logging module doesn't provide a way to completely
    # clear all loggers, but we can at least clear their handlers
    logger_dict = logging.Logger.manager.loggerDict.copy()
    for name, logger in logger_dict.items():
        if isinstance(logger, logging.Logger):
            for handler in logger.handlers[:]:
                logger.removeHandler(handler)
                handler.close()
            logger.setLevel(logging.NOTSET)
            logger.propagate = True


@pytest.fixture
def capture_logs():
    """
    Fixture to capture log output for testing.

    Returns a function that can be used to get log output as a string.
    """
    import io

    from quick_colorlog import init_colors

    log_stream = io.StringIO()
    init_colors(output=log_stream, level=logging.DEBUG)

    def get_logs():
        return log_stream.getvalue()

    return get_logs


@pytest.fixture
def sample_logger():
    """
    Fixture that provides a pre-configured logger for testing.

    Returns a logger instance with colorized formatting.
    """
    import io

    from quick_colorlog import init_colors

    log_stream = io.StringIO()
    logger = init_colors(output=log_stream, level=logging.DEBUG)

    # Attach the stream to the logger for easy access in tests
    logger._test_stream = log_stream

    return logger


@pytest.fixture
def named_logger():
    """
    Fixture that provides a named logger for testing.

    Returns a named logger instance with colorized formatting.
    """
    import io

    from quick_colorlog import get_colorized_logger

    log_stream = io.StringIO()
    logger = get_colorized_logger(
        "test.fixture", output=log_stream, level=logging.DEBUG
    )

    # Attach the stream to the logger for easy access in tests
    logger._test_stream = log_stream

    return logger


# Test markers for organizing tests
def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line(
        "markers", "regression: mark test as a regression test for specific issues"
    )
    config.addinivalue_line(
        "markers", "double_logging: mark test as related to double logging issues"
    )
    config.addinivalue_line(
        "markers", "concurrency: mark test as related to concurrency/threading"
    )
    config.addinivalue_line(
        "markers", "cleanup: mark test as related to resource cleanup"
    )


# Custom assertion helpers
class LoggingAssertions:
    """Helper class for logging-related assertions."""

    @staticmethod
    def assert_single_occurrence(text, message, context="log output"):
        """Assert that a message appears exactly once in the text."""
        count = text.count(message)
        assert (
            count == 1
        ), f"Expected message '{message}' to appear once in {context}, but appeared {count} times"

    @staticmethod
    def assert_no_occurrence(text, message, context="log output"):
        """Assert that a message does not appear in the text."""
        assert (
            message not in text
        ), f"Expected message '{message}' to not appear in {context}, but it did"

    @staticmethod
    def assert_colorized_handler_count(logger, expected_count):
        """Assert the number of colorized handlers on a logger."""
        from quick_colorlog import ColorizedFormatter

        colorized_handlers = [
            h
            for h in logger.handlers
            if isinstance(h, logging.StreamHandler)
            and isinstance(h.formatter, ColorizedFormatter)
        ]
        actual_count = len(colorized_handlers)
        assert (
            actual_count == expected_count
        ), f"Expected {expected_count} colorized handlers, found {actual_count}"


@pytest.fixture
def logging_assertions():
    """Fixture that provides logging assertion helpers."""
    return LoggingAssertions() @ pytest.fixture


def logging_assertions():
    """Fixture that provides logging assertion helpers."""
    return LoggingAssertions()
