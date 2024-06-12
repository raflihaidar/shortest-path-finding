import axios from "https://cdn.jsdelivr.net/npm/axios@1.3.5/+esm";

export const addCoordinate = async (payload) => {
  try {
    let response = await axios.post("http://127.0.0.1:105/api/data", payload);
    return response.data.route;
  } catch (error) {
    console.log(error);
  }
};
