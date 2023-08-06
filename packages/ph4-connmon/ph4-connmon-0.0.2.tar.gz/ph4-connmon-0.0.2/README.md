# Connection monitoring

Simple tool to monitor the health of SSH tunnels.

## Use case
Assume you have several SSH tunnels set up from your home network to a remote server with a public IPv4, so you can easily reach back to your private network from the internet.

This monitoring tool can periodically tests health of the SSH tunnels and notifies you over Telegram or Email (or both) if anything changes, e.g., tunnel is not usable (e.g., in a case of connectivity loss in your home network or tunneled host being down / unresponsive).

## Setup

- pip-install this package `pip install -U ph4-connmon`
- Configure `config.json` according to [assets/config-example.json](assets/config-example.json)
- Configure notification channels, either 
  - [Telegram bot](https://www.teleme.io/articles/create_your_own_telegram_bot?hl=en) 
  - or Email sender (e.g., [Gmail](https://www.lifewire.com/get-a-password-to-access-gmail-by-pop-imap-2-1171882)) or both
- Run `assets/install.sh` to install `ph4connmon.service` systemd service
- Run `systemctl start ph4connmon.service`

## Notification examples

```
Status: nas-ssh @ 127.0.0.1:3022 - ssh over ssh, open: True (0x), app: SSH-2.0-OpenSSH_8.2, 0.12s
nas-web @ 127.0.0.1:2001 - https over ssh, open: True (0x), app: True, 0.02s
rpi-ssh @ 127.0.0.1:1022 - ssh over ssh, open: True (0x), app: SSH-2.0-OpenSSH_8.2, 0.03s, 2.19 s old
```

Telegram bot supports also several commands, e.g., `/status` and `/full_status`, to which it responds with current state. You can manually request status information and to check that system is responsive.

Note that Email notifier sends only state changes, while Telegram notifier sends also regular state updates when UPS is running on the battery.
If email user is empty, email notifier is not use. Likewise, if bot API key is empty, telegram is not used.

## Dependencies
This project uses monitoring tool library https://github.com/ph4r05/ph4-monitlib
