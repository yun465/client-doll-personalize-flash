# client-doll-personalize-flash

A privacy-first Codex skill for personalizing and provisioning ESP32-S3 AI dolls.

## What it covers

- Two-step customer workflow: persona approval first, authorized local wake acknowledgement audio second.
- Local chat analysis with explicit speaker selection and sanitized persona data.
- Offline preview and validation before firmware integration.
- ESP32-S3 build, target-board identification, minimal-write flashing, and verification gates.
- Explicit boundaries for recordings, API keys, Wi-Fi credentials, cloud calls, and paid tests.

## Install

Copy this directory into your Codex skills directory as `client-doll-personalize-flash`, then invoke it with:

```text
$client-doll-personalize-flash
```

The skill is a workflow reference. It does not include customer chat records, recordings, credentials, firmware images, build caches, or device backups.

## Privacy and safety

Keep customer-specific data in a private, ignored workspace. Do not commit chat exports, audio, API keys, Wi-Fi passwords, voice URIs, NVS images, flash backups, or customer firmware images.

Before any real cloud request, credential write, erase, flash, or paid test, obtain the corresponding explicit authorization and report exactly what was performed.

## License

MIT. See [LICENSE](LICENSE).
