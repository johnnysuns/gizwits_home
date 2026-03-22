# Gizwits for Home Assistant

A Home Assistant custom integration for Gizwits-based devices.

Home Assistant 的机智云设备自定义集成。

The current implementation has been tested in a real Home Assistant setup with a Zhuohu smart meter. The integration supports a configurable Gizwits `app_id`, so it can be adapted to other Gizwits-based apps and devices as well.

当前实现已在真实 Home Assistant 环境中配合卓虎智能电表验证通过。集成支持自定义 Gizwits `app_id`，因此也可以适配其他基于机智云的 App 和设备。

The default `app_id` in the config flow is the Zhuohu-tested one. If your device belongs to another Gizwits app ecosystem, replace it with the correct `app_id` for that app.

配置流程中的默认 `app_id` 是卓虎设备验证时使用的值。如果你的设备属于其他机智云 App 体系，请改成对应 App 的正确 `app_id`。

It is a `cloud_polling` integration.
It does not use a local LAN protocol.

这是一个 `cloud_polling` 集成。
它不使用本地局域网协议。

## Features

Current meter-oriented entities:

- active power
- reactive power
- current
- voltage
- frequency
- energy
- power factor

当前面向电表场景提供这些实体：

- 有功功率
- 无功功率
- 电流
- 电压
- 频率
- 电量
- 功率因数

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

### HACS 自定义仓库

1. 将此仓库推送到公开的 GitHub 仓库。
2. 在 Home Assistant 中打开 `HACS -> Integrations -> Custom repositories`。
3. 添加你的 GitHub 仓库地址。
4. 类型选择 `Integration`。
5. 安装 `Gizwits`。
6. 重启 Home Assistant。
7. 进入 `Settings -> Devices & Services -> Add Integration`。
8. 搜索 `Gizwits`。

### Manual install

Copy `custom_components/gizwits` into your Home Assistant `custom_components` directory, then restart Home Assistant.

### 手动安装

将 `custom_components/gizwits` 复制到 Home Assistant 的 `custom_components` 目录，然后重启 Home Assistant。

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

在 Home Assistant 中打开 `Gizwits` 集成，并填写：

- App 账号用户名
- 密码
- app ID
- 可选的 `did`
- 可选的设备名称
- 轮询间隔

如果不填写 `did`，集成会尝试自动获取设备列表。
如果当前账号下没有拉到设备，请先确认你使用的是该 App 体系对应的正确 Gizwits `app_id`，必要时也可以直接填写已知的 `did`。

## Energy Dashboard

Use the `Energy` entity from this integration as a source in the Home Assistant Energy dashboard.
It is exposed with:

- `device_class: energy`
- `state_class: total_increasing`
- `unit_of_measurement: kWh`

可以在 Home Assistant 能源面板中把本集成的 `Energy` 实体作为数据源使用。
该实体具备：

- `device_class: energy`
- `state_class: total_increasing`
- `unit_of_measurement: kWh`

## Repository layout

- `custom_components/gizwits`: Home Assistant custom integration

- `custom_components/gizwits`：Home Assistant 自定义集成

## Publish checklist

Before publishing, make sure you do not commit:

- real usernames
- passwords
- real `did` values
- Home Assistant database files
- local debug exports

发布前请确认不要提交这些内容：

- 真实用户名
- 密码
- 真实 `did`
- Home Assistant 数据库文件
- 本地调试导出文件

Repository:

- [johnnysuns/gizwits_home](https://github.com/johnnysuns/gizwits_home)

## HACS

There are two ways users can find it in HACS.

用户在 HACS 里通常有两种方式找到它。

### 1. HACS custom repository

Any public GitHub repository that meets the HACS requirements can be added manually by URL in:

`HACS -> Integrations -> Custom repositories`

That is the fastest path and usually how new integrations start.

这是最快的方式，也是大多数新集成的起点。

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

如果想让它直接出现在 HACS 默认商店中，而不是靠手动添加仓库地址，还需要：

- 保持 GitHub 仓库公开
- 保持标准 `custom_components/<domain>` 目录结构
- 包含 `hacs.json`
- 通过 HACS GitHub Action
- 通过 `hassfest`
- 至少创建一个 GitHub Release
- 添加集成品牌资源
- 向 `hacs/default` 提交收录 PR

## References

- [HACS general requirements](https://hacs.xyz/docs/publish/start/)
- [HACS integration requirements](https://hacs.xyz/docs/publish/integration/)
- [HACS include in default store](https://hacs.xyz/docs/publish/include/)
- [Gizwits OpenAPI](https://docs.gizwits.com/zh-cn/Cloud/openapi_apps.html)
- [Hassbian article](https://bbs.hassbian.com/thread-19326-1-1.html)
