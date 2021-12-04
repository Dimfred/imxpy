import { CreateIMXClient } from './imx'
import { BigNumber } from 'ethers';
import { ERC721TokenType, ETHTokenType } from '@imtbl/imx-sdk'


(async (): Promise<void> => {
    ////////////////////////////////////////////////////////////////////////////////
    // GENERAL
    const pk = process.env.PRIVATE_KEY!;
    const network = process.env.NETWORK!;
    const gasLimit = process.env.GAS_LIMIT;
    const gasPrice = process.env.GAS_PRICE;
    // SPECIFIC
    const userAddr = process.env.USER_ADDRESS!.toLowerCase();
    const orderType = process.env.SIDE;
    const ethAmountDouble = + process.env.ETH_AMOUNT!;
    const tokenId = process.env.TOKEN_ID!;
    const tokenAddr = process.env.TOKEN_ADDRESS!;
    ////////////////////////////////////////////////////////////////////////////////

    // we can write ATMAX!!! 5 decimals as input
    const ethDecimals = BigNumber.from(1000).mul(BigNumber.from(10000000000));
    const nftAmount: BigNumber = BigNumber.from(1);
    const ethAmount: BigNumber = BigNumber.from(Math.floor(ethAmountDouble * 100000)).mul(ethDecimals)

    const client = await CreateIMXClient(pk, network, gasLimit, gasPrice);

    let gres;
    switch (orderType) {
        case "SELL": {
            const res = await client.createOrder({
                user: userAddr,
                tokenSell: {
                    type: ERC721TokenType.ERC721,
                    data: {
                        tokenAddress: tokenAddr,
                        tokenId: tokenId,
                    }
                },
                amountSell: nftAmount,
                tokenBuy: {
                    type: ETHTokenType.ETH,
                    data: {
                        decimals: 18
                    }
                },
                amountBuy: ethAmount,
                include_fees: false,
            })
            gres = res;
            break;
        }
        case "BUY": {
            const res = await client.createOrder({
                user: userAddr,
                tokenSell: {
                    type: ETHTokenType.ETH,
                    data: {
                        decimals: 18
                    }
                },
                amountSell: ethAmount,
                tokenBuy: {
                    type: ERC721TokenType.ERC721,
                    data: {
                        tokenAddress: tokenAddr,
                        tokenId: tokenId,
                    }
                },
                amountBuy: nftAmount,
                include_fees: false,
            })
            gres = res;
            break;
        }
        default:
            gres = {
                "status": "error",
                "message": "Unknown order side",
            }
    }

    console.log(JSON.stringify(gres));

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
