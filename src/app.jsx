import { useState, useEffect } from 'react';
import { MBot } from "mbot-js-api";

function isDeepEqual(data1, data2) {
  if (data1 === data2) {
    return true;
  }

  if (!data1 || !data2) {
    return false;
  }

  if (data1.length !== data2.length) {
    return false;
  }

  const chs1 = data1.map((item, index) => (item.channel));
  const chs2 = data2.map((item, index) => (item.channel));

  for (const key of chs1) {
    if (!chs2.includes(key)) {
      return false;
    }
  }

  for (const key of chs2) {
    if (!chs1.includes(key)) {
      return false;
    }
  }

  return true;
}


function ChannelStatus({channel, dtype}) {
  return (
    <tr>
      <td>{channel}</td>
      <td>{dtype}</td>
      <td>tmp</td>
      <td>tmp</td>
    </tr>
  )
}


function ChannelList({ channels }) {
    if (!channels) {
      return null;
    }
    return (
      <>
        {channels.map((item, index) => (
          <ChannelStatus key={index} channel={item.channel} dtype={item.dtype}/>
        ))}
      </>
    )
}

const mbotIP = window.location.host.split(":")[0]  // Grab the IP from which this page was accessed.
const mbot = new MBot(mbotIP);


export default function LCMMonitorApp() {
  const [channels, setChannels] = useState(null);

  // This lets the React App start and cleanup the timer properly.
  useEffect(() => {
    // Check for new channels every 2 seconds.
    const timerId = setInterval(() => {
      mbot.readChannels((chs) => {
        // Update the channels only if the have changed to prevent a rerender.
        if (!isDeepEqual(channels, chs)) {
          setChannels(chs);
        }
      });
    }, 2000);

    // Return the cleanup function which stops the rerender.
    return () => clearInterval(timerId);
  }, [channels, setChannels]);

  return (
    <div className="container">
      <h2 className="mt-5">Status</h2>
      <table className="table table-striped mt-3">
        <thead className="thead-dark">
          <tr>
            <th>Channel</th>
            <th>Type</th>
            <th>Rate</th>
            <th>Total Messages</th>
          </tr>
        </thead>
        <tbody id="status-table-body">
            <ChannelList channels={channels}/>
        </tbody>
      </table>

      <div id="decoded-messages" className="mt-5">
        {/* <!-- Decoded messages will be dynamically inserted here --> */}
      </div>
    </div>
  );
}

// document.addEventListener("DOMContentLoaded", function() {
//     // var socket = io();
//     // socket.on('status_update', function(status) {
//     //     document.getElementById('status-table-body').innerHTML = generateStatusHTML(status.status);
//     //     document.getElementById('decoded-messages').innerHTML = generateDecodedMessagesHTML(status.decoded_status);
//     // });

//     function generateStatusHTML(status) {
//         let html = '';
//         status.forEach(function(item) {
//             html += `<tr>
//                 <td>${item.channel}</td>
//                 <td>${item.type}</td>
//                 <td>${item.rate.toFixed(2)}</td>
//                 <td>${item.total_messages}</td>
//             </tr>`;
//         });
//         return html;
//     }

//     function generateDecodedMessagesHTML(decoded_status) {
//         let html = '';
//         decoded_status.forEach(function(decoded) {
//             html += `<div class="card mb-3">
//                         <div class="card-header">
//                             ${decoded.channel}
//                         </div>
//                         <div class="card-body">`;
//             decoded.decoded_message.forEach(function(line) {
//                 html += `<pre>${line}</pre>`;
//             });
//             html += `  </div>
//                      </div>`;
//         });
//         return html;
//     }
// });