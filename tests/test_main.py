import unittest
from unittest.mock import Mock, patch, MagicMock
from pynput import keyboard


class TestPushToTalkBehavior(unittest.TestCase):
    """Tests for push-to-talk hotkey behavior (hold to record, release to stop)."""

    def setUp(self):
        """Set up test fixtures with mocked dependencies."""
        with patch('main.AudioRecorder'), \
             patch('main.AudioTranscriber'), \
             patch('main.TextInjector'), \
             patch('main.play_start_sound'), \
             patch('main.play_stop_sound'):
            from main import VoiceToTextApp
            self.app = VoiceToTextApp()
            self.app.recorder = Mock()
            self.app.transcriber = Mock()
            self.app.injector = Mock()

    def test_on_press_starts_recording_when_not_recording(self):
        """Pressing the hotkey should start recording if not already recording."""
        self.app.is_recording = False

        with patch('main.play_start_sound'):
            self.app.on_press(keyboard.Key.cmd_r)

        self.assertTrue(self.app.is_recording)
        self.app.recorder.start.assert_called_once()

    def test_on_press_does_not_start_if_already_recording(self):
        """Pressing the hotkey should not restart recording if already recording."""
        self.app.is_recording = True
        self.app.recorder.start.reset_mock()

        self.app.on_press(keyboard.Key.cmd_r)

        self.assertTrue(self.app.is_recording)
        self.app.recorder.start.assert_not_called()

    def test_on_press_ignores_other_keys(self):
        """Pressing non-hotkey keys should not affect recording."""
        self.app.is_recording = False

        self.app.on_press(keyboard.Key.cmd_l)  # Left command, not right
        self.app.on_press(keyboard.Key.space)

        self.assertFalse(self.app.is_recording)
        self.app.recorder.start.assert_not_called()

    def test_on_release_stops_recording_when_recording(self):
        """Releasing the hotkey should stop recording and trigger transcription."""
        self.app.is_recording = True
        self.app.recorder.stop.return_value = Mock(__len__=lambda x: 1000)

        with patch('main.play_stop_sound'), \
             patch('main.threading.Thread') as mock_thread:
            self.app.on_release(keyboard.Key.cmd_r)

        self.assertFalse(self.app.is_recording)
        self.app.recorder.stop.assert_called_once()

    def test_on_release_does_nothing_when_not_recording(self):
        """Releasing the hotkey should do nothing if not recording."""
        self.app.is_recording = False

        self.app.on_release(keyboard.Key.cmd_r)

        self.assertFalse(self.app.is_recording)
        self.app.recorder.stop.assert_not_called()

    def test_on_release_ignores_other_keys(self):
        """Releasing non-hotkey keys should not affect recording."""
        self.app.is_recording = True

        self.app.on_release(keyboard.Key.cmd_l)
        self.app.on_release(keyboard.Key.space)

        self.assertTrue(self.app.is_recording)
        self.app.recorder.stop.assert_not_called()

    def test_full_push_to_talk_cycle(self):
        """Test complete push-to-talk cycle: press -> release."""
        self.app.is_recording = False
        self.app.recorder.stop.return_value = Mock(__len__=lambda x: 1000)

        # Press hotkey - should start recording
        with patch('main.play_start_sound'):
            self.app.on_press(keyboard.Key.cmd_r)

        self.assertTrue(self.app.is_recording)
        self.app.recorder.start.assert_called_once()

        # Release hotkey - should stop and transcribe
        with patch('main.play_stop_sound'), \
             patch('main.threading.Thread'):
            self.app.on_release(keyboard.Key.cmd_r)

        self.assertFalse(self.app.is_recording)
        self.app.recorder.stop.assert_called_once()


class TestRecordingStateManagement(unittest.TestCase):
    """Tests for recording state flag management."""

    def setUp(self):
        with patch('main.AudioRecorder'), \
             patch('main.AudioTranscriber'), \
             patch('main.TextInjector'), \
             patch('main.play_start_sound'), \
             patch('main.play_stop_sound'):
            from main import VoiceToTextApp
            self.app = VoiceToTextApp()
            self.app.recorder = Mock()
            self.app.transcriber = Mock()
            self.app.injector = Mock()

    def test_initial_state_is_not_recording(self):
        """App should start with is_recording=False."""
        self.assertFalse(self.app.is_recording)

    def test_start_recording_sets_flag_before_recorder_start(self):
        """is_recording should be True after start_recording."""
        with patch('main.play_start_sound'):
            self.app.start_recording()

        self.assertTrue(self.app.is_recording)

    def test_stop_recording_clears_flag(self):
        """is_recording should be False after stop_recording_and_transcribe."""
        self.app.is_recording = True
        self.app.recorder.stop.return_value = Mock(__len__=lambda x: 0)

        with patch('main.play_stop_sound'):
            self.app.stop_recording_and_transcribe()

        self.assertFalse(self.app.is_recording)


if __name__ == '__main__':
    unittest.main()
