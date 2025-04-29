# Apple Music SSH

这是一个 Home Assistant 的自定义组件，通过 SSH 连接到 Mac 电脑来控制 Apple Music。

## 功能

- 显示 Apple Music 播放状态
- 显示当前播放的曲目
- 播放/暂停控制
- 上一曲/下一曲控制
- 系统音量控制

## 安装

1. 下载此仓库
2. 将 `apple_music_ssh` 文件夹复制到你的 Home Assistant 配置目录下的 `custom_components` 文件夹中
3. 重启 Home Assistant
4. 在集成页面中添加 "Apple Music SSH" 集成
5. 配置 SSH 连接信息（主机地址、用户名、密码或私钥文件）

## 配置

你可以选择两种认证方式：

1. 密码认证：
   - 输入主机地址
   - 输入用户名
   - 输入密码

2. 私钥认证：
   - 输入主机地址
   - 输入用户名
   - 输入私钥文件路径

## 使用

安装完成后，你可以：

1. 在 Home Assistant 中查看：
   - Apple Music 的播放状态
   - 当前播放的曲目名称
   - 系统音量大小

2. 控制功能：
   - 播放/暂停音乐
   - 切换上一曲/下一曲
   - 调节系统音量

## 要求

- Home Assistant
- 运行 macOS 的电脑
- SSH 访问权限
- Apple Music 应用

## 依赖

- paramiko >= 2.7.2

## 作者

[@DTZSGHNR](https://github.com/DTZSGHNR)

## 许可

MIT License 