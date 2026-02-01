from typing import Any, Callable, Dict, List, Optional
from .base import *
from .exceptions import *
from ..utils import log
import shlex


class Workspace:
    _tf: Terraform
    _cmd: str

    def __init__(self, terraform_object: Terraform, workspace_name: str = "default"):
        self._cmd = "workspace"
        self.current = workspace_name
        self._tf = terraform_object

    def list(
        self,
        quiet: Optional[bool] = False,
        color: Optional[bool] = True,
        chdir: Optional[str] = None,
    ) -> TerraformResult[bool, List[str]]:
        cmd = [self._cmd, "list"]
        if not color:
            color = self._tf.color
        cmd.append(self._tf._build_arg("color", not color))

        result = self._tf.cmd(
            cmd, "Terraform workspace list", chdir=chdir, show_output=not quiet
        )

        if not result.success:
            if not quiet:
                log.failed(
                    f"Terraform workspace list failed in {result.duration}s",
                    end_sub=True,
                )
            raise TerraformError(
                "Failed to execute terraform workspace list",
                "workspace list",
                result.command,
                result.stderr,
                result.duration,
            )
        if not quiet:
            log.success(
                f"Terraform workspace list succeded in {result.duration}s", end_sub=True
            )
        self.current = (
            list(
                filter(
                    lambda x: len(x.strip()) > 0 and "*" in x,
                    result.stdout.splitlines(),
                )
            )[0]
            .replace("*", "")
            .strip()
        )
        log.set_env(self.current)

        res = TerraformResult(
            result.success,
            [line.replace("*", "").strip() for line in result.stdout.splitlines()],
        )
        res.result = list(filter(lambda x: len(x) > 0, res.result))
        return res

    def select(
        self,
        workspace: str,
        or_create: Optional[bool] = False,
        color: Optional[bool] = None,
        chdir: Optional[str] = None,
        quiet: Optional[bool] = False,
    ) -> TerraformResult:
        cmd = [self._cmd, "select"]

        if not color:
            color = self._tf.color
        cmd.append(self._tf._build_arg("color", not color))
        if or_create is True:
            if (
                self._tf.version_dict["version"]["major"] >= 1
                and self._tf.version_dict["version"]["minor"] >= 4
            ):
                cmd.append(self._tf._build_arg("or_create", or_create))
            else:
                existing = self.list(True, color=color, chdir=chdir).result
                if workspace not in existing:
                    if not quiet:
                        log.warn(
                            "The arg -or-create is available since version 1.4.x, and your version is",
                            self._tf.version_dict["version_str"],
                            "Using alternate method",
                        )
                    return self.new(workspace, color=color, chdir=chdir)
        cmd.append(shlex.quote(workspace))

        result = self._tf.cmd(
            cmd, "Terraform workspace select", chdir=chdir, show_output=not quiet
        )

        if not result.success:
            if not quiet:
                log.failed(
                    f"Terraform workspace select failed in {result.duration}s",
                    end_sub=True,
                )
            raise TerraformError(
                "Failed to execute terraform workspace list",
                "workspace select",
                result.command,
                result.stderr,
                result.duration,
            )
        if not quiet:
            log.success(
                f"Terraform workspace select succeded in {result.duration}s",
                end_sub=True,
            )
        self._tf.workspace = workspace
        self.current = workspace
        log.set_env(workspace)
        return TerraformResult(result.success, workspace)

    def new(
        self,
        workspace: str,
        lock: Optional[bool] = None,
        lock_timeout: Optional[str] = None,
        state: Optional[str] = None,
        color: Optional[bool] = None,
        chdir: Optional[str] = None,
    ) -> TerraformResult:
        cmd = [self._cmd, "new"]
        if not lock:
            lock = self._tf.__lock__
        if not color:
            color = self._tf.color
        if not lock_timeout:
            lock_timeout = self._tf.__lock_timeout__

        cmd.append(self._tf._build_arg("lock", lock))
        cmd.append(self._tf._build_arg("color", not color))
        cmd.append(self._tf._build_arg("lock_timeout", lock_timeout))
        cmd.append(self._tf._build_arg("state", state))

        cmd.append(shlex.quote(workspace))

        result = self._tf.cmd(cmd, "Terraform workspace new", chdir=chdir)

        if not result.success:
            log.failed(
                f"Terraform workspace new failed in {result.duration}s", end_sub=True
            )
            raise TerraformError(
                "Failed to execute terraform workspace new",
                "workspace new",
                result.command,
                result.stderr,
                result.duration,
            )
        log.success(
            f"Terraform workspace new succeded in {result.duration}s", end_sub=True
        )
        self._tf.workspace = workspace
        self.current = workspace
        log.set_env(workspace)
        return TerraformResult(result.success, workspace)
