import { CreateIMXClient } from "./imx"


(async (): Promise<void> => {
    ////////////////////////////////////////////////////////////////////////////////
    // GENERAL
    const pk = process.env.PRIVATE_KEY!;
    const network = process.env.NETWORK!;
    const gasLimit = process.env.GAS_LIMIT;
    const gasPrice = process.env.GAS_PRICE;
    // SPECIFIC
    const mintToAddr = process.env.MINT_TO_ADDR!.toLowerCase();
    const tokens = JSON.parse(process.env.TOKENS!);
    const contractAddr = process.env.CONTRACT_ADDR!.toLowerCase();

    let royalties;
    if (process.env.ROYALTIES !== "") {
        royalties = JSON.parse(process.env.ROYALTIES!);
    }
    else {
        royalties = [];
    }
    ////////////////////////////////////////////////////////////////////////////////

    const client = await CreateIMXClient(pk, network, gasLimit, gasPrice);
    const res = await client.mintV2([
        {
            contractAddress: contractAddr,
            royalties: royalties,
            users: [{
                etherKey: mintToAddr,
                tokens: tokens
            }],
        }
    ]);

    let res_ = {
        "status": "success",
        "message": res["results"]
    }

    console.log(JSON.stringify(res_));

})().catch((e) => {
    let msgStr = e.message.toString();
    let msg = JSON.parse(msgStr)["message"]
    let err = {
        "status": "error",
        "message": msg,
        "tokens": JSON.parse(process.env.TOKENS!)!
    }
    console.log(JSON.stringify(err));

    process.exit(1);
});
