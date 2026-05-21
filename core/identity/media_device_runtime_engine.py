from __future__ import annotations

from typing import Any, Dict, List

_DEVICES = {
    "default": {
        "audio_inputs": ["Default Microphone"],
        "video_inputs": ["Integrated Camera"],
        "audio_outputs": ["Default Speakers"],
    },
    "profile_a": {
        "audio_inputs": ["MacBook Microphone"],
        "video_inputs": ["FaceTime HD Camera"],
        "audio_outputs": ["MacBook Speakers"],
    },
    "profile_b": {
        "audio_inputs": ["USB Audio Device"],
        "video_inputs": ["HD Pro Webcam"],
        "audio_outputs": ["HDMI Output"],
    },
}


def build_media_device_runtime(profile_id: str = "default") -> Dict[str, Any]:
    profile = profile_id if profile_id in _DEVICES else "default"
    data = _DEVICES[profile]

    return {
        "audio_inputs": list(data["audio_inputs"]),
        "video_inputs": list(data["video_inputs"]),
        "audio_outputs": list(data["audio_outputs"]),
        "bounded": True,
    }
