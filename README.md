# E2EE Messaging System

## Creators
- Yuval Ben Eliyahu - 207386970
- Tal Tribitch - 209396019

## Overview
A secure end-to-end encryption (E2EE) system for sending and receiving encrypted messages.

End-to-End Encryption (E2EE) ensures that all communication between two clients is fully encrypted and not exposed to any third party, including the server through which the messages are transmitted. The goal of this project is to develop a messaging system that protects against Man-in-the-Middle (MITM) attacks, ensuring Confidentiality, Integrity, and Authentication.

## Project Goals
- Develop an encryption system based on the AES-256 protocol in CBC mode.
- Integrate a Key Derivation Function (KDF) mechanism to generate strong encryption keys.
- Implement a client authentication mechanism to protect against spoofing using a secure channel.
- Protect against MITM attacks using digital certificates.
- Support multi-threading to improve system performance.

## System Description
### System Architecture

**Client:**
- Initial Registration: Perform initial registration with the server for identification and connection to the system.
- Identity Verification: Verify client identity with the server as part of information protection.
- Key Management: Securely exchange encryption keys with another client to create a secure communication channel.
- Message Sending: Send encrypted messages to other clients in the system.

**Server:**
- Public Key Storage: Store clients' public keys in a database (DB) to support encryption processes.
- OTP Sending: Send one-time passwords (OTP) for initial client registration via a secure channel.
- Encrypted Message Management: Handle the transfer of encrypted messages only between clients to maintain privacy.
- Offline Message Storage: Store messages in the database (DB) for clients who are unavailable, for later delivery.

## Features
- AES-256 for message encryption
  - Fast and efficient symmetric encryption algorithm.
  - Uses a random IV for each message to ensure randomness.
  - Used to encrypt message content.
- RSA for key exchange
  - Asymmetric encryption for secure transmission of symmetric keys.
  - Digital signatures for user identity verification.
- HMAC for data integrity
  - Used for data authentication and ensuring data integrity.
  - Based on the SHA-256 hashing function.
- Multi-threaded server
- Elliptic Curve Cryptography (ECC) for key generation and exchange
- Public key caching and retrieval with retry logic
- Signature verification for public key integrity


## Requirements
- Python 3.9+
- Libraries:
  - pycryptodome
  - cryptography

## Installation
1. Clone the repository.
2. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage
1. Run the server:
    ```sh
    python main.py
    ```
2. Use the client to send and receive encrypted messages.

