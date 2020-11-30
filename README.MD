# Home Server Raspberry Pi Zero DHT-11 Logger
This is a small companion project for [Home Server API](https://github.com/NoworksM/home-server-api) for a simple
codebase designed to run on a Raspberry Pi Zero to periodically log temperature and humidity to the API server using
a DHT-11 temperature/humidity sensor connected to the Pi Zero's GPIO port. 
  
For this all you need to do is setup a json config file containing the `pin` that the sensor is connected to, the
`hostname` of the server, and finally the `sensorId` and `secret` that you configured on the server. You can also
optionally configure a wait time inbetween

A small note on the unit tests is that they expect an instance of the server to be running at `http://localhost:8081`
and that you've preconfigured the `sensorId` and `secret` to be what is in the tests. Since this project is so small I
just created the unit tests there for simplicity sake.