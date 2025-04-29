# MacMusiCast

MacMusiCast 是一个 Home Assistant 自定义集成（HACS 支持），允许通过 SSH 远程控制 Mac 上的 Apple Music 应用，并将播放信息无缝集成到你的智能家居中。

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub Release][releases-shield]][releases]
[![License][license-shield]](LICENSE)

## 功能特点

- 🎵 实时显示播放状态和曲目信息
- 🎮 远程控制（播放/暂停、上一曲/下一曲）
- 🔊 系统音量控制
- 🔐 支持密码和密钥两种 SSH 认证方式
- 🏠 完全集成到 Home Assistant 界面

## 安装

### HACS 安装（推荐）

1. 确保已经安装了 [HACS](https://hacs.xyz/)
2. 在 HACS 中点击集成
3. 点击右上角的 ⋮ 按钮
4. 选择"自定义存储库"
5. 添加 URL：`https://github.com/Nanako718/MacMusiCast`
6. 选择类别为"集成"
7. 点击"添加"
8. 在 HACS 中搜索 "MacMusiCast"
9. 点击"下载"
10. 重启 Home Assistant

### 手动安装

1. 下载此仓库
2. 将 `custom_components/apple_music_ssh` 文件夹复制到你的 Home Assistant 配置目录下的 `custom_components` 文件夹中
3. 重启 Home Assistant

## 配置

1. 在 Home Assistant 的集成页面中点击"添加集成"
2. 搜索 "MacMusiCast"
3. 按照配置向导进行设置：

### SSH 认证选项

#### 密码认证
- 主机地址：你的 Mac 的 IP 地址
- 用户名：Mac 用户名
- 密码：Mac 用户密码

#### 密钥认证
- 主机地址：你的 Mac 的 IP 地址
- 用户名：Mac 用户名
- 私钥文件路径：SSH 私钥文件的完整路径

## 实体

安装后，你将获得以下实体：

### 传感器
- `sensor.apple_music_state`：显示当前播放状态
- `sensor.apple_music_track`：显示当前播放的曲目

### 按钮
- `button.apple_music_play_pause`：播放/暂停控制
- `button.apple_music_next`：下一曲
- `button.apple_music_previous`：上一曲

### 数字
- `number.system_volume`：系统音量控制（0-100）

## 使用建议

### Lovelace 卡片示例
```yaml
type: entities
entities:
  - sensor.apple_music_state
  - sensor.apple_music_track
  - button.apple_music_play_pause
  - button.apple_music_previous
  - button.apple_music_next
  - number.system_volume
```

### 自动化示例
```yaml
automation:
  - alias: "音乐播放时调暗灯光"
    trigger:
      platform: state
      entity_id: sensor.apple_music_state
      to: 'playing'
    action:
      service: light.turn_on
      target:
        entity_id: light.living_room
      data:
        brightness_pct: 30
```

## 要求

- Home Assistant 2023.8.0 或更高版本
- 运行 macOS 的电脑（已测试 Sonoma 14.0+）
- SSH 访问权限
- Apple Music 应用

## 依赖

- paramiko >= 2.7.2

## 故障排除

1. 确保你的 Mac 已启用 SSH 访问（系统设置 > 共享 > 远程登录）
2. 确保 Apple Music 应用已安装并至少运行过一次
3. 检查防火墙设置，确保 SSH 端口（默认 22）未被阻止
4. 如果使用密钥认证，确保私钥文件权限正确（600）

## 贡献

欢迎提交 Issues 和 Pull Requests！

## 作者

[@DTZSGHNR](https://github.com/Nanako718)

## 许可

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

[releases-shield]: https://img.shields.io/github/release/Nanako718/MacMusiCast.svg
[releases]: https://github.com/Nanako718/MacMusiCast/releases
[license-shield]: https://img.shields.io/github/license/Nanako718/MacMusiCast.svg 