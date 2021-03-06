import { BigNumber } from 'ethers';
import { AlchemyProvider } from '@ethersproject/providers';
import { Wallet } from '@ethersproject/wallet';
import { ImmutableXClient, ETHTokenType, ERC721TokenType, ERC20TokenType } from '@imtbl/imx-sdk'

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

const CreateIMXClient = async (
    privateKey: string,
    network: string,
    gasLimit: string = "",
    gasPrice: string = ""): Promise<ImmutableXClient> => {
    let selectedNetwork;
    if (network === "test")
        selectedNetwork = networkParams.test;
    else if (network === "main")
        selectedNetwork = networkParams.main;
    else
        throw Error(`[TYPESCRIPTWRAPPER]: Unknown network type: '${network}'`);

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

const createSuccessMsg = (msg: any) => {
    return {
        "status": "success",
        "result": msg
    }
};

const createErrorMsg = (msg: any) => {
    return {
        "status": "error",
        "result": msg
    }
};

(async (): Promise<void> => {

    const baseParams = JSON.parse(process.env.BASE_PARAMS!);
    const params = JSON.parse(process.env.PARAMS!);

    const client = await CreateIMXClient(
        baseParams.pk,
        baseParams.network,
        baseParams.gas_limit,
        baseParams.gas_price
    );

    let res, msg;
    switch (baseParams.function_name) {
        case "sign_msg": {
            res = await client.signMessage(params.msg);
            msg = createSuccessMsg(res);
            break;
        }
        case "register": {
            res = await client.registerImx({
                etherKey: client.address.toLowerCase(),
                starkPublicKey: client.starkPublicKey
            });
            msg = createSuccessMsg(res);
            break;
        }
        case "create_project": {
            res = await client.createProject(params);
            msg = createSuccessMsg(res);
            break;
        }
        case "create_collection": {
            res = await client.createCollection(params);
            msg = createSuccessMsg(res);
            break;
        }
        case "update_collection": {
            res = await client.updateCollection(
                params.contractAddress, params.params
            );
            msg = createSuccessMsg(res);
            break;
        }
        case "create_metadata_schema": {
            res = await client.addMetadataSchemaToCollection(
                params.contractAddress, params.params
            );
            msg = createSuccessMsg(res);
            break;
        }
        case "update_metadata_schema": {
            res = await client.updateMetadataSchemaByName(
                params.name, params.contractAddress, params.params
            );
            msg = createSuccessMsg(res);
            break;
        }
        case "transfer": {
            params.quantity = BigNumber.from(params.quantity);
            res = await client.transfer(params);
            msg = createSuccessMsg(res);
            break;
        }
        case "mint": {
            res = await client.mintV2(params);
            msg = createSuccessMsg(res.results);
            break;
        }
        case "burn": {
            res = await client.burn(params);
            msg = createSuccessMsg(res);
            break;
        }
        case "prepare_withdrawal": {
            res = await client.prepareWithdrawal(params);
            msg = createSuccessMsg(res);
            break;
        }
        case "complete_withdrawal": {
            params["starkPublicKey"] = client.starkPublicKey;
            res = await client.completeWithdrawal(params);
            msg = createSuccessMsg(res);
            break;
        }
        case "deposit": {
            res = await client.deposit(params);
            msg = createSuccessMsg(res);
            break;
        }
        case "deposit_cancel": {
            throw new Error("deposit_cancel not implemented");
            break;
        }
        case "deposit_reclaim": {
            throw new Error("deposit_reclaim not implemented");
            break;
        }
        case "create_order": {
            res = await client.createOrder(params);
            msg = createSuccessMsg(res);
            break;
        }
        case "cancel_order": {
            res = await client.cancelOrder(params.order_id);
            msg = createSuccessMsg(res);
            break;
        }
        case "create_trade": {
            res = await client.createTrade(params);
            msg = createSuccessMsg(res);
            break;
        }
        case "approve_nft": {
            res = await client.approveNFT(params);
            msg = createSuccessMsg(res);
            break;
        }
        case "approve_erc20": {
            params.amount = BigNumber.from(params.amount);
            res = await client.approveERC20(params);
            msg = createSuccessMsg(res);
            break;
        }
        case "create_exchange": {
            res = await client.createExchange(params.wallet_addr);
            msg = createSuccessMsg(res);
            break;
        }
        default: {
            throw new Error(`Invalid method name: '${baseParams.method_name}'`);
        }
    }

    // log result to stdout to be parsed by the python process
    console.log(JSON.stringify(msg));

})().catch((e) => {
    let msgStr = e.message.toString();
    let msg;
    try {
        msg = JSON.parse(msgStr)["message"];
    }
    catch (e_) {
        msg = `[TYPESCRIPTWRAPPER]: ${msgStr}`;
    }

    let err = createErrorMsg(msg);
    console.log(JSON.stringify(err));

    process.exit(1);
});
