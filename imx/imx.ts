import { AlchemyProvider } from '@ethersproject/providers';
import { Wallet } from '@ethersproject/wallet';
import { ImmutableXClient } from '@imtbl/imx-sdk'

const provider = new AlchemyProvider('ropsten', "DvukuyBzEK-JyP6zp1NVeNVYLJCrzjp_");

const networkParams = {
    test: {
        apiUrl: "https://api.uat.x.immutable.com/v1",
        starkContractAddr: "0x4527BE8f31E2ebFbEF4fCADDb5a17447B27d2aef",
        registratrionContractAddr: "0x6C21EC8DE44AE44D0992ec3e2d9f1aBb6207D864"
    },
    main: {
        apiUrl: "https://api.x.immutable.com/v1",
        starkContractAddr: "0x5FDCCA53617f4d2b9134B29090C87D01058e27e9",
        registratrionContractAddr: "0x72a06bf2a1CE5e39cBA06c0CAb824960B587d64c"
    }
}

export const CreateIMXClient = async (
    privateKey: string,
    network: string,
    gasLimit: string = "",
    gasPrice: string = ""): Promise<ImmutableXClient> =>
{
    let selectedNetwork;
    if (network === "test")
        selectedNetwork = networkParams.test;
    else if (network === "main")
        selectedNetwork = networkParams.main;
    else
        throw Error(`Unknown network type: '${network}'`);

    // TODO do I have to connect each time?
    const signer = new Wallet(privateKey).connect(provider);
    const client = await ImmutableXClient.build({
        publicApiUrl: selectedNetwork.apiUrl,
        signer: signer,
        starkContractAddress: selectedNetwork.starkContractAddr,
        registrationContractAddress: selectedNetwork.registratrionContractAddr,
        gasLimit: gasLimit,
        gasPrice: gasPrice,
    });

    return client;
}

export const waitForTransaction = async (promise: Promise<string>) => {
    const txId = await promise;
    console.log('Waiting for transaction', {
        txId,
        etherscanLink: `https://ropsten.etherscan.io/tx/${txId}`,
        alchemyLink: `https://dashboard.alchemyapi.io/mempool/eth-ropsten/tx/${txId}`,
    });
    const receipt = await provider.waitForTransaction(txId);
    if (receipt.status === 0) {
        throw new Error('Transaction rejected');
    }
    console.log('Transaction Mined: ' + receipt.blockNumber);
    return receipt;
};
