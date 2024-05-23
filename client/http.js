import "regenerator-runtime/runtime";
import axios from "axios";

export const addCoordinate = async (payload) => {
  try {
    await axios.post("http://127.0.0.1:105/api/data", payload);
    alert("Kordinat terkirim");
  } catch (error) {
    console.log(error);
  }
};
