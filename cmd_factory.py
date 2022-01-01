import sys
from pathlib import Path


class CMDFactory:
    @staticmethod
    def make(base_params, params):
        if sys.platform == "linux":
            envkw = "export"
            separator = ";"
            encloser = "'"
        elif sys.platform == "win32":
            envkw = "set"
            separator = "&"
            encloser = ""
        else:
            raise ValueError(f"Unsupported platform: {sys.platform}")

        set_env = (
            lambda varname, var: f"{envkw} {varname}={encloser}{var}{encloser} {separator} "
        )

        working_dir = Path(__file__).parent
        cmd = f'cd "{working_dir}" {separator} '
        cmd += set_env("BASE_PARAMS", f"{base_params.json()}")
        cmd += set_env("PARAMS", f"{params.json() if params is not None else {}}")
        cmd += f"node ./build/imx.js"

        return cmd
