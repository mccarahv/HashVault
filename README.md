**HashVault: Blockchain-Enhanced File Integrity and Ownership Verification**

**Overview:**
HashVault empowers individuals and organizations to establish a decentralized, encrypted file management system that records hashes of files on the Ethereum blockchain. This provides a verifiable, immutable timestamp of file creation and ownership without disclosing the file's contents to the public.

**Key Features:**
- **Secure Hash Generation:** Automatically generates a secure hash of any file, ensuring the content's integrity without revealing any sensitive information.
- **Blockchain Integration:** Utilizes the public Ethereum blockchain to record hashes, providing a tamper-proof and permanent record that can be publicly verified.
- **Flexible File Support:** Supports multiple file formats including CSV, TXT, and XLSX, making it suitable for a wide range of applications.

**Use Cases:**
- **Intellectual Property Protection:** Ideal for creators and inventors looking to establish first ownership of trademarks, copyrighted materials, and patents.
- **Data Integrity Verification:** Useful for researchers and data scientists to maintain and prove the editing history and authenticity of machine learning datasets and other critical data files.
- **Corporate Governance:** Assists organizations in maintaining auditable records of important documents to ensure compliance with regulatory and legal requirements.

**Benefits:**
- **Transparency and Trust:** Provides a clear, auditable trail of file creation and modification history that enhances trust and transparency.
- **Ease of Use:** Features a user-friendly interface that simplifies the process of hashing files and sending them to the blockchain, making advanced blockchain technology accessible to non-technical users.
- **Privacy and Security:** Ensures privacy by only exposing the hash of a file on the blockchain, not the file's actual content.

**Potential for Expansion:**
HashVault's modular design allows for future enhancements such as support for additional file types, integration with other blockchain platforms, and advanced security features like multi-factor authentication and end-to-end encryption.

---

## Prerequisites
Before you begin, you will need to set up the following:

1. **Infura Account:**
   - Sign up at [Infura.io](https://infura.io/) and create a new project to get an API key. This key will allow you to connect to Ethereum networks without running a full node.
   - Note your project ID, as you will need to include this in your application configuration.

2. **Etherscan API Key:**
   - Register at [Etherscan.io](https://etherscan.io/) and generate an API key. This key is used to query transaction details and other blockchain data.
   - You will need this key to verify transaction statuses and retrieve timestamps.

3. **Ethereum Wallet:**
   - Generate an Ethereum wallet address and private key. You can use tools like [MyEtherWallet](https://www.myetherwallet.com/) or [MetaMask](https://metamask.io/).
   - Ensure your wallet has some Ethereum for deploying contracts and making transactions. For testnet deployment, you can get free Ether from a faucet.

---

## Project Structure

This section outlines the purpose of each file in the HashVault project and provides a guide on how to deploy your own version of the system.

### File Descriptions

- **`package.json`**:
  - **Purpose:** Manages the project's dependencies, scripts, and metadata.
  - **Key Details:** Contains all the necessary Node.js package dependencies required for running the project.

- **`package-lock.json`**:
  - **Purpose:** Automatically generated file to lock the versions of installed packages, ensuring consistent installs across machines.
  - **Key Details:** Should not be manually edited.

- **`truffle-config.js`**:
  - **Purpose:** Configuration file for Truffle, used to define network configurations and compiler settings.
  - **Key Details:** Modify this file to include custom settings for different blockchain networks (development, testnet, mainnet).

- **`2_deploy_contracts.js`**:
  - **Purpose:** Deployment script for Truffle that manages the deployment of smart contracts to the blockchain.
  - **Key Details:** Edit this script if you are adding more contracts or need specific deployment logic.

- **`SmartContract.sol`**:
  - **Purpose:** Contains the Solidity smart contract code for managing file hashes on the Ethereum blockchain.
  - **Key Details:** This contract includes functions for storing and retrieving file hashes.

- **`SmartContract.json`**:
  - **Purpose:** Generated by Truffle, this JSON file contains the ABI and bytecode of the compiled smart contract.
  - **Key Details:** Used by the frontend application to interact with the deployed smart contract.

- **`HashVault_Widget.py`**:
  - **Purpose:** The main PyQt5 application file that provides the GUI for file selection, hashing, and interaction with the Ethereum blockchain.
  - **Key Details:** This script integrates the blockchain with a user-friendly interface for file management.

### Deployment Instructions

**Step 1: Clone the Repository**
- Clone this repository to your local machine using:
  ```bash
  git clone <repository-url>
  ```

**Step 2: Install Node.js and Truffle**
- Ensure Node.js is installed on your machine. [Download Node.js](https://nodejs.org/)
- Install Truffle globally using npm:
  ```bash
  npm install -g truffle
  ```

**Step 3: Install Project Dependencies**
- Navigate to the project directory and install the required Node.js dependencies:
  ```bash
  cd HashVault
  npm install
  ```

**Step 4: Configure Truffle**
- Edit `truffle-config.js` to set up your desired Ethereum network (development, Ganache, testnet, or mainnet).

**Step 5: Compile and Deploy Smart Contract**
- Compile your smart contracts to check for any compilation errors:
  ```bash
  truffle compile
  ```
- Deploy your smart contracts to the network defined in `truffle-config.js`:
  ```bash
  truffle migrate --network development
  ```

**Step 6: Update and Run the Python Application**
- Update `HashVault_Widget.py` with the deployed smart contract address and network details.
- Ensure Python and required packages are installed, then run the application:
  ```bash
  python HashVault_Widget.py
  ```

**Step 7: Verify Operation**
- Use the application to hash and store a file's hash on the blockchain. Verify that transactions are successfully recorded and retrievable.

---


## Installation and Configuration

1. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   ```
2.    **Step 2: Install Node.js and Truffle**
- Ensure Node.js is installed on your machine. [Download Node.js](https://nodejs.org/)
- Install Truffle globally using npm:
  ```bash
  npm install -g truffle
  ```

3. **Install Dependencies:**
   Navigate to the project directory and install dependencies:
   ```bash
   cd HashVault
   npm install
   ```

4. **Configure the Truffle Framework:**
   Update `truffle-config.js` with the Infura endpoint and your wallet information. Here is an example configuration for the Sepolia testnet:
   ```javascript
   const HDWalletProvider = require('@truffle/hdwallet-provider');
   const infuraKey = 'YOUR_INFURA_API_KEY';

   module.exports = {
     networks: {
       sepolia: {
         provider: () => new HDWalletProvider('YOUR_PRIVATE_KEY', `https://sepolia.infura.io/v3/${infuraKey}`),
         network_id: 11155111, // Sepolia's network id
         gas: 5500000, // Gas limit
         confirmations: 2,
         timeoutBlocks: 200,
         skipDryRun: true
       },
     },
     compilers: {
       solc: {
         version: "^0.8.0",
       }
     }
   };
   ```

5. **Compile and Deploy Smart Contracts:**
   Compile your smart contracts to check for errors and prepare them for deployment:
   ```bash
   truffle compile
   truffle migrate --network sepolia
   ```
   After deployment, note the contract address output by Truffle. This is required for the Python application to interact with the smart contract. Paste this contract in the `HashVault_Widget.py` contract address at line 242.

6. **Configure the Python Application:**
   Open `HashVault_Widget.py` and update the configuration lines to include your Infura API key, Etherscan API key, Ethereum wallet address, private key, and the newly deployed contract address. Look for the following lines:
   ```python
   infura_api_key = "###" (Line 238)
   contract_address = "###" (Line 242)
   from_address = "###" (Line 247)
   private_key = "####" (Line 248)
   ```

7. **Run the Application:**
   With all configurations set, you can now run the application:
   ```bash
   python HashVault_Widget.py
   ```
