# 项目适配指南

只有目标项目明确提供下面的能力，Skill 才能从人格预览继续到集成、构建和烧录。先从项目受版本控制的文件中解析实际值；不要把本指南中的字段名、路径或示例当作目标项目事实。

## 适配清单

| 能力 | 需要确认的内容 | 缺失时的处理 |
|---|---|---|
| 私有工作区 | 客户目录规则、`private_data` 忽略状态 | 停止处理客户材料 |
| 聊天分析 | 支持格式、说话人标签、脱敏输出、调用命令 | 只登记输入，不读取聊天正文 |
| 人格编译 | 输出结构、校验器、示例审批机制 | 只交付人工预览 |
| 公共配置写入 | 与秘密配置隔离的 schema、A/B 或原子写入机制 | 不写设备配置 |
| 构建 | 锁定工具链、依赖、测试、构建命令、产物清单 | 不构建、不推测版本 |
| 板卡探测 | 串口枚举、芯片、MAC、Flash、PSRAM 的只读探测 | 不连接或写入设备 |
| Flash 计划 | 本次构建生成的参数、分区表、偏移、长度 | 不使用参考偏移替代 |
| 写后验证 | 写入哈希、读回方式、启动日志和本地功能检查 | 不宣称烧录成功 |

## 推荐的项目配置记录

在客户私有工作区记录一份不含秘密的适配摘要。字段可以按项目调整：

```yaml
project_root: <absolute local path>
project_revision: <git commit>
customer_workspace: <private ignored path>
chat_analyzer: <existing local command or adapter>
persona_compiler: <existing local command or adapter>
public_config_writer: <existing local command or interface>
toolchain: <project-locked version>
build_command: <project command>
build_artifacts: <generated manifest or directory>
board_probe: <read-only command>
flash_plan_source: <generated flash args and partition table>
verification: <read-back and startup checks>
hardware_profile: <board, flash, psram, audio and wake model>
authorized_stage: <current user-approved boundary>
```

这份记录不得包含聊天正文、真实姓名、Wi-Fi、API Key、音色 URI、录音内容、设备备份或客户固件哈希以外的可识别材料。

## 参考配置兼容性

只有同时满足以下条件，才可声明目标项目匹配 [current-project-baseline.md](current-project-baseline.md)：

- 项目自己的配置确认目标是 ESP32-S3 N16R8 和对应 PSRAM 模式。
- 项目锁定的 ESP-IDF、分区表、唤醒模型和音频链路与参考配置一致。
- 文档中提到的分析器、人格编译器、配置写入器、测试和构建产物在目标项目中真实存在。
- 目标板已在本轮重新识别；历史 COM、MAC 或旧构建报告不作为当前证据。

任一条件不满足时，把参考配置视为示例，只使用本 Skill 的授权、隐私和最小写入原则。

## 对外发布边界

项目适配摘要、日志和 Issue 只报告布尔状态、计数、版本和脱敏错误。不要发布本机绝对路径、真实串口归属、聊天片段、录音、秘密值或包含客户声音的固件。
