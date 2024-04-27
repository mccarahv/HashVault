const HDWalletProvider = require('@truffle/hdwallet-provider');
const privateKey = '####'; // Your new private key
const sepoliaInfuraUrl = `https://sepolia.infura.io/v3/####`; // Your Infura URL for Sepolia

module.exports = {
  networks: {
    sepolia: {
      provider: () => new HDWalletProvider(privateKey, sepoliaInfuraUrl),
      network_id: 11155111, // Sepolia's network id
      confirmations: 2,    // # of confirmations to wait between deployments. (default: 0)
      timeoutBlocks: 200,  // # of blocks before a deployment times out (minimum/default: 50)
      skipDryRun: true     // Skip dry run before migrations? (default: false for public nets)
    }
  },
  compilers: {
    solc: {
      version: "0.8.21", // Use the Solidity version that your contracts require
      settings: {
        optimizer: {
          enabled: true, // Enable optimizer
          runs: 200     // Set the optimizer runs
        }
      }
    }
  },
  // Additional configurations like mocha and db settings can be added here as needed
};
