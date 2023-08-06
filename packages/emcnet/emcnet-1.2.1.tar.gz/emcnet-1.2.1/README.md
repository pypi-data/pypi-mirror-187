# EMCNet
Energy Monitoring and Control Network
EMCNet is a Cloud-Edge IoT infrastructure that is flexible, configurable, and tolerant to communication loss.

This package contains the core central components of EMCNet.  Most of this code
is
1. intended to run on a central server within the EMCNet HQ LAN (or in the cloud in the future 
   if/when scalability becomes an issue), or
2. provide epcnet-specific utilities to device, edge, or gateway packages

Other packages such as `bigbird` contain the files that run at the device, edge, 
or gateway-level but are compatible with EMCNet.

![EMCNet Diagram](docs/img/emcnet_diagram.png)

## Installation

### Hardware

EMCNet is being designed to accommodate many different site configurations,
each with a different site ID, but the first use case is that of a camper van with a lithium battery and
solar generator.  The first test site ID `bigbird`.

To measure current and voltage, we need some hardware.  In the case of the first EMCNet
test site, BigBird, the needed hardware is an INA226 chip and a serial USB connection to a Victron MPPT 
solar/battery charge controller.  A shematic of BigBird elecrical system is as follows:

![EMCNet Diagram](docs/img/BigBird-Electrical-System-II.png)

The main part of the electrical system of BigBird is pictured below, along with a view of the
control panel.

![EMCNet Diagram](docs/img/photo_electrical_system.png)

![EMCNet Diagram](docs/img/photo_electrical_panel.png)


For the INA226, BigBird uses a module that can be purchased 
from Amazon [here](https://www.amazon.com/gp/product/B07PMNQ2DQ).  I followed 
[this](https://github.com/MarioAriasGa/raspberry-pi-ina226) guide to
get it working.

### Software - Raspberry Pi

First, set up the RPi with one of the Raspian OS distros.  There are many online tutorials for this.
I usually:
1. Install Raspian Lite to the SD card using the Raspberry Pi Imager for MacOS
2. Add the empty file "ssh" to the root (boot) directory on the SD card (you can use TextEdit)
3. Insert the SD card into the Raspberry Pi
4. Install a USB newtork dongle into the pi and connect it directly to your router.  Alternately, insert the
   SD card into another computer, and create `wpa_supplicant.conf` file in the root directory of it.
   Then, insert it into the Pi.
5. Boot the Pi
6. From your PC, `ssh pi@raspberrypi.local` and log in with the default password `raspberry`
7. Update the OS
    ```
    sudo apt-get update
    sudo apt-get dist-upgrade
    ```
7. Change the account password for user `pi` using the command `passwd`
8. Add a user account for yourself and add yourself to the important groups:
    ```
    sudo adduser <your username>
    sudo usermod newuser_name -a -G pi,adm,dialout,cdrom,sudo,audio,video,plugdev,games,users,input,netdev,spi,i2c,gpio
    ```
9. If you like, you can change the `sudoers` file so members of the `sudo` group can do `sudo` without re-entering 
their password each time. 
Run `sudo visudo` and make sure the line `%sudo   ALL=(ALL:ALL) NOPASSWD:ALL` appears.
10. Run `raspi-config` and make the following changes:
    1. In Network Options, set localization and log onto the local wifi network
    2. In Network Options, change the hostname if you like
    3. In Interfacing Options, turn on SSH and I2C
11. It is also recommended to make sure the HDMI port is turned off - it is not needed in the BigBird application.
    ```
    sudo /opt/vc/bin/tvservice -o
    ```
12. Reboot - `sudo reboot`
13. SSH wirelessly and edit the `wpa-supplicant.conf` file to add other wireless networks:
    ```
    ssh <your username>@<new hostname>.local
    sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
    ```
    After, the `wpa_supplicant.conf` file should look something like this:
    ```
    ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
    update_config=1
    country=US
    autoscan=periodic:10
    
    network={
            ssid="CasaFife"
            psk="<password1>" 
    }
    
    network={
            ssid="DENBend"
            psk="<password2>"
    }
    
    network={
            ssid="Fife's Pixel"
            psk="<password3>"
    }

    network={
            ssid="MikeEnelXBigBird"
            psk="<password4>"
    }
    ```

During the process above, be sure to remember the new password for user `pi` to something you will remember.  
And you may want to create
a new account and use that for most of your work.  That way, if things go wrong (I have accidentally lost `sudo` 
privileges for example) you can go back to the pi account and recover more quickly by creating a new account 
from there.

Python 3 comes pre-installed on Raspian.  But for running BigBird on a Raspberry Pi, there are some dependencies:
```
sudo apt-get install -y python3-pip python3-dev libatlas3-base
sudo apt-get install -y mosquitto mosquitto-clients
```

Installing `mosquitto` as above is fine but versions prior to 1.6.9 have a bug that prevents the
proper caching of messages and persistence when communications over a bridge is lost.  To build and
install a newer version of `mosquitto`, follow 
[this](https://github.com/bapowell/bapowell.github.io/wiki/Mosquitto-Build-Notes-(Linux)) guide.
except:
1. Dont worry about installing websockets
2. Download the latest source from https://mosquitto.org/download/
3. Also install `libcjson` with `sudo apt install libcjson1 libcjson-dev` 
4. Alsi install `systemd` dev library with `sudo apt-get install libsystemd-dev`
5. In the `config.mk` file, set WITH_TLS:=no, WITH_TLS_PSK:=no, WITH_SRV:=no, and WITH_SYSTEMD:=yes
6. `make`
7. Copy files
   ```
   cd src
   sudo cp mosquitto /usr/sbin
   
   ```
8. Change permissions on the PID file location:
    ```
    sudo mkdir -m 755 /var/run/mosquitto
    sudo chown mosquitto /var/run/mosquitto
    ``` 
9. Create a new /etc/mosquitto/mosquitto.conf:
    ```
    listener 1883
    protocol mqtt
    pid_file /var/run/mosquitto/mosquitto.pid
    include_dir /etc/mosquitto/conf.d
    ```
10. Make sure the service file /lib/systemd/system/mosquitto.service is something like this, 
    noting the dynamic addition of the mosquitto directory on startup:
    ```
    [Unit]
    Description=Mosquitto MQTT v3.1/v3.1.1 Broker
    Documentation=http://mosquitto.org/documentation/
    After=network-online.target
    Wants=network-online.target
    
    [Service]
    Type=notify
    NotifyAccess=main
    ExecStart=/usr/sbin/mosquitto -c /etc/mosquitto/mosquitto.conf
    ExecStartPre=/bin/mkdir -m 740 -p /var/run/mosquitto
    ExecStartPre=/bin/chown mosquitto: /var/run/mosquitto
    Restart=on-failure
    
    [Install]
    WantedBy=multi-user.target
    ```
11. Remove the old persistence database if it exists: `sudo rm /var/lib/mosquitto/mosquitto.db`
12. Enable the service with `sudo systemctl enable mosquitto.service`

Activate the `mosquitto` mqtt server on the "gateway" which is also the same RPi we are using for data collection and 
run it in verbose mode to test it:
```
sudo systemctl enable mosquitto.service
mosquitto -v
mosquitto_sub -t "testtopic"
mosquitto_pub -t "testtopic" -m "test message"
```

Next, we want to set up the server MQTT broker.  First, set up a password file
following [this](http://www.steves-internet-guide.com/mqtt-username-password-example/) link.
(NOTE, however, if we are using a mosquitto broker built from source that does not include TLS, then
DO NOT ENCRYPT THE PASSWORD FILE ON THE SERVER.) 
Then, round out the mosquitto config file in `/etc/mosquitto/conf.d`:
```
listener 1883
protocol mqtt
pid_file /var/run/mosquitto/mosquitto.pid
include_dir /etc/mosquitto/conf.d

# require password to access server broker
allow_anonymous false
password_file /etc/mosquitto/mosquitto_pw_encrypted.txt       

# log to syslog
log_dest syslog
log_facility 0
log_timestamp false
```

Next, we want to set up the site MQTT broker.
To do this, create a mew mosquitto config file in `/etc/mosquitto/conf.d` with the following content:
```
persistence true
persistence_location /var/lib/mosquitto/

connection bridge-to-emcnet
address jmfife.com:1883
topic emcnet/intervaldata/# out 2
topic emcnet/devicedata/# out 0
remote_username <here, use the user id you set up for the emcnet server broker>
remote_password <here, use the password you set up for the emcnet server broker>

max_inflight_messages 1
max_queued_messages 6000
autosave_interval 300

# log to syslog
log_dest syslog
log_facility 0
log_timestamp false
```
Or, copy the file in the repo named `mosquitto_site.conf` to the directory `/etc/mosquitto/conf.d`.
Be careful that none of the values in `mosquitto_site.conf` have already been set in `/etc/mosquitto/mosquitto.conf`
which is read first when mosquitto starts. 
If parameters are already set, and your config file tries to set them again, `mosquitto.service` will not 
start correctly. Check the service is started with `systemctl status mosquitto.service`.  If it is stopped or there 
is an error, check logs with `journalctl -u mosquitto.service`.

We still need to make the site computer automatically start the right processes during boot.
But see below for setting up autostart of the necessary processes on a linux computer with systemd.

#### User

If you are just using bigbird, follow these directions to install it.
Make a projects directory and install Bigbird directly from the GitHub repo:
```
mkdir ~/projects
cd ~/projects
git clone git@github.com:jmfife/rpi-ina226.git
cd vedirect
python3 -m pip install -e .
python3 -m pip install git+https://github.com/jmfife/bigbird"
```
The package `vedirect-jmfife` should also install automatically.

#### Developer

If you are helping to develop bigbird, follow these directions.

First set up password-less access via SSH.  Follow this script to create SSH RSA keys: 
https://www.raspberrypi.org/documentation/remote-access/ssh/passwordless.md
If you already have a key generated on your PC, just use:
```
ssh-copy-id <USERNAME>@<IP-ADDRESS>
```
Also log into GitHub, go to settings, and copy and paste your public keys (in `~/.ssh/id_rsa.pub`) from both
the RPi and your PC.

Set up `git`:
```
sudo apt-get install git
git config --global user.name "<your name>"
git config --global user.email "<your email address>"
git config --global core.editor nano
```
Then you can clone the `bigbird` and `vedirect-jmfife` project to the RPi and install it as an editable package:
```
mkdir ~/projects
cd ~/projects
git clone git@github.com:jmfife/rpi-ina226.git
cd vedirect
python3 -m pip install -e .
cd ..
git clone git@github.com:jmfife/vedirect.git
cd vedirect
python3 -m pip install -e .
cd ..
git clone git@github.com:jmfife/bigbird.git
cd bigbird
python3 -m pip install -e .
```

You may also want to install some other developer-oriented packages.  For example:
```
sudo apt install emacs
```

And you may want to set up rsub to edit files on the RPi from Sublime Text 3 on MacOS by following this 
[LINK](https://www.pkshiu.com/loft/2016/12/remote-file-editing-on-the-raspberry-pi-using-sublime-text-3-and-iterm).

Set auto-start as services with systemd.  Follow [THIS GUIDE](https://github.com/torfsen/python-systemd-tutorial).
The .service files are included in the distro so you can, in short:
``` 
cp emcnet/service/*.service ~/.config/systemd/user
systemctl --user enable emcnet_dashboard
systemctl --user start emcnet_dashboard
systemctl --user enable emcnet_device_ina226
systemctl --user start emcnet_device_ina226
systemctl --user enable emcnet_device_vmppt
systemctl --user start emcnet_device_vmppt
systemctl --user enable emcnet_site_data_processor
systemctl --user start emcnet_site_data_processor
```
Or, for the server:
``` 
cp emcnet/service/*.service ~/.config/systemd/user
systemctl --user enable emcnet_dashboard
systemctl --user start emcnet_dashboard
systemctl --user enable emcnet_server_data_store
systemctl --user start emcnet_server_data_store
```
Then, importantly, the command to make the services start when the system boots 
(even though you are not logged in) is:
```
sudo loginctl enable-linger $USER
```
You can list unit files with:
```
systemctl --user list-unit-files
```
And you can disable unit files with `systemctl --user disable <unit>`.
And you can restart unit files wthat have changed with `systemctl --user restart <unit>`
To reload all units after they have changed: `systemctl --user daemon-reload` but the services need
to be stopped first.

For viewing log files, use `journalctl --user-unit <unit name>`.  For example:
```
journalctl --user-unit emcnet_server_data_store.service -f
```

## EMCNet Configuration

The command line utilities in `emcnet` can be configured in 3 different ways:
 
1. With environment variables
   
2. Using a `config.env` file in the path $EMCNETDIR which will over-ride (1)

3. Using command line options which will override (2)

The recommended installation process utilizes the `config.env` file:

1. Create a folder in `<a user home directory>/emcnet`.  This will be where EMCNet will keep all of
   its files.
   
2. In the site's .bashrc or equivalent, create the environment variable EMCNETDIR and set it equal to the
   path the directory you just created. For example:
   ```
   export EMCNETDIR=/home/jmfife/emcnet
   ```
3. In `EMCNETDIR` create a `config.env` file.  Within it, at a minimum, if its a site, set `SITE_ID` to the 
   name of the site. For example:
   ```
   # Unique site identifier (string)
   # Not used by server
   SITE_ID=bb8
   
   # Address of MQTT broker
   MQTT_BROKER_ADDRESS=localhost
   
   # MQTT broker port
   MQTT_BROKER_PORT=1883
   
   # Loging level from one of [DEBUG, INFO, WARNING, ERROR, CRITICAL]
   LOG_LEVEL=INFO
   
   # Number of intervals per hour to be accumulated by the Interval Manager
   # Not used by server
   INTERVALS_PER_HOUR=4
   
   # Number of time-series records to plot in the web dashboard
   MAX_PLOT_RECORDS=672
   
   # Credentials for remote broker (server)
    REMOTEBROKERID=<here, use the user id you set up for the emcnet server broker>
    REMOTESERVERPW=<here, use the password you set up for the emcnet server broker>
   ```

## Example

### Set up Raspberry Pi in BigBird

For connecting the existing Pi Zero in bigbird, if there is no connected WiFi, remove the SIM card and create two files in the root directory:  one blank one named 'ssh' and one 'wpa_supplicant.conf' file with the following contents:

```
    ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
    update_config=1
    country=US
    autoscan=periodic:10
    
    network={
            ssid="<SSID>"
            psk="<password>" 
    }
```

Then, reboot and you should see it connected by going to the router page and checking the list of connected devices.  Then, from a mac connected to the same network, you should be able to ssh into the RPi Zero with

```
ssh bigbird.local
```

If you don't have access to the router web page, you can try using nmap.  For example, see https://all3dp.com/2/find-raspberry-pi-on-network/#:~:text=Open%20a%20command%20line%20or,re%20using%20Raspberry%20Pi%20OS.

Once the Pi Zero is connecte, it should be publishing a dashboard visible on the mac at http://bigbird.local:8050/emcnet/bigbird

### Debugging

#### Logs

First `ssh` into bigbird's Pi Zero.

One option for increasing the logging is to set the `LOG_LEVEL` environment variable in config.env in the directory `~/emcnet'.

Another option is to edit the systemd unit files in `~/.config/systemd/user`.  For example, you can edit `emcnet_device_ina226.service` and add `--loglevel=DEBUG` in the option list of the call to `device_data_publisher`.

Reboot.

For reading logs, you can use something like:

```
journalctl --user-unit emcnet_device_ina226.service
```

### Installing influxdb

#### In native environment

Follow https://docs.influxdata.com/influxdb/v2.5/install/

For MacOS:

```
brew update 
brew install influxdb
brew install influxdb-cli
```

Create a configuration for each database you want to connect to.

```
influx config create --config-name influxdbcloud \
    --host-url https://europe-west1-1.gcp.cloud2.influxdata.com \
    --org jmfife@gmail.com \
    --token FcSL3TvxLBanhkZFw1GdT7f3SnNaiCHeU4idhIEXOQX6KE0Omz670NTH85J-z_Qlw0-26tkRPmeXrEZW_Jr4iA== \
    --active
```

Note that the `influx config create -o` parameter must be the organization NAME, not ID.

But for some reason, even when this config is active, you must continuously re-enter the token on the command line.  
You can avoid re-entering the API token by setting the environment variable `INFLUX_TOKEN=<your all-access API token>`.  For example:

```
jmfife@mse-6:~/projects/emcnet$ export INFLUX_HOST=https://europe-west1-1.gcp.cloud2.influxdata.com
jmfife@mse-6:~/projects/emcnet$ export INFLUX_TOKEN=FcSL3TvxLBanhkZFw1GdT7f3SnNaiCHeU4idhIEXOQX6KE0Omz670NTH85J-z_Qlw0-26tkRPmeXrEZW_Jr4iA==
jmfife@mse-6:~/projects/emcnet$ export INFLUX_ORG=jmfife@gmail.com

jmfife@mse-6:~/projects/emcnet$ influx bucket list
ID			Name		Retention	Shard group duration	Organization ID		Schema Type
a0cb9f17ee606c13	_monitoring	168h0m0s	n/a			9aea191806c5168c	implicit
d1c4a94317a90cb1	_tasks		72h0m0s		n/a			9aea191806c5168c	implicit
82ab5a630f3633ff	test		720h0m0s	n/a			9aea191806c5168c	implicit
```

#### A Great InfluxDB IOT Example

Follow https://www.influxdata.com/blog/influxdb-iot-edge-historian/ except there seems to be an issue with the way the options are represented in the example.  So use the short notation and replace all of the existing dashes in the copy-paste with normal dashes:

```
$ influx config create -a -n "edge" -u "https://localhost:8086" -o "flyinion" -t "teydRew_qE4Z00uqRPFcuYoS-XERvv0Qd4aXSgqaciR-gBS_MBms8IGlNRk5wOrfMlpYXbJrVS7XpFHNp6wmNw=="
```

Similarly for the Telegraf config:

```
$ telegraf --config ./telegraf.conf
```

Similarly for the cloud config:

```
$ influx config create -a -n "cloud" -o "jmfife@gmail.com" -u "http://europe-west1-1.gcp.cloud2.influxdata.com" -t "Ybth0xrDDZLM7mH3X1_EAX2Wr8ilq_IJFLYd87kFOJ2fwrV_KgXnAvuclKGhzvk5ONB30B4oDMuIn5cNIHuHTw=="
```

Local (edge) InfluxDB event "aggregate" that aggregates high speed data and stores it locally in "northbound" bucket:

```
import "influxdata/influxdb/tasks"
import "influxdata/influxdb/secrets"

option task = {name: "aggregate_local", every: 1m}

from(bucket: "devices")
    |> range(start: tasks.lastSuccess(orTime: -1h))
    |> aggregateWindow(every: 1m, fn: mean, createEmpty: false)
    |> to(bucket: "northbound")
```

And finally, a Local (edge) InfluxDB event "sync_northbound" that synchronizes northbound bucket with cloud InfluxDB:

```
import "influxdata/influxdb/tasks"
import "influxdata/influxdb/secrets"

option task = { 
  name: "sync_northbound",
  every: 5m,
  offset: 0s
}

cloud_host = secrets.get(key: "cloud_host")
cloud_org = secrets.get(key: "cloud_org")
cloud_token = secrets.get(key: "cloud_token")

from(bucket: "northbound")
    |> range(start: tasks.lastSuccess(orTime: -1h))
    |> set(key: "edge_id", value: "001")
    |> to(host: cloud_host, org: cloud_org, token: cloud_token, bucket: "edge_devices")
```

Tokens: 

test token for edge docker influxdb (jmfife's token (cloned...)) : `teydRew_qE4Z00uqRPFcuYoS-XERvv0Qd4aXSgqaciR-gBS_MBms8IGlNRk5wOrfMlpYXbJrVS7XpFHNp6wmNw==`

test token on influxdb cloud
`Ybth0xrDDZLM7mH3X1_EAX2Wr8ilq_IJFLYd87kFOJ2fwrV_KgXnAvuclKGhzvk5ONB30B4oDMuIn5cNIHuHTw==`

Second clound token (needed to access new bucket device_data):
`RQVnjw2fgf0gCXsb0W9drJA6rlW2jIIRP1rZAx2hqvRMPw-tmAD__Pk0MOmGUzlB4NsgRRt738HdLjDxYQdFIw==`

# InfluxDB Branch - Setting Up

## BigBird Setup

Burn a new "lite" OS image to an SD card by downloading and installing the RPI imager:  https://www.raspberrypi.com/software/.  In the imager app, be sure to go to settings before burning the image and set up user IDs, WiFi, etc.

SSH into bigbird and run `raspi-config` and ensure the following settings:
    1. In Network Options, set localization and log onto the local wifi network
    2. In Network Options, change the hostname if you like
    3. In Interfacing Options, turn on SSH and I2C

```
sudo /opt/vc/bin/tvservice -o
```

Reboot - `sudo reboot`
    
Install InfluxDB 2.6 and set it up.  Follow https://portal.influxdata.com/downloads/

```
$ cd Downloads
$ wget -q https://repos.influxdata.com/influxdb.key
$ echo '23a1c8836f0afc5ed24e0486339d7cc8f6790b83886c4c96995b88a061c5bb5d influxdb.key' | sha256sum -c && cat influxdb.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/influxdb.gpg > /dev/null
$ echo 'deb [signed-by=/etc/apt/trusted.gpg.d/influxdb.gpg] https://repos.influxdata.com/debian stable main' | sudo tee /etc/apt/sources.list.d/influxdata.list
$ sudo apt-get update
$ sudo apt-get install influxdb2
$ sudo systemctl unmask influxdb
$ sudo systemctl enable influxdb
$ sudo service influxdb start
```

Now, influxdb should start on boot.

Go to http://bigbird.local:8086/ and set up user credentials.  Set Org to "flyinion."  Be sure to save the API access token so you don't need to create another one.

Install Mosquitto:

```
$ sudo apt-get install -y mosquitto mosquitto-clients
$ sudo systemctl unmask mosquitto.service
$ sudo systemctl enable mosquitto.service
```

Prereqeuisites:

```
$ sudo apt install git python3-pip
```

Create a new SSH public key and save it to Github:

```
$ ssh-keygen
$ more ~/.ssh/id_rsa.pu
```

<!-- Install WiringPi:

```
$ mkdir ~/projects
$ cd ~/projects
$ git clone https://github.com/WiringPi/WiringPi.git
$ cd WiringPi
$ ./build
``` -->

Now load the custom software we will be running on the Pi.  

```
$ sudo apt install python3-pip
$ sudo python3 -m pip install --upgrade pip
$ cd ~/projects
$ git clone git@github.com:jmfife/emcnet.git
$ sudo mkdir /etc/emcnet
$ sudo cp emcnet/config_example.env /etc/emcnet/config.env
$ sudo cp emcnet/services/* /lib/systemd/system/
$ sudo python3 -m pip install emcnet --upgrade emcnet
```

Create a configuration for accessing the cloud database from the influx command line:
```
$ influx config create -a -n "cloud" -o "jmfife@gmail.com" -u "http://europe-west1-1.gcp.cloud2.influxdata.com" -t Ybth0xrDDZLM7mH3X1_EAX2Wr8ilq_IJFLYd87kFOJ2fwrV_KgXnAvuclKGhzvk5ONB30B4oDMuIn5cNIHuHTw==
```

Go to the edge instance of InfluxDB at http://bigbird.local:8086/ and create a new all-access token.  Copy and save it, and put it in the following command:
```
$ influx config create -a -n "edge" -u "http://localhost:8086" -o "flyinion" -t PlbtNY3Lvm_PVPrYW6UUbc3PqIPH9r8wiZwpGBnotzFxb6Js8_f28p1bb0ZUhJYgxT4v4c9ws1Hh7cIEEC82NQ==
```

Load the edge InfluxDB template in the emcnet/influxdb folder:

```
$ cd ~/projects/emcnet/influxdb
$ influx apply -f edge_template.yml
```

Edit the emcnet configuration file and put the same token in there, along with the site name:
```
$ sudo nano /etc/emcnet/config.env
```

Exit nano with ^O and ^W.

Set the InfluxDB edge instance's secret key values to access the cloud, and to set the site name:

```
$ influx secret update --key cloud_host --value "https://europe-west1-1.gcp.cloud2.influxdata.com"
$ influx secret update --key cloud_org --value "jmfife@gmail.com"
$ influx secret update --key cloud_token --value "Ybth0xrDDZLM7mH3X1_EAX2Wr8ilq_IJFLYd87kFOJ2fwrV_KgXnAvuclKGhzvk5ONB30B4oDMuIn5cNIHuHTw=="
$ influx secret update --key site --value "bigbird"
```

NOTE ABOVE, the cloud host url must have https://..., but the edge host must be http://....

Activate the device services:

```
$ cd ~/projects/emcnet
$ sudo cp service/*.service /lib/systemd/system/
$ sudo systemctl unmask emcnet_device_vmppt
$ sudo systemctl enable emcnet_device_vmppt
$ sudo systemctl start emcnet_device_vmppt
$ sudo systemctl unmask emcnet_device_ina226
$ sudo systemctl enable emcnet_device_ina226
$ sudo systemctl start emcnet_recorder
$ sudo systemctl unmask emcnet_recorder
$ sudo systemctl enable emcnet_recorder
$ sudo systemctl start emcnet_recorder
```

Reboot the raspberry pi and you should be good to go.
