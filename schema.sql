CREATE DATABASE IF NOT EXISTS blockchain;
USE blockchain;

CREATE TABLE user_operations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    userOpHash VARCHAR(66),
    sender VARCHAR(42),
    paymaster VARCHAR(42),
    nonce BIGINT,
    success BOOLEAN,
    actualGasCost BIGINT,
    actualGasUsed BIGINT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
