import { useState, useEffect } from 'react';


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


function ChannelData({ data, indent = 0 }) {
  function formatArray(array, indentLevel, maxLength = 12) {
    if (array.length > maxLength) {
      const halfMax = Math.floor(maxLength / 2);
      array = [...array.slice(0, halfMax), " ... ", ...array.slice(-halfMax)];
    }
    const formattedArray = array.map((item, index) => {
      if (Array.isArray(item)) {
        return `Array(${item.length})`;
      } else if (typeof item === 'object' && item !== null) {
        return `{...}`;
      } else if (typeof item === 'number') {
        return Number.isInteger(item) ? item : item.toFixed(4);
      } else if (typeof item === 'string') {
        return item;
      } else {
        return JSON.stringify(item);
      }
    });

    return (
      <div style={{ marginLeft: `${(indentLevel + 1) * 20}px` }}>
        [{formattedArray.join(', ')}]
      </div>);
  };

  function formatValue(value, indentLevel) {
    if (Array.isArray(value)) {
      return formatArray(value, indentLevel);
    } else if (typeof value === 'object' && value !== null) {
      return (
        <div style={{ marginLeft: `${indentLevel * 20}px` }}>
          <ChannelData data={value} indent={indentLevel + 1} />
        </div>
      );
    } else if (typeof value === 'number') {
        return <span>{Number.isInteger(value)? value : value.toFixed(4)}</span>;
    }
    return <span>{JSON.stringify(value)}</span>;
  };

  return (
    <div>
      {Object.keys(data).map((key) => (
        <div key={key} style={{ marginLeft: `${indent * 20}px` }}>
          <strong>{key}:</strong> {formatValue(data[key], indent)}
        </div>
      ))}
    </div>
  );
}


function ChannelStatus({ channel, dtype, mbot }) {
  const [lcmData, setData] = useState({});
  const [count, setCount] = useState(0);
  const [open, setOpen] = useState(false);

  // This lets the React App start and cleanup the subscriber properly.
  useEffect(() => {
    // Subscribe to the data.
    mbot.subscribe(channel, (msg) => {
      setCount(count => count + 1);
      setData(msg.data);
    }).catch((error) => {
      console.error('Subscription failed for channel', channel, error);
    });

    // Return the cleanup function which stops the rerender.
    return () => {
      mbot.unsubscribe(channel).catch((err) => console.warn(err));
    }
  }, []);

  return (
    <>
    <tr onClick={() => setOpen(!open)}>
      <td>{channel}</td>
      <td>{dtype}</td>
      <td>tmp</td>
      <td>{count}</td>
    </tr>
    {open && (
      <tr className="lcm-data-row">
        <td colSpan="4">
          <ChannelData data={lcmData} />
        </td>
      </tr>
    )}
    </>
  )
}


function ChannelList({ channels, mbot }) {
    if (!channels) {
      return null;
    }
    return (
      <>
        {channels.map((item, index) => (
          <ChannelStatus key={index} channel={item.channel} dtype={item.dtype} mbot={mbot}/>
        ))}
      </>
    )
}


export default function LCMMonitorApp({ mbot }) {
  const [channels, setChannels] = useState(null);
  const [hostname, setHostname] = useState("mbot-???");
  const [connected, setConnected] = useState(false);

  // This lets the React App start and cleanup the timer properly.
  useEffect(() => {
    let timerId = null;

    // Read the hostname. Start the timer to read the channels only if reading
    // the hostname throws no errors.
    mbot.readHostname().then((name) => {
      setHostname(name);
      if (!connected) setConnected(true);

      // Check for new channels every 2 seconds.
      timerId = setInterval(() => {
        mbot.readChannels().then((chs) => {
          // Update the channels only if the have changed to prevent a rerender.
          if (!isDeepEqual(channels, chs)) {
            setChannels(chs);
          }
        }).catch((err) => {
          console.warn(err);
          // If we failed to read the channels, set as disconnected.
          if (connected) setConnected(false);
          if (channels) setChannels(null);
        });
      }, 2000);
    }).catch((err) => {if (connected) setConnected(false)});

    // Return the cleanup function which stops the rerender.
    return () => {if (timerId) clearInterval(timerId)};
  }, [channels, setChannels, hostname, setHostname, connected, setConnected]);

  return (
    <div className="container">
      <div className="status-bar">
        <h2>{hostname.toUpperCase()}</h2>
        <span className={"status " + (connected ? "valid" : "invalid")}>
          {connected ? "Connected" : "Not Connected"}
        </span>
      </div>

      <table className="table mt-3">
        <thead className="thead-dark">
          <tr>
            <th>Channel</th>
            <th>Type</th>
            <th>Rate</th>
            <th>Total Messages</th>
          </tr>
        </thead>
        <tbody id="status-table-body">
            <ChannelList channels={channels} mbot={mbot}/>
        </tbody>
      </table>
    </div>
  );
}
