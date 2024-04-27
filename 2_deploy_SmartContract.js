const HashStore = artifacts.require("HashStore");

module.exports = function (deployer) {
  deployer.deploy(HashStore);
};
