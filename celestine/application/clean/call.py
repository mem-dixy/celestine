"""Run a bunch of auto formaters."""


from celestine.package import run


def clean(**star):
    """"""

    # run("pyupgrade")
    run("pydocstringformatter")
    # run("autoflake")
    # run("isort")
    #run("black")

    print("I am a talking cow.")
