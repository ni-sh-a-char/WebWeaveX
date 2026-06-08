/**
 * Converted from Python: core/identity/media_device_runtime_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

let _DEVICES: any = {"default": {"audio_inputs": ["Default Microphone"], "video_inputs": ["Integrated Camera"], "audio_outputs": ["Default Speakers"]}, "profile_a": {"audio_inputs": ["MacBook Microphone"], "video_inputs": ["FaceTime HD Camera"], "audio_outputs": ["MacBook Speakers"]}, "profile_b": {"audio_inputs": ["USB Audio Device"], "video_inputs": ["HD Pro Webcam"], "audio_outputs": ["HDMI Output"]}};
export function buildMediaDeviceRuntime(profile_id: any = "default"): any {
  var profile: any = (py.contains(_DEVICES, profile_id) ? profile_id : "default");
  var data: any = py.at(_DEVICES, profile);
  return {"audio_inputs": [...py.iter(py.at(data, "audio_inputs"))], "video_inputs": [...py.iter(py.at(data, "video_inputs"))], "audio_outputs": [...py.iter(py.at(data, "audio_outputs"))], "bounded": true};
}
