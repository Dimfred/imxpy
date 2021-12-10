# imxpy

## USE AT YOUR OWN RISK

THIS LIBRARY IS IN DEVELOPMENT AND CAN CONTAIN BUGS, USE AT YOUR OWN RISK! I WON'T BE RESPONSIBLE IF YOU LOSE YOUR MONEY!

## Build & Install

    // install npm

    // install all dependencies
    npm install

    // build the typescript files
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

## TODO

- client features:
  - ~~withdraw~~
  - ~~sell order~~
  - ~~cancel order~~
  - ~~create trade~~
  - buy order?

- database features:
  - almost every is missing except for transfer, asset n stuff
  - write tests for database features
  - parse the inputs, as well as the results into pydantic objects
