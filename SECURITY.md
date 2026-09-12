# Security Policy

## Reporting a vulnerability

Do not open a public Issue containing a vulnerability that could expose customer chat, recordings, credentials, device configuration, or firmware secrets.

Use GitHub's private **Report a vulnerability** channel for this repository when it is available. If it is not available, contact the maintainer through the GitHub profile without including exploit details or sensitive samples in the first public message.

Include only the minimum reproducible information. Replace customer data, local paths, MAC addresses, credentials, audio, and firmware images with synthetic placeholders.

## Scope

Security reports may cover:

- secret or customer-data leakage;
- unsafe authorization expansion;
- destructive or misdirected flash behavior;
- incorrect separation of public persona and secret device configuration;
- instructions that could cause unauthorized audio upload or paid cloud calls.

The included ESP32-S3 reference profile explicitly does not enable Flash Encryption, NVS Encryption, or Secure Boot. Physical extraction from that reference device is therefore a documented limitation, not a confidential security claim.
