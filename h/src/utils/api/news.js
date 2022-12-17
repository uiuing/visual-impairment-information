import axios from "axios";

axios.defaults.baseURL = "https://xw.uiuing.com/api";
// axios.defaults.baseURL = "http://localhost:7573/api";

const getCategoryNews = async (channel, num) => {
  const params = {
    channel,
    num,
  };
  const axiosResponse = await axios.get("/news/randomly", { params });
  return axiosResponse.data;
};

export default getCategoryNews;
