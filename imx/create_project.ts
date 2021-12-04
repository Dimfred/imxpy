import { CreateIMXClient } from "./imx"


(async (): Promise<void> => {
    ////////////////////////////////////////////////////////////////////////////////
    // GENERAL
    const pk = process.env.PRIVATE_KEY!;
    const network = process.env.NETWORK!;
    const gasLimit = process.env.GAS_LIMIT;
    const gasPrice = process.env.GAS_PRICE;

    // SPECIFIC
    const name = process.env.NAME!;
    const companyName = process.env.COMPANY_NAME!;
    const contactEmail = process.env.CONTACT_EMAIL!;
    ////////////////////////////////////////////////////////////////////////////////

    const client = await CreateIMXClient(pk, network, gasLimit, gasPrice);
    const res = await client.createProject({
        name: name,
        company_name: companyName,
        contact_email: contactEmail,
    });

    let msg = {
        "status": "okay",
        "message": res.id,
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
