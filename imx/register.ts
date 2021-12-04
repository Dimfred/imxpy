import { CreateIMXClient, waitForTransaction } from "./imx"


(async (): Promise<void> => {
    ////////////////////////////////////////////////////////////////////////////////
    // GENERAL
    const pk = process.env.PRIVATE_KEY!;
    const network = process.env.NETWORK!;
    const gasLimit = process.env.GAS_LIMIT;
    const gasPrice = process.env.GAS_PRICE;
    ////////////////////////////////////////////////////////////////////////////////

    const client = await CreateIMXClient(pk, network, gasLimit, gasPrice);
    const res = await client.registerImx({
        etherKey: client.address.toLowerCase(),
        starkPublicKey: client.starkPublicKey,
    });

    if (res.tx_hash !== "")
        await waitForTransaction(Promise.resolve(res.tx_hash));

    let msg = {
        "status": "okay",
        "message": res.tx_hash,
        "addr": client.address.toLowerCase(),
    }
    console.log(JSON.stringify(msg));

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
