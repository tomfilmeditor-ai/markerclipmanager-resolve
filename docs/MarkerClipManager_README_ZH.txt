MarkerClipManager — DaVinci Resolve 时间线和剪辑标记管理器
==========================================================
Author: Tommaso Feraboli — Film Editor
Version: 1.4.8
MIT License — see the script header

功能说明
--------
一个窗口用于查看和管理 Resolve 时间线中的所有标记: 包括标尺
(时间线级别) 标记和放在各个剪辑上的标记，在每个视频和音频轨道上。

对于每个标记，它显示: 标记图形 (与 Resolve 相同的原生形状)、
轨道、TC 入、TC 出、时长、颜色、名称、关键字、备注。

功能
----
- 选择一个或多个标记，更改颜色、更改轨道 (包括移到"TIMELINE"标尺或从中
  移出)、删除
- 直接在表中编辑名称、关键字和备注 (双击)，并可同时作用于选中的多个标记
- Delete 键的作用与删除按钮相同，确认提示可以关闭
- 使用 Cmd+Z / Ctrl+Z 撤销和重做，还有 History 面板：双击之前的某一步即可
  直接回到那里。仅涵盖当前会话，关闭脚本后清空
- 按颜色、轨道、作者/名称或关键字筛选
- 以 CSV 导出和导入标记
- 单击某一行：时间线播放头跳转到该标记
- 界面提供 12 种语言：如果系统语言在其中则以该语言启动，否则以英语启动，
  也可以在窗口顶部的菜单中更改 (重启脚本后生效)

系统要求
--------
- DaVinci Resolve 19/20 (macOS)
- 系统上已安装 Python 3
- PySide6 (由下面的设置脚本自动安装 — 不需要
  手动步骤)

安装 (一次性)
-------------
1. 下载适合你系统的安装程序
2. macOS：右键单击 .command 文件并选择"打开"，不要双击。该文件没有用
   Apple 开发者证书签名，双击会被 macOS 阻止
   Windows：双击 .cmd 文件；如果 SmartScreen 发出警告，选择"更多信息"，
   然后选择"仍要运行"
3. 安装程序会复制文件，然后准备脚本所需的 Python 环境 (这一步需要联网，
   大约需要一分钟)
4. 如果第二步失败 (没有网络，或者没有安装 Python)，文件仍然已正确安装：
   打开安装后的文件夹，方便时运行 "MarkerClipManager_Setup.command"
   (macOS) 或 "MarkerClipManager_Setup_Windows.cmd" (Windows)
5. 完成。更新也以同样方式安装，覆盖在上一版本之上，你的设置不会被改动

用法
----
在 DaVinci Resolve 中: Workspace > Scripts > Comp > MarkerClipManager > MarkerClipManager
(脚本位于 Comp 内的 "MarkerClipManager" 子文件夹中，因此在菜单中显示为
同名的子菜单)

已知限制
--------
- 表中的标记是由脚本绘制的重新创建的图标，不是
  Resolve 的官方图标 (API 未公开)。颜色是用户提供的精确
  十六进制值 — 只有图标形状仍是近似值
- "关键字"不是本机 Resolve 标记字段: 它存储在
  内部标记字段 (customData) 中，在 Resolve 的本机
  标记面板中不可见 — 仅此脚本可读/写
- 时间码直接从项目的活动时间线读取 fps 和 Drop Frame/Non-Drop Frame 模式
  (29.97 和 59.94 DF 使用标准 SMPTE 算法正确处理); 在非标准 fps 上，
  数学仍然是近似值
- 此脚本不处理 EDL 导入/导出: 使用 Resolve 的本机
  功能 (Timeline > Markers > Export/Import)
- 将标记移到视频/音频轨道需要该位置已存在剪辑

支持
----
错误报告: 使用应用中的 🐛 按钮 (打开预填充的电子邮件至
tomfilmeditor.tools@gmail.com)
如果您想支持开发: 应用中的 ☕ 按钮，或
https://paypal.me/acoffeefortom

⚠️  Note on translations: This documentation is available in multiple languages.
These translations were generated automatically. If you find any errors or typos,
please report them to the contact listed in the SUPPORT section above.
