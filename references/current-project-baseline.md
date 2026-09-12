# 当前项目基线

这是一个来自配套私有固件工程的参考配置，不随本仓库分发，也不是其他 ESP32-S3 项目的默认值。先按 [project-adaptation.md](project-adaptation.md)确认目标项目确实匹配；不匹配时只复用授权、隐私和最小写入原则，不复制本文的路径、版本、引脚、模型或分区偏移。进入构建前仍要读取目标项目最新 `AGENTS.md`、`PLAN.md`、受版本控制的配置和 Git 状态。

## 已验收目标

- 硬件：ESP32-S3 N16R8，16 MB Flash，8 MB Octal PSRAM。
- 框架：ESP-IDF 6.0.2。
- 麦克风：INMP441/I2S 兼容模块，BCLK=GPIO4、WS=GPIO5、SD=GPIO6、L/R 接 GND、VDD 接 3V3。
- 扬声器：MAX98357A，BCLK=GPIO15、LRC=GPIO16、DIN=GPIO7，连接 3 W 扬声器。
- BOOT：GPIO0。板载 WS2812B：GPIO48。
- 当前唤醒词：`小酥肉`，模型 `wn9_xiaosurou_tts2`。旧 `Computer` 仅为历史记录，不再启用。
- 当前链路为：本地 WakeNet 检测“小酥肉” → 本地播放客户授权的“我在” → 清空麦克风 DMA → ESP-SR VAD 录音 → 硅基流动 SenseVoiceSmall ASR → DeepSeek → 硅基流动 CosyVoice2 TTS。
- VAD 使用 30 ms 帧、约 120 ms 连续语音确认起声、起声后连续 810 ms 静音自动停录、3 秒未起声取消、最长 5 秒；VAD 初始化失败时退回最长 5 秒。
- 默认 TTS 回退音色为 `david`；可选用户预置音色 URI 只存 NVS。
- BOOT 短按不控制对话；长按 3 至 10 秒进入手机配网。

## 已验收音频基线

- 设备音量设为 100% 时，固件使用 `DOLL_TTS_OUTPUT_GAIN_PERCENT=180U`，即在 PCM 上进行约 +5.1 dB 的饱和限幅放大；超出采样范围时钳位，不发生整数回绕。若某个扬声器出现明显破音，可以降低比例，但不得静默取消增益。
- TTS 响应限制在 2 MiB 以内。固件先把有效 WAV 完整下载到 8 MB PSRAM，再连续播放，避免网络抖动造成播放中途卡顿。代价是开始出声前要等待完整下载。
- I2S 发送必须处理短写：一次写入不足时循环发送剩余数据，直到当前音频块完整写完或明确失败。
- 每次构建都必须重新记录应用大小、分区余量、各镜像 SHA-256、测试计数和是否完整构建通过；不要把历史客户构建的哈希或录音统计当作新客户结果。
## 手机配网

- SoftAP 名称：`GiftDoll-XXXXXX`。
- 配网凭据必须由目标项目在本地安全生成或配置；不要把开发密码、真实 Wi-Fi 密码或 API Key 写入 skill、Git 或公开构建物。
- 本地页面：`http://192.168.4.1`。
- 配置字段：2.4 GHz Wi-Fi、DeepSeek API Key、硅基流动 API Key、可选个人音色 URI。
- 页面不回显既有秘密、不使用浏览器持久化；配置模式 5 分钟超时。
- 配网阶段不调用云 API。

## 人格系统

- PC 端：`desktop_tool/ai_doll_tool/chat_import.py`、`style_analyzer.py`、`persona_package.py`、`prompt_builder.py`。
- CLI：`python -m desktop_tool.ai_doll_tool.cli`。
- `analyze-chat` 支持 UTF-8 TXT/Markdown、恰好两位参与者，`--owner` 必须精确匹配说话人标签。
- 敏感内容由 `privacy.py` 过滤；候选示例只有人工批准后才可使用。
- 设备端：`firmware/components/doll_platform/doll_persona.c`。
- 设备公共人格结构：

```json
{
  "persona": {"summary": "...", "reply_style": "..."},
  "style_examples": [{"example": "...", "keywords": ["..."]}],
  "memories": [{"id": "...", "content": "...", "keywords": ["..."], "importance": 3, "confirmed": true}],
  "blocked_topics": ["..."]
}
```

- 固件提示词会加入人格摘要、回复规则、按关键词检索的示例与确认记忆。
- 固件必须保留 AI 身份说明；不替现实中的本人承诺或报告实时事实。

## 16 MB 分区

| 分区 | 偏移 | 大小 | 用途 |
|---|---:|---:|---|
| nvs | `0x9000` | `0x10000` | Wi-Fi、API Key、音色 URI 等私有配置 |
| otadata | `0x19000` | `0x2000` | OTA 元数据 |
| phy_init | `0x1B000` | `0x1000` | PHY |
| ota_0 | `0x20000` | `0x300000` | 应用 A |
| ota_1 | `0x320000` | `0x300000` | 应用 B |
| doll_a | `0x620000` | `0x180000` | LittleFS 公共配置 A |
| doll_b | `0x7A0000` | `0x180000` | LittleFS 公共配置 B |
| coredump | `0x920000` | `0x10000` | 崩溃转储 |
| model | `0x930000` | `0x100000` | ESP-SR 模型 |

## 已知边界

- 项目明确不启用 Flash 加密、NVS 加密或 Secure Boot；设备丢失或被拆机时，专业人员可能读取固件和秘密。
- 对话原始录音仅在一次请求期间位于 RAM，结束或失败后清零；不保存。
- 本地“我在”属于另一类静态私有资产，会嵌入应用镜像且可能被物理提取；原始录音、临时 WAV、PCM 和含录音的固件不得跨客户或进入公共输出。
- 新的真实 ASR、DeepSeek、TTS、音色上传或付费试听均需本次单独批准。
- 最近的客户板验收只证明该板完整镜像和启动成功；任何新板都必须重新识别和验证。
- 设备 MAC、历史烧录记录或应用分区可写入都不能证明 Bootloader、分区表、双 LittleFS 和模型实际存在；每块板都要在写入前只读分类 Flash 完整性。
- 新刷或恢复基础分区后，NVS 可能仍为空。必须以配置存在布尔状态为准，缺少 Wi-Fi、API Key 或音色 URI 时由用户通过手机本地网页重新填写，不能从上一位客户复制。
- skill 所在目录不代表客户固件源码工作副本已经建立；应检查目标项目中的具体 `customers\<customer-id>` 目录。

## 客户项目与母版关系

- 母版用于提供已验收源码和测试，不承载新客户的聊天或配置。
- 客户项目为每位客户建立独立工作副本和 `private_data/`。
- 初始化副本时只复制 Git 跟踪文件，排除母版 `private_data/`、`build_artifacts/`、`firmware/build*/`、Flash 备份、录音和本地密钥。
- 任何客户人格调整先在客户副本完成；除非修复通用缺陷，不回写母版。
