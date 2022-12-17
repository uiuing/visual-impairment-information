import { textToVoice } from "../api/voice";

let voiceAudio;

const play = () => {
  voiceAudio = document.getElementById("voiceAudio");
  voiceAudio.play();
};
const pause = () => {
  voiceAudio = document.getElementById("voiceAudio");
  voiceAudio.pause();
};

const init = async (text, voiceType) => {
  voiceAudio = document.getElementById("voiceAudio");
  voiceAudio.src = "/";
  const res = await textToVoice(text, voiceType);
  voiceAudio.src = `data:audio/x-wav;base64,${res}`;
  voiceAudio.play();
};

export { init, pause, play };
