// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract HashStore {
    mapping(uint => string) private hashes;
    uint private nextId = 1;
    address private owner;

    constructor() {
        owner = msg.sender; // Set the contract deployer as the owner
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only the owner can perform this action");
        _;
    }

    function storeHash(string memory hash) public onlyOwner {
        hashes[nextId] = hash;
        nextId++;
    }

    function getHash(uint id) public view returns (string memory) {
        require(id > 0 && id < nextId, "ID out of bounds");
        return hashes[id];
    }

    function getCurrentId() public view returns (uint) {
        return nextId;
    }
}

