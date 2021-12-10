"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.waitForTransaction = exports.CreateIMXClient = void 0;
var ethers_1 = require("ethers");
var providers_1 = require("@ethersproject/providers");
var wallet_1 = require("@ethersproject/wallet");
var imx_sdk_1 = require("@imtbl/imx-sdk");
var provider = new providers_1.AlchemyProvider('ropsten', "DvukuyBzEK-JyP6zp1NVeNVYLJCrzjp_");
var networkParams = {
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
};
// TODO remove export later
var CreateIMXClient = function (privateKey, network, gasLimit, gasPrice) {
    if (gasLimit === void 0) { gasLimit = ""; }
    if (gasPrice === void 0) { gasPrice = ""; }
    return __awaiter(void 0, void 0, void 0, function () {
        var selectedNetwork, signer, client;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    if (network === "test")
                        selectedNetwork = networkParams.test;
                    else if (network === "main")
                        selectedNetwork = networkParams.main;
                    else
                        throw Error("[TYPESCRIPTWRAPPER]: Unknown network type: '" + network + "'");
                    signer = new wallet_1.Wallet(privateKey).connect(provider);
                    return [4 /*yield*/, imx_sdk_1.ImmutableXClient.build({
                            publicApiUrl: selectedNetwork.apiUrl,
                            signer: signer,
                            starkContractAddress: selectedNetwork.starkContractAddr,
                            registrationContractAddress: selectedNetwork.registratrionContractAddr,
                            gasLimit: gasLimit,
                            gasPrice: gasPrice,
                        })];
                case 1:
                    client = _a.sent();
                    return [2 /*return*/, client];
            }
        });
    });
};
exports.CreateIMXClient = CreateIMXClient;
// TODO remove export later
var waitForTransaction = function (promise) { return __awaiter(void 0, void 0, void 0, function () {
    var txId, receipt;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0: return [4 /*yield*/, promise];
            case 1:
                txId = _a.sent();
                console.log('Waiting for transaction', {
                    txId: txId,
                    etherscanLink: "https://ropsten.etherscan.io/tx/" + txId,
                    alchemyLink: "https://dashboard.alchemyapi.io/mempool/eth-ropsten/tx/" + txId,
                });
                return [4 /*yield*/, provider.waitForTransaction(txId)];
            case 2:
                receipt = _a.sent();
                if (receipt.status === 0) {
                    throw new Error('Transaction rejected');
                }
                console.log('Transaction Mined: ' + receipt.blockNumber);
                return [2 /*return*/, receipt];
        }
    });
}); };
exports.waitForTransaction = waitForTransaction;
var createSuccessMsg = function (msg) {
    return {
        "status": "success",
        "result": msg
    };
};
var createErrorMsg = function (msg) {
    return {
        "status": "error",
        "result": msg
    };
};
(function () { return __awaiter(void 0, void 0, void 0, function () {
    var baseParams, params, client, res, msg, _a;
    return __generator(this, function (_b) {
        switch (_b.label) {
            case 0:
                baseParams = JSON.parse(process.env.BASE_PARAMS);
                params = JSON.parse(process.env.PARAMS);
                return [4 /*yield*/, (0, exports.CreateIMXClient)(baseParams.pk, baseParams.network, baseParams.gas_limit, baseParams.gas_price)];
            case 1:
                client = _b.sent();
                _a = baseParams.function_name;
                switch (_a) {
                    case "register": return [3 /*break*/, 2];
                    case "create_project": return [3 /*break*/, 4];
                    case "create_collection": return [3 /*break*/, 6];
                    case "update_collection": return [3 /*break*/, 8];
                    case "create_metadata_schema": return [3 /*break*/, 10];
                    case "update_metadata_schema": return [3 /*break*/, 12];
                    case "transfer": return [3 /*break*/, 13];
                    case "mint": return [3 /*break*/, 15];
                    case "burn": return [3 /*break*/, 17];
                    case "prepare_withdrawal": return [3 /*break*/, 19];
                    case "complete_withdrawal": return [3 /*break*/, 21];
                    case "create_order": return [3 /*break*/, 23];
                }
                return [3 /*break*/, 25];
            case 2: return [4 /*yield*/, client.registerImx({
                    etherKey: client.address.toLowerCase(),
                    starkPublicKey: client.starkPublicKey
                })];
            case 3:
                res = _b.sent();
                msg = createSuccessMsg(res);
                return [3 /*break*/, 26];
            case 4: return [4 /*yield*/, client.createProject(params)];
            case 5:
                res = _b.sent();
                msg = createSuccessMsg(res);
                return [3 /*break*/, 26];
            case 6: return [4 /*yield*/, client.createCollection(params)];
            case 7:
                res = _b.sent();
                msg = createSuccessMsg(res);
                return [3 /*break*/, 26];
            case 8: return [4 /*yield*/, client.updateCollection(params.contractAddress, params.params)];
            case 9:
                res = _b.sent();
                msg = createSuccessMsg(res);
                return [3 /*break*/, 26];
            case 10: return [4 /*yield*/, client.addMetadataSchemaToCollection(params.contractAddress, params.params)];
            case 11:
                res = _b.sent();
                msg = createSuccessMsg(res);
                return [3 /*break*/, 26];
            case 12:
                {
                    // TODO
                    throw new Error("update_metadata_schema not implemented");
                    // res = await client.updateMetadataSchemaByName()
                    return [3 /*break*/, 26];
                }
                _b.label = 13;
            case 13:
                params.quantity = ethers_1.BigNumber.from(params.quantity);
                return [4 /*yield*/, client.transfer(params)];
            case 14:
                res = _b.sent();
                msg = createSuccessMsg(res);
                return [3 /*break*/, 26];
            case 15: return [4 /*yield*/, client.mintV2(params)];
            case 16:
                res = _b.sent();
                msg = createSuccessMsg(res);
                return [3 /*break*/, 26];
            case 17: return [4 /*yield*/, client.burn(params)];
            case 18:
                res = _b.sent();
                msg = createSuccessMsg(res);
                return [3 /*break*/, 26];
            case 19: return [4 /*yield*/, client.prepareWithdrawal(params)];
            case 20:
                res = _b.sent();
                msg = createSuccessMsg(res);
                return [3 /*break*/, 26];
            case 21:
                params["starkPublicKey"] = client.starkPublicKey;
                return [4 /*yield*/, client.completeWithdrawal(params)];
            case 22:
                res = _b.sent();
                msg = createSuccessMsg(res);
                return [3 /*break*/, 26];
            case 23: return [4 /*yield*/, client.createOrder(params)];
            case 24:
                res = _b.sent();
                msg = createSuccessMsg(res);
                return [3 /*break*/, 26];
            case 25:
                {
                    throw new Error("Invalid method name: '" + baseParams.method_name + "'");
                }
                _b.label = 26;
            case 26:
                // log result to stdout to be parsed by the python process
                console.log(JSON.stringify(msg));
                return [2 /*return*/];
        }
    });
}); })().catch(function (e) {
    var msgStr = e.message.toString();
    var msg;
    try {
        msg = JSON.parse(msgStr)["message"];
    }
    catch (e_) {
        msg = "[TYPESCRIPTWRAPPER]: " + e;
    }
    var err = createErrorMsg(msg);
    console.log(JSON.stringify(err));
    process.exit(1);
});
