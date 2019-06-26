const UI = activate require("@syndicate-lang/driver-browser-ui");
// @jsx UI.html
// @jsxFrag UI.htmlFragment

const { WSServer, FromServer, ServerConnected } = activate require("@syndicate-lang/server/lib/client");

assertion type BME280(host, timestamp, temperature, pressure, humidity);

spawn {
  const addr = WSServer('wss://steam.eighty-twenty.org/syndicate', 'test');
  during ServerConnected(addr) {
    const ui = new UI.Anchor();
    during FromServer(addr, BME280($host, _, $temperature, $pressure, $humidity)) {
      assert ui.context(host).html('#main tbody',
                                   <tr>
                                     <td>{host}</td>
                                     <td>{(new Date()).toTimeString().split(/ +/)[0]}</td>
                                     <td>{temperature.value.toFixed(1)}</td>
                                     <td>{pressure.value.toFixed(1)}</td>
                                     <td>{humidity.value.toFixed(1)}</td>
                                   </tr>);
    }
  }
}
