# Gizwits for Home Assistant

[English](README.md)

这是一个用于接入机智云设备的 Home Assistant 自定义集成。

当前实现已经在真实 Home Assistant 环境中结合卓虎智能电表验证通过。集成支持自定义 Gizwits `app_id`，因此也可以适配其他基于机智云的 App 和设备。

配置流程中的默认 `app_id` 是卓虎设备验证时使用的值。如果你的设备属于其他机智云 App 体系，请改成对应 App 的正确 `app_id`。

这是一个 `cloud_polling` 集成。
它不使用本地局域网协议。

## 功能

当前面向电表场景提供这些实体：

- 有功功率
- 无功功率
- 电流
- 电压
- 频率
- 电量
- 功率因数

## 已验证设备清单

以下设备或 App 生态已经在当前版本中完成验证：

- 卓虎智能电表
- 默认内置 `app_id` 对应的卓虎 App 生态

如果你使用的是其他基于机智云的 App 或硬件厂商设备，也可以在配置时替换 `app_id` 后尝试接入。

## 安装

### 通过 HACS 安装

如果你已经能在 HACS 中看到 `gizwits_home`，可以直接在 HACS 里打开并安装。

如果暂时还看不到，再先把这个仓库作为自定义仓库添加进去：

1. 将此仓库推送到公开的 GitHub 仓库。
2. 在 Home Assistant 中打开 `HACS -> Integrations -> Custom repositories`。
3. 添加你的 GitHub 仓库地址。
4. 类型选择 `Integration`。
5. 安装 `Gizwits`。
6. 重启 Home Assistant。
7. 进入 `Settings -> Devices & Services -> Add Integration`。
8. 搜索 `Gizwits`。

### 手动安装

将 `custom_components/gizwits` 复制到 Home Assistant 的 `custom_components` 目录，然后重启 Home Assistant。

## 配置

在 Home Assistant 中打开 `Gizwits` 集成，并填写：

- App 账号用户名
- 密码
- app ID
- 可选的 `did`
- 可选的设备名称
- 轮询间隔

如果不填写 `did`，集成会尝试自动获取设备列表。
如果当前账号下没有拉取到设备，请先确认你使用的是该 App 体系对应的正确 Gizwits `app_id`，必要时也可以直接填写已知的 `did`。

## 能源面板

可以在 Home Assistant 能源面板中把本集成的 `Energy` 实体作为数据源使用。该实体具备：

- `device_class: energy`
- `state_class: total_increasing`
- `unit_of_measurement: kWh`

## 仓库结构

- `custom_components/gizwits`：Home Assistant 自定义集成

## 发布前检查

发布前请确认不要提交这些内容：

- 真实用户名
- 密码
- 真实 `did`
- Home Assistant 数据库文件
- 本地调试导出文件

仓库地址：

- [johnnysuns/gizwits_home](https://github.com/johnnysuns/gizwits_home)

## 参考资料

- [HACS general requirements](https://hacs.xyz/docs/publish/start/)
- [HACS integration requirements](https://hacs.xyz/docs/publish/integration/)
- [HACS include in default store](https://hacs.xyz/docs/publish/include/)
- [Gizwits OpenAPI](https://docs.gizwits.com/zh-cn/Cloud/openapi_apps.html)
- [Hassbian article](https://bbs.hassbian.com/thread-19326-1-1.html)
