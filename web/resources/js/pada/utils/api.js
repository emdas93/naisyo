import axios from "axios";

export const fetchRooms = async (channelId) => {
  try {
    const response = await axios.post("http://localhost/api/chat/get-rooms", { channel_id: channelId });
    return response.data.success ? response.data.rooms : [];
  } catch (error) {
    console.error("방 가져오기 에러:", error);
    return [];
  }
};

export const fetchMessages = async (roomId) => {
  try {
    const response = await axios.post("http://localhost/api/chat/get-messages", { room_id: roomId });
    return response.data.status === "success" ? response.data.messages : [];
  } catch (error) {
    console.error("메시지 가져오기 에러:", error);
    return [];
  }
};

export const sendMessageToRoom = async (roomId, message) => {
  try {
    await axios.post("http://localhost/api/chat/send-message", { room_id: roomId, message });
  } catch (error) {
    console.error("메시지 전송 에러:", error);
  }
};
