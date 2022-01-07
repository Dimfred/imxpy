# imxpy

## USE AT YOUR OWN RISK

THIS LIBRARY IS IN DEVELOPMENT AND CAN CONTAIN BUGS, USE AT YOUR OWN RISK! I WON'T BE RESPONSIBLE IF YOU LOSE YOUR MONEY!

## Build & Install

    // install npm

    // install all dependencies
    npm install

    // build the typescript file
    tsc

## Examples

    from imxpy import IMXClient

    client = IMXClient(
        net="<main/test>, n_workers=<number of async workers>, pk="<YOUR_PRIVATE_KEY>"
    )

    # see imx_objects for parameter types
    some_params = SomeParams()

    # the client returns a future
    future = client.some_function(some_params)
    # resolve the future
    res = future.result()

    # if not interested in returned results, make the client shutdown its running processes
    client.shutdown()

Other examples on how to use the `client` correctly can be found in `tests/test_imx_client.py`. Tests starting with `test_okay_*`, are meant to show the correct usage of the library, whereas the others show wrong behavior.

## Feature Overview

Fell free to submit any feature requests / proposals through the issues.

### Signable

- [x] `register`
- [x] `approveNFT`
- [x] `approveERC20`
- [x] `deposit`
- [ ] `depositCancel`
- [ ] `depositReclaim`
- [x] `prepareWithdrawal`
- [x] `completeWithdrawal`
- [x] `transfer`
- [x] `burn`
- [x] `signMessage` (it is there, but IMX currently just returns a success)
- [x] `mint`
- [x] `createOrder`
- [x] `cancelOrder`
- [x] `createTrade`
- [x] `createExchange`
- [x] `createProject`
- [x] `createCollection`
- [x] `updateCollection`
- [x] `addMetadataSchemaToCollection`
- [x] `updateMetadataSchemaByName`

### Database

- [x] `applications`
  - [x] `list`
  - [x] `details`
- [x] `assets`
  - [x] `list`
  - [x] `details`
- [x] `balances`
  - [x] `list`
  - [x] `token balance`
- [ ] `TLV Info`
- [ ] `collections`
  - [ ] `list`
  - [ ] `details`
  - [ ] `filters`
  - [ ] `metadataSchema`
- [ ] `depostis`
  - [ ] `list`
  - [ ] `details`
- [x] `mints`
  - [x] `mintable_token`
  - [x] `mintable_token_with_addr`
  - [x] `mints`
  - [x] `mints details`
- [ ] `orders
  - [x] `list`
  - [ ] `details`
- [x] `claims
- [x] `starkkeys`
- [x] `transfers`
- [ ] `withdrawals`
  - [ ] `list`
  - [ ] `details`
- [ ] `snapshot`
- [ ] `tokens`
  - [ ] `list`
  - [ ] `details`
- [x] `trades`
  - [x] `list`
  - [x] `details`

## Known Issues
