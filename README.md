# Gizwits for Home Assistant

[简体中文](README.zh-Hans.md)

A Home Assistant custom integration for Gizwits-based devices.

The current implementation has been tested in a real Home Assistant setup with a Zhuohu smart meter. The integration supports a configurable Gizwits `app_id`, so it can be adapted to other Gizwits-based apps and devices as well.

The default `app_id` in the config flow is the Zhuohu-tested one. If your device belongs to another Gizwits app ecosystem, replace it with the correct `app_id` for that app.

It is a `cloud_polling` integration.
It does not use a local LAN protocol.

## Features

Current meter-oriented entities:

- active power
- reactive power
- current
- voltage
- frequency
- energy
- power factor

## Verified devices

The following devices or app ecosystems have been validated with the current integration:

- Zhuohu smart meter
- Zhuohu app ecosystem with the default bundled `app_id`

If you are using another Gizwits-based app or hardware vendor, you can still try this integration by replacing the `app_id` during setup.

## Install

### HACS custom repository

1. Push this repository to a public GitHub repository.
2. In Home Assistant, open `HACS -> Integrations -> Custom repositories`.
3. Add your GitHub repository URL.
4. Select `Integration`.
5. Install `Gizwits`.
6. Restart Home Assistant.
7. Go to `Settings -> Devices & Services -> Add Integration`.
8. Search for `Gizwits`.

### Manual install

Copy `custom_components/gizwits` into your Home Assistant `custom_components` directory, then restart Home Assistant.

## Configure

Open the `Gizwits` integration in Home Assistant and enter:

- app account username
- password
- app ID
- optional `did`
- optional device name
- scan interval

If `did` is omitted, the integration will try to fetch the device list automatically.
If the device list is empty for your account, first verify that you are using the correct Gizwits `app_id` for that app ecosystem, then use a known `did` directly if needed.

## Energy Dashboard

Use the `Energy` entity from this integration as a source in the Home Assistant Energy dashboard.
It is exposed with:

- `device_class: energy`
- `state_class: total_increasing`
- `unit_of_measurement: kWh`

## Repository layout

- `custom_components/gizwits`: Home Assistant custom integration

## Publish checklist

Before publishing, make sure you do not commit:

- real usernames
- passwords
- real `did` values
- Home Assistant database files
- local debug exports

Repository:

- [johnnysuns/gizwits_home](https://github.com/johnnysuns/gizwits_home)

## HACS

There are two ways users can find it in HACS.

### 1. HACS custom repository

Any public GitHub repository that meets the HACS requirements can be added manually by URL in:

`HACS -> Integrations -> Custom repositories`

That is the fastest path and usually how new integrations start.

### 2. HACS default store listing

To appear in the default HACS catalog without manual repository entry, you still need to:

- keep the repository public on GitHub
- keep the standard `custom_components/<domain>` layout
- include `hacs.json`
- pass the HACS GitHub Action
- pass `hassfest`
- create at least one GitHub Release
- add integration brand assets
- submit a PR to `hacs/default`

## References

- [HACS general requirements](https://hacs.xyz/docs/publish/start/)
- [HACS integration requirements](https://hacs.xyz/docs/publish/integration/)
- [HACS include in default store](https://hacs.xyz/docs/publish/include/)
- [Gizwits OpenAPI](https://docs.gizwits.com/zh-cn/Cloud/openapi_apps.html)
- [Hassbian article](https://bbs.hassbian.com/thread-19326-1-1.html)
