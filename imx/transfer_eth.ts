import { BigNumber } from 'ethers';
import { ETHTokenType } from '@imtbl/imx-sdk'

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
    ////////////////////////////////////////////////////////////////////////////////

    const client = await CreateIMXClient(pk, network, gasLimit, gasPrice);

    // we can write ATMAX!!! 5 decimals as input
    let ethAmount: BigNumber;
    const asWei = process.env.AS_WEI;
    if (asWei === "False") {
        const ethDecimals = BigNumber.from(1000).mul(BigNumber.from(10000000000));
        const ethAmountDouble = + process.env.AMOUNT!;
        ethAmount = BigNumber.from(Math.floor(ethAmountDouble * 100000)).mul(ethDecimals)
    }
    else {
        const ethAmountInteger = process.env.AMOUNT!;
        ethAmount = BigNumber.from(ethAmountInteger);
    }

    let res = await client.transfer({
        sender: sender,
        receiver: receiver,
        quantity: ethAmount,
        token: {
            type: ETHTokenType.ETH,
            data: {
                decimals: 18
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
