# imxpy

## TODO

Some text about this is a work in progress, and use at your own risk and blabla

Have a lot of todos, super prototypi rightnow

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

    # todo fix more examples for now look in the code
    future = client.mint(...)
    res = future.result()

    # if not interested in results, just make the internal pool shutdown
    # this will run all internal processes
    client.wait()
