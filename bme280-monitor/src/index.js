const UI = activate require("@syndicate-lang/driver-browser-ui");
// @jsx UI.html
// @jsxFrag UI.htmlFragment

// const { Bytes } = require("@syndicate-lang/core");
const { WSServer, ToServer, FromServer, ServerConnected } = activate require("@syndicate-lang/server/lib/client");

assertion type BME280(host, timestamp, temperature, pressure, humidity);

spawn {
  const url = 'wss://steam.eighty-twenty.org/syndicate';
  const scope = 'test';
  const addr = WSServer(url, scope);

  const ui = new UI.Anchor();
  assert ui.html('body',
                 <table id="main">
                   <thead>
                     <tr>
                       <th>Measurement device ID</th>
                       <th>Timestamp</th>
                       <th>Temperature</th>
                       <th>Pressure</th>
                       <th>Humidity</th>
                     </tr>
                   </thead>
                   <tbody>
                   </tbody>
                 </table>);

  during ServerConnected(addr) {
    during FromServer(addr, BME280($host, _, $temperature, $pressure, $humidity)) {
      const now = new Date();
      assert ui.context(host).html('#main tbody',
                                   <tr>
                                     <td>{host}</td>
                                     <td>{now.toTimeString().split(/ +/)[0]}</td>
                                     <td>{temperature.value.toFixed(1)}</td>
                                     <td>{pressure.value.toFixed(1)}</td>
                                     <td>{humidity.value.toFixed(1)}</td>
                                   </tr>);
    }
  }
}
