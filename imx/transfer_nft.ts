import { BigNumber } from 'ethers';
import { ERC721TokenType  } from '@imtbl/imx-sdk'

import { CreateIMXClient } from "./imx"

(async (): Promise<void> => {
    ////////////////////////////////////////////////////////////////////////////////
    // GENERAL
    const pk = process.env.PRIVATE_KEY!;
    const network = process.env.NETWORK!;
    const gasLimit = process.env.GAS_LIMIT;
    const gasPrice = process.env.GAS_PRICE;
    // SPECIFIC
    const sender = process.env.SENDER_ADDR!.toLowerCase();
    const receiver = process.env.RECEIVER_ADDR!.toLowerCase();
    const tokenId = process.env.TOKEN_ID!;
    const contractAddr = process.env.CONTRACT_ADDR!.toLowerCase();

    ////////////////////////////////////////////////////////////////////////////////

    const client = await CreateIMXClient(pk, network, gasLimit, gasPrice);
    let res = await client.transfer({
        sender: sender,
        receiver: receiver,
        quantity: BigNumber.from(1),
        token: {
            type: ERC721TokenType.ERC721,
            data: {
                tokenAddress: contractAddr,
                tokenId: tokenId,
            }
        }
    });
    console.log(JSON.stringify(res));

})().catch((e) => {
    let msgStr = e.message.toString();
    let msg = JSON.parse(msgStr)["message"];
    let err = {
        "status": "error",
        "message": msg,
    }
    console.log(JSON.stringify(err));

    process.exit(1);
});
