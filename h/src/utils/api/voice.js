import axios from "axios";

axios.defaults.baseURL = "https://xw.uiuing.com/api";
// axios.defaults.baseURL = "http://localhost:7573/api";

const textToVoice = async (text, voiceType) => {
  const params = {
    text,
    voiceType,
  };
  const res = await axios.get("/voice/text", { params });
  return res.data;
};
const voiceToText = async (voiceBase64) => {
  const data = {
    voiceBase64,
  };
  const res = await axios.post("/voice/voice", data);
  return res.data;
};

export { textToVoice, voiceToText };
