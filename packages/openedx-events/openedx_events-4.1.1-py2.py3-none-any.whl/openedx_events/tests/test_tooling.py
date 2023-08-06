"""
This file contains all test for the tooling.py file.

Classes:
    EventsToolingTest: Test events tooling.
"""
from contextlib import contextmanager
from unittest.mock import Mock, patch

import attr
import ddt
import pytest
from django.test import TestCase, override_settings

from openedx_events.exceptions import SenderValidationError
from openedx_events.tests.utils import FreezeSignalCacheMixin
from openedx_events.tooling import OpenEdxPublicSignal


@contextmanager
def receivers_attached(signal, receivers):
    """
    Attach the receivers to the signal for the duration of the context.
    """
    try:
        for receiver in receivers:
            signal.connect(receiver)

        yield
    finally:
        for receiver in receivers:
            signal.disconnect(receiver)


@ddt.ddt
class OpenEdxPublicSignalTestCache(FreezeSignalCacheMixin, TestCase):
    """
    Test cases for Open edX events base class.
    """

    def setUp(self):
        """
        Setup common conditions for every test case.
        """
        super().setUp()
        self.event_type = "org.openedx.learning.session.login.completed.v1"
        self.user_mock = Mock()
        self.data_attr = {
            "user": Mock,
        }
        self.public_signal = OpenEdxPublicSignal(
            event_type=self.event_type,
            data=self.data_attr,
        )

        self.receiver_error = Exception("fake error")

        def error_receiver(*args, **kwargs):
            raise self.receiver_error

        self.ok_receiver = Mock(return_value="success")
        self.error_receiver = error_receiver

    def test_string_representation(self):
        """
        This methods checks the string representation for events base class.

        Expected behavior:
            The representation contains the event_type.
        """
        self.assertIn(self.event_type, str(self.public_signal))

    def test_get_signal_by_type(self):
        """
        Test found and not-found behavior.
        """
        assert isinstance(
            OpenEdxPublicSignal.get_signal_by_type('org.openedx.learning.session.login.completed.v1'),
            OpenEdxPublicSignal
        )

        with pytest.raises(KeyError):
            OpenEdxPublicSignal.get_signal_by_type('xxx')

    @override_settings(SERVICE_VARIANT="lms")
    @patch("openedx_events.data.openedx_events")
    @patch("openedx_events.data.socket")
    def test_get_signal_metadata(self, socket_mock, events_package_mock):
        """
        This methods tests getting the generated metadata for an event.

        Expected behavior:
            Returns the metadata containing information about the event.
        """
        events_package_mock.__version__ = "0.1.0"
        socket_mock.gethostname.return_value = "edx.devstack.lms"
        expected_metadata = {
            "event_type": self.event_type,
            "minorversion": 0,
            "source": "openedx/lms/web",
            "sourcehost": "edx.devstack.lms",
            "sourcelib": [0, 1, 0],
        }

        metadata = self.public_signal.generate_signal_metadata()

        self.assertDictContainsSubset(expected_metadata, attr.asdict(metadata))

    @patch("openedx_events.tooling.OpenEdxPublicSignal.generate_signal_metadata")
    @patch("openedx_events.tooling.Signal.send")
    def test_send_event_successfully(self, send_mock, fake_metadata):
        """
        This method tests the process of sending an event that's allow to fail.

        Expected behavior:
            The event is sent as a django signal with send method.
        """
        expected_metadata = Mock(some_data="some_data")
        fake_metadata.return_value = expected_metadata
        self.public_signal.allow_send_event_failure()

        self.public_signal.send_event(user=self.user_mock)

        send_mock.assert_called_once_with(
            sender=None,
            user=self.user_mock,
            metadata=expected_metadata,
        )

    @patch("openedx_events.tooling.OpenEdxPublicSignal.generate_signal_metadata")
    @patch("openedx_events.tooling.log", autospec=True)
    @patch("openedx_events.tooling.format_responses", autospec=True, return_value="fake-output")
    def test_send_robust_event_successfully(self, format_responses_mock, log_mock, fake_metadata):
        """
        This method tests the process of sending an event that won't crash.

        Expected behavior:
            The event is sent as a django signal with send_robust method.
        """
        expected_metadata = Mock(some_data="some_data")
        fake_metadata.return_value = expected_metadata

        with receivers_attached(self.public_signal, [self.ok_receiver, self.error_receiver]):
            self.public_signal.send_event(user=self.user_mock)

        self.ok_receiver.assert_called_once_with(
            signal=self.public_signal, sender=None, user=self.user_mock, metadata=expected_metadata
        )
        # format_responses is mocked out because its output is
        # complicated enough to warrant its own set of tests.
        format_responses_mock.assert_called_once_with(
            [(self.ok_receiver, "success"), (self.error_receiver, self.receiver_error)], depth=2
        )
        log_mock.info.assert_called_once_with(
            "Responses of the Open edX Event <org.openedx.learning.session.login.completed.v1>: \nfake-output"
        )

    @ddt.data(
        (
            {"student": Mock()},
            "SenderValidationError org.openedx.learning.session.login.completed.v1: "
            "Missing required argument 'user'",
        ),
        (
            {"user": {"student": Mock()}},
            "SenderValidationError org.openedx.learning.session.login.completed.v1: "
            "The argument 'user' is not instance of the Class Attribute 'type'",
        ),
        (
            {"student": Mock(), "user": Mock()},
            "SenderValidationError org.openedx.learning.session.login.completed.v1: "
            "There's a mismatch between initialization data and send_event arguments",
        ),
    )
    @ddt.unpack
    def test_invalid_sender(self, send_arguments, exception_message):
        """
        This method tests sending an event with invalid setup on the sender
        side.

        Expected behavior:
            A SenderValidationError exception is raised.
        """
        with self.assertRaisesMessage(SenderValidationError, exception_message):
            self.public_signal.send_event(**send_arguments)

    def test_send_event_with_django(self):
        """
        This method tests sending an event using the `send` built-in Django
        method.

        Expected behavior:
            A warning is showed advicing to use Open edX events custom
            send_signal method.
        """
        message = "Please, use 'send_event' when triggering an Open edX event."

        with self.assertWarns(Warning, msg=message):
            self.public_signal.send(sender=Mock())

    def test_send_robust_event_with_django(self):
        """
        This method tests sending an event using the `send` built-in Django
        method.

        Expected behavior:
            A warning is showed advicing to use Open edX events custom
            send_signal method.
        """
        message = "Please, use 'send_event' with send_robust equals to True when triggering an Open edX event."

        with self.assertWarns(Warning, msg=message):
            self.public_signal.send_robust(sender=Mock())

    @patch("openedx_events.tooling.Signal.send")
    def test_send_event_disabled(self, send_mock):
        """
        This method tests sending an event that has been disabled.

        Expected behavior:
            The Django Signal associated to the event is not sent.
        """
        self.public_signal.disable()

        result = self.public_signal.send_event(sender=Mock())

        send_mock.assert_not_called()
        self.assertListEqual([], result)
