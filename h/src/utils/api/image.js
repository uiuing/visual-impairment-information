import axios from "axios";

axios.defaults.baseURL = "https://xw.uiuing.com/api";
// axios.defaults.baseURL = "http://localhost:7573/api";

const imgToText = async (imgBase64) => {
  const data = {
    imgBase64,
  };
  const res = await axios.post("/image/text", data);
  return res.data.result;
};

export default imgToText;
