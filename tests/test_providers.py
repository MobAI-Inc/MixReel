import json
from pathlib import Path
import tempfile
import unittest

from providers.base import ProviderError, VideoRequest
from providers.minimax_video import MiniMaxVideo
from providers.seedance_video import SeedanceVideo
from providers.workflow import init_journal, prepare_and_submit


def scripted(responses):
    calls = []

    def transport(method, url, headers, body, timeout):
        calls.append({"method": method, "url": url, "body": body, "headers": headers})
        status, payload = responses.pop(0)
        raw = payload if isinstance(payload, bytes) else json.dumps(payload).encode()
        return status, {}, raw

    transport.calls = calls
    return transport


class MiniMaxTests(unittest.TestCase):
    def test_text_request_matches_the_public_create_shape(self):
        transport = scripted([(200, {"task_id": "task-1"})])
        client = MiniMaxVideo("MiniMax-H3", api_key="test-key", transport=transport)
        task_id = client.submit(VideoRequest(
            prompt="A bottle turns on a table.", model="MiniMax-H3",
            duration=5, resolution="2K", ratio="9:16",
        ))
        self.assertEqual(task_id, "task-1")
        sent = json.loads(transport.calls[0]["body"])
        self.assertEqual(sent["model"], "MiniMax-H3")
        self.assertEqual(sent["content"], [{"type": "text", "text": "A bottle turns on a table."}])
        self.assertEqual(sent["resolution"], "2K")
        self.assertNotIn("test-key", json.dumps(sent))
        self.assertTrue(transport.calls[0]["url"].endswith("/v2/video_generation"))

    def test_first_frame_and_reference_cannot_mix(self):
        client = MiniMaxVideo("MiniMax-H3", api_key="test-key", transport=scripted([]))
        with self.assertRaises(ProviderError):
            client.submit(VideoRequest(
                prompt="Hold the label.", model="MiniMax-H3", duration=5, resolution="768P", ratio="9:16",
                references=[
                    {"kind": "image", "role": "first_frame", "url": "https://cdn.example/a.png"},
                    {"kind": "image", "role": "reference_image", "url": "https://cdn.example/b.png"},
                ],
            ))

    def test_text_ratio_cannot_be_adaptive(self):
        client = MiniMaxVideo("MiniMax-H3", api_key="test-key", transport=scripted([]))
        with self.assertRaises(ProviderError):
            client.submit(VideoRequest(
                prompt="A bottle.", model="MiniMax-H3", duration=5, resolution="768P", ratio="adaptive",
            ))

    def test_status_reads_content_url(self):
        transport = scripted([(200, {"task": {"status": "succeeded", "content": {"url": "https://cdn.example/out.mp4"}}})])
        client = MiniMaxVideo("MiniMax-H3", api_key="test-key", transport=transport)
        status = client.status("task-1")
        self.assertEqual(status.state, "succeeded")
        self.assertEqual(status.video_url, "https://cdn.example/out.mp4")

    def test_missing_key_is_refused(self):
        with self.assertRaises(ProviderError):
            MiniMaxVideo("MiniMax-H3", api_key="", transport=scripted([]))


class SeedanceTests(unittest.TestCase):
    def test_reference_audio_on_2_0_needs_a_picture(self):
        client = SeedanceVideo("doubao-seedance-2-0-260128", api_key="test-key", transport=scripted([]))
        with self.assertRaises(ProviderError):
            client.submit(VideoRequest(
                prompt="Use this voice.", model="doubao-seedance-2-0-260128",
                duration=5, resolution="720p", ratio="9:16",
                references=[{"kind": "audio", "role": "reference_audio", "url": "https://cdn.example/a.mp3"}],
            ))

    def test_2_5_can_send_audio_alone(self):
        transport = scripted([(200, {"id": "cgt-1"})])
        client = SeedanceVideo("dreamina-seedance-2-5-260628", api_key="test-key",
                               base_url="https://ark.ap-southeast.bytepluses.com/api/v3", transport=transport)
        task_id = client.submit(VideoRequest(
            prompt="A short product line.", model="dreamina-seedance-2-5-260628",
            duration=5, resolution="720p", ratio="9:16", generate_audio=True,
            references=[{"kind": "audio", "role": "reference_audio", "url": "https://cdn.example/a.mp3"}],
        ))
        self.assertEqual(task_id, "cgt-1")
        self.assertIn("bytepluses.com", transport.calls[0]["url"])
        sent = json.loads(transport.calls[0]["body"])
        self.assertEqual(sent["generate_audio"], True)
        self.assertEqual(sent["content"][1]["role"], "reference_audio")

    def test_unknown_model_is_refused_until_the_caller_overrides(self):
        client = SeedanceVideo("my-future-model", api_key="test-key", transport=scripted([]))
        with self.assertRaises(ProviderError):
            client.submit(VideoRequest(
                prompt="A bottle.", model="my-future-model", duration=5, resolution="720p", ratio="9:16",
            ))

    def test_status_reads_video_url_and_maps_expired(self):
        transport = scripted([(200, {"id": "cgt-1", "status": "expired", "content": {}})])
        client = SeedanceVideo("doubao-seedance-2-5-260628", api_key="test-key", transport=transport)
        status = client.status("cgt-1")
        self.assertEqual(status.state, "failed")
        self.assertEqual(status.raw_state, "expired")

    def test_download_returns_a_digest(self):
        transport = scripted([(200, b"video-bytes")])
        client = SeedanceVideo("doubao-seedance-2-5-260628", api_key="test-key", transport=transport)
        with tempfile.TemporaryDirectory() as tmp:
            info = client.download("https://cdn.example/out.mp4", Path(tmp) / "out.mp4")
        self.assertEqual(info["bytes"], len(b"video-bytes"))
        self.assertEqual(len(info["sha256"]), 64)


class JournalWorkflowTests(unittest.TestCase):
    def test_submit_records_the_task_and_does_not_retry_after_a_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "journal.json"
            init_journal(path, {"USD": "10.00"})

            class Client:
                name = "minimax"
                model = "MiniMax-H3"
                calls = 0

                def submit(self, request):
                    self.calls += 1
                    if self.calls == 1:
                        raise ProviderError("timeout")
                    return "should-not-run"

            client = Client()
            request = VideoRequest(
                prompt="A bottle.", model="MiniMax-H3", duration=5, resolution="768P", ratio="9:16",
            )
            with self.assertRaises(ProviderError):
                prepare_and_submit(client, request, path, "job-1", "USD", "1.00", "user approved one render")
            data = json.loads(path.read_text())
            self.assertEqual(data["jobs"]["job-1"]["state"], "outcome_unknown")
            with self.assertRaises(ValueError):
                prepare_and_submit(client, request, path, "job-2", "USD", "1.00", "retry")
            self.assertEqual(client.calls, 1)


if __name__ == "__main__":
    unittest.main()
