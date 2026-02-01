import sys

sys.path.append("..")
from typing import Any, Callable, Dict, List, Optional
from .base import *
from .exceptions import *
from ..utils import log
import shlex
from uuid import uuid4 as uuid
import os


class State:
    _tf: Terraform
    _cmd: str

    def __init__(self, terraform_object: Terraform):
        self._cmd = "state"
        self._tf = terraform_object

    def list(
        self,
        address: Optional[str] = None,
        state_file: Optional[str] = None,
        id: Optional[str] = None,
        color: Optional[bool] = True,
        chdir: Optional[str] = None,
    ):
        cmd = [self._cmd, "list"]
        if not color:
            color = self._tf.color
        cmd.append(self._tf._build_arg("color", not color))
        cmd.append(self._tf._build_arg("state", state_file))
        cmd.append(self._tf._build_arg("id", id))
        if address:
            if isinstance(address, str):
                cmd.append(shlex.quote(address))
            elif isinstance(address, list):
                for item in address:
                    cmd.append(shlex.quote(item))

        result = self._tf.cmd(cmd, "Terraform state list", chdir=chdir)

        if not result.success:
            log.failed(
                f"Terraform state list failed in {result.duration}s", end_sub=True
            )
            raise TerraformError(
                "Failed to run terraform state list",
                "state list",
                result.command,
                result.stderr,
                result.duration,
            )
        log.success(
            f"Terraform state list completed in {result.duration}s", end_sub=True
        )
        return TerraformResult(True, result.stdout)

    def show(
        self,
        address: Optional[str] = None,
        state_file: Optional[str] = None,
        json: Optional[bool] = True,
        color: Optional[bool] = True,
        chdir: Optional[str] = None,
    ):
        cmd = [self._cmd, "list"]
        if not color:
            color = self._tf.color
        cmd.append(self._tf._build_arg("color", not color))
        cmd.append(self._tf._build_arg("state", state_file))
        cmd.append(self._tf._build_arg("json", json))
        if address:
            cmd.append(shlex.quote(address))
        result = self._tf.cmd(cmd, "Terraform state list", chdir=chdir)

        res = TerraformResult(True, result.stdout)
        if not result.success:
            log.failed(
                f"Terraform state list failed in {result.duration}s", end_sub=True
            )
            raise TerraformError(
                "Failed to run terraform state list",
                "state list",
                result.command,
                result.stderr,
                result.duration,
            )
        log.success(
            f"Terraform state list completed in {result.duration}s", end_sub=True
        )
        return res

    def mv(
        self,
        src: str,
        dest: str,
        dry_run: Optional[bool] = False,
        lock: Optional[bool] = False,
        lock_timeout: Optional[str] = None,
        state: Optional[str] = None,
        state_out: Optional[str] = None,
        backup: Optional[str] = None,
        backup_out: Optional[str] = None,
        ignore_remote_version: Optional[bool] = None,
        color: Optional[bool] = None,
        chdir: Optional[str] = None,
    ):
        cmd = [self._cmd, "mv"]
        if not color:
            color = self._tf.color
        cmd.append(self._tf._build_arg("color", not color))
        cmd.append(self._tf._build_arg("dry_run", dry_run))
        if lock is False:
            cmd.append(self._tf._build_arg("lock", lock))
        if lock_timeout != "0s":
            cmd.append(self._tf._build_arg("lock_timeout", lock_timeout))

        cmd.append(self._tf._build_arg("state", state))
        cmd.append(self._tf._build_arg("state_out", state_out))
        cmd.append(self._tf._build_arg("backup", backup))
        cmd.append(self._tf._build_arg("backup_out", backup_out))
        cmd.append(self._tf._build_arg("ignore_remote_version", ignore_remote_version))

        cmd.append(shlex.quote(src))
        cmd.append(shlex.quote(dest))

        result = self._tf.cmd(cmd, "Terraform state mv", chdir=chdir)

        res = TerraformResult(True, result.stdout)
        if not result.success:
            log.failed(f"Terraform state mv failed in {result.duration}s", end_sub=True)
            raise TerraformError(
                "Failed to run terraform state mv",
                "state mv",
                result.command,
                result.stderr,
                result.duration,
            )
        log.success(f"Terraform state mv completed in {result.duration}s", end_sub=True)
        return res

    def rm(
        self,
        address: str,
        dry_run: Optional[bool] = None,
        lock: Optional[bool] = None,
        lock_timeout: Optional[str] = None,
        state: Optional[str] = None,
        state_out: Optional[str] = None,
        backup: Optional[str] = None,
        ignore_remote_version: Optional[bool] = None,
        chdir: Optional[str] = None,
    ):
        cmd = [self._cmd, "rm"]
        cmd.append(self._tf._build_arg("dry_run", dry_run))
        if not lock:
            lock = self._tf.lock
        if not lock_timeout:
            lock_timeout = self._tf.lock_timeout
        if lock is False:
            cmd.append(self._tf._build_arg("lock", lock))
        if lock_timeout != "0s":
            cmd.append(self._tf._build_arg("lock_timeout", lock_timeout))

        cmd.append(self._tf._build_arg("state", state))
        cmd.append(self._tf._build_arg("state_out", state_out))
        cmd.append(self._tf._build_arg("backup", backup))
        cmd.append(self._tf._build_arg("ignore_remote_version", ignore_remote_version))

        cmd.append(shlex.quote(address))

        result = self._tf.cmd(cmd, "Terraform state rm", chdir=chdir)

        if not result.success:
            log.failed(f"Terraform state rm failed in {result.duration}s", end_sub=True)
            raise TerraformError(
                "Failed to run terraform state rm",
                "state rm",
                result.command,
                result.stderr,
                result.duration,
            )
        log.success(f"Terraform state rm completed in {result.duration}s", end_sub=True)
        return TerraformResult(True, result.stdout)

    def replace_provider(
        self,
        src_provider: str,
        dest_provider: str,
        auto_approve: Optional[bool] = None,
        lock: Optional[bool] = None,
        lock_timeout: Optional[str] = None,
        state: Optional[str] = None,
        state_out: Optional[str] = None,
        backup: Optional[str] = None,
        ignore_remote_version: Optional[bool] = None,
        chdir: Optional[str] = None,
    ):
        cmd = [self._cmd, "replace-provider"]
        if not lock:
            lock = self._tf.lock
        if not lock_timeout:
            lock_timeout = self._tf.lock_timeout
        if lock is False:
            cmd.append(self._tf._build_arg("lock", lock))
        if lock_timeout != "0s":
            cmd.append(self._tf._build_arg("lock_timeout", lock_timeout))

        cmd.append(self._tf._build_arg("auto_approve", auto_approve))
        cmd.append(self._tf._build_arg("state", state))
        cmd.append(self._tf._build_arg("state_out", state_out))
        cmd.append(self._tf._build_arg("backup", backup))
        cmd.append(self._tf._build_arg("ignore_remote_version", ignore_remote_version))

        cmd.append(shlex.quote(src_provider))
        cmd.append(shlex.quote(dest_provider))

        result = self._tf.cmd(cmd, "Terraform state replace-provider", chdir=chdir)

        if not result.success:
            log.failed(
                f"Terraform state replace-provider failed in {result.duration}s",
                end_sub=True,
            )
            raise TerraformError(
                "Failed to run terraform state replace-provider",
                "state replace-provider",
                result.command,
                result.stderr,
                result.duration,
            )
        log.success(
            f"Terraform state replace-provider completed in {result.duration}s",
            end_sub=True,
        )
        return TerraformResult(True, result.stdout)

    def pull(self, chdir: Optional[str] = None):
        cmd = [self._cmd, "pull"]

        result = self._tf.cmd(cmd, "Terraform state pull", chdir=chdir)

        if not result.success:
            log.failed(
                f"Terraform state pull failed in {result.duration}s",
                end_sub=True,
            )
            raise TerraformError(
                "Failed to run terraform state pull",
                "state pull",
                result.command,
                result.stderr,
                result.duration,
            )
        log.success(
            f"Terraform state pull completed in {result.duration}s",
            end_sub=True,
        )
        return TerraformResult(True, result.stdout)

    def push(
        self,
        file_path: Optional[str] = None,
        file_content: Optional[str] = None,
        force: Optional[bool] = False,
        ignore_remote_version: Optional[bool] = None,
        chdir: Optional[str] = None,
    ):
        cmd = [self._cmd, "push"]

        if file_content is None and file_path is None:
            log.error("No file path or content provided, please provide one")
            raise TerraformError(
                "Failed to run terraform state push",
                "state push",
                None,
                "No file path or content provided, please provide one",
                0,
            )
        cmd.append(self._tf._build_arg("force", force))
        cmd.append(self._tf._build_arg("ignore_remote_version", ignore_remote_version))
        if not chdir:
            chdir = self._tf.chdir

        if file_content is not None:
            filename = f"terraform-temp-state-{uuid()}.tfstate"
            with open(os.path.normpath(os.path.join(chdir, filename)), "w") as file:
                res = file.write(file_content)
                if res == len(file_content):
                    log.info("Created temp state file")
            file_path = filename

        cmd.append(shlex.quote(file_path))

        result = self._tf.cmd(cmd, "Terraform state push", chdir=chdir)

        if file_content is not None:
            os.unlink(os.path.normpath(os.path.join(chdir, file_path)))

        res = TerraformResult(True, result.stdout)
        if not result.success:
            log.failed(
                f"Terraform state push failed in {result.duration}s",
                end_sub=True,
            )
            raise TerraformError(
                "Failed to run terraform state push",
                "state push",
                result.command,
                result.stderr,
                result.duration,
            )
        log.success(
            f"Terraform state push completed in {result.duration}s",
            end_sub=True,
        )
        return res
