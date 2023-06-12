// import { io } from "socket.io-client";

// //export let socket = io("http://211.117.84.151:8083",{ transports: ['websocket', 'polling', 'flashsocket']  });
// export let socket = io("http://localhost:8083",{ transports: ['websocket', 'polling', 'flashsocket']  });
// export const initSocketConnection = () => {
//   if (socket) return;
//   socket.connect();
// };

// // 이벤트 명을 지정하고 데이터를 보냄
// export const sendSocketMessage = (cmd, body = null) => {
//   if (socket == null || socket.connected === false) {
//     initSocketConnection();
//   }
//   io.emit("message",{"data":cmd})

//   socket.emit("my_room_event", {
//     cmd: cmd,
//     body: body,
//   });
// };

// let cbMap = new Map();

// // 해당 이벤트를 받고 콜백 함수를 실행함
// export const socketInfoReceived = (cbType, cb) => {
//   cbMap.set(cbType, cb);
  
//   if (socket.hasListeners("message")) {
//     socket.off("message");
//   }

//   socket.on("message", ret => {
//     for (let [, cbValue] of cbMap) {
//       cbValue(null, ret);
//     }
//   });

//   socket.on("TEST",function(data){
//     console.log(data);
//   })
// };

// // 소켓 연결을 끊음
// export const disconnectSocket = () => {
//   if (socket == null || socket.connected === false) {
//     return;
//   }
//   socket.disconnect();
//   socket = undefined;
// };