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
    const contractAddr = process.env.CONTRACT_ADDR!.toLowerCase();
    const ownerPublicKey = process.env.OWNER_PUBLIC_KEY!;
    const projectId = process.env.PROJECT_ID!;

    const description = process.env.DESCRIPTION!;
    const iconUrl = process.env.ICON_URL!;
    const metadataApiUrl = process.env.METADATA_API_URL!;
    const collectionImageUrl = process.env.COLLECTION_IMAGE_URL!;
    ////////////////////////////////////////////////////////////////////////////////

    const client = await CreateIMXClient(pk, network, gasLimit, gasPrice);
    const res = await client.createCollection({
        name: name,
        contract_address: contractAddr,
        owner_public_key: ownerPublicKey,
        project_id: parseInt(projectId),
        icon_url: iconUrl,
        metadata_api_url: metadataApiUrl,
        collection_image_url: collectionImageUrl,
        description: description,
    });

    let msg = {
        "status": "okay",
        "message": res,
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
