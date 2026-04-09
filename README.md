# Project by Camélia El Rhabi

## Project Presentation
This portal is a decentralized application (dApp) designed to participate in the famous **Keynesian Beauty Contest** via a **Commit-Reveal** protocol on the blockchain. 
The objective is to choose a number between 0 and 100 that is closest to **2/3 of the average** of all numbers chosen by the class.

## System Architecture
To guarantee the integrity and confidentiality of the votes, the system uses a two-phase cryptographic mechanism:

* **Commit Phase**: The user generates a proof of their choice by hashing their `ID|Number|Secret` with the **SHA-256** algorithm. Only the hash is sent to the ledger, keeping the choice secret.
* **Reveal Phase**: Once the deadline has passed, the user reveals their number and secret. The system verifies that the hash matches the initial commitment before counting the vote.

## Tech Stack
* **Frontend**: Streamlit (Custom Pastel Pink & Beige design)
* **Backend**: Google Apps Script API (Shared Ledger)
* **Cryptography**: SHA-256 (`hashlib` library)
* **Typography**: Aeonik Pro (Lexend Deca)

## Installation and Launch
Clone the repository:
```bash
git clone [https://github.com/your-username/neoma-blockchain-portal.git](https://github.com/your-username/neoma-blockchain-portal.git)
