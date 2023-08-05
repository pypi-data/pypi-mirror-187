from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, ClassVar, cast

from isolate.backends.remote import IsolateServer, IsolateServerConnection
from isolate.backends.settings import IsolateSettings
from isolate.interface import BoxedEnvironment, RemoteBox
from isolate.server.definitions import EnvironmentDefinition
from isolate_cloud.sdk import (
    UNSET,
    CloudKeyCredentials,
    FalCloudClient,
    FalConnection,
    MachineRequirements,
    ResultT,
)

MACHINE_TYPES = ["XS", "S", "M", "GPU"]


@dataclass
class HostedRemoteBox(RemoteBox):
    """Run on an hosted isolate server."""

    machine_type: str = "S"
    creds: CloudKeyCredentials | None = None

    def __post_init__(self):
        if self.machine_type not in MACHINE_TYPES:
            raise RuntimeError(
                f"Machine type {self.machine_type} not supported. Use one of: {' '.join(MACHINE_TYPES)}"
            )

    def wrap(
        self,
        definition: dict[str, Any],
        settings: IsolateSettings,
    ) -> BoxedEnvironment:
        definition = definition.copy()

        # Extract the kind of environment to use.
        kind = definition.pop("kind", None)
        assert kind is not None, f"Corrupted definition: {definition}"

        target_list = [{"kind": kind, "configuration": definition}]

        # Create a remote environment.
        return BoxedEnvironment(
            FalHostedServer(
                host=self.host,
                machine_type=self.machine_type,
                target_environments=target_list,
                creds=self.creds,
            ),
            pool_size=self.pool_size,
        )


@dataclass
class FalHostedServer(IsolateServer):
    machine_type: str
    BACKEND_NAME: ClassVar[str] = "hosted-isolate-server"
    creds: CloudKeyCredentials | None = None

    def open_connection(
        self,
        connection_key: list[EnvironmentDefinition],
    ) -> FalHostedServerConnection:
        return FalHostedServerConnection(
            self,
            self.host,
            connection_key,
            machine_requirements=MachineRequirements(machine_type=self.machine_type),
            creds=self.creds,
        )


@dataclass
class FalHostedServerConnection(IsolateServerConnection):
    host: str
    creds: CloudKeyCredentials | None = None
    machine_requirements: MachineRequirements | None = None
    _fal_cloud_client: FalCloudClient | None = None
    _fal_connection: FalConnection | None = None

    @property
    def fal_cloud_client(self) -> FalCloudClient:
        if self._fal_cloud_client:
            return self._fal_cloud_client

        if self.creds:
            cloud_key_creds = CloudKeyCredentials(
                self.creds.key_id, self.creds.key_secret
            )
            self._fal_cloud_client = FalCloudClient(self.host, cloud_key_creds)
        else:
            self._fal_cloud_client = FalCloudClient(self.host)
        return self._fal_cloud_client

    @property
    def fal_connection(self) -> FalConnection:
        if self._fal_connection:
            return self._fal_connection
        self._fal_connection = self.fal_cloud_client.connect()
        return self._fal_connection

    def run(
        self,
        executable: Callable[[], ResultT],
        *args: Any,
        **kwargs: Any,
    ) -> ResultT:
        results = self.fal_connection.run(
            executable, self.definitions, machine_requirements=self.machine_requirements
        )

        return_value = []
        for result in results:
            for log in result.logs:
                self.log(log.message, level=log.level, source=log.source)
            if result.result is not UNSET:
                return_value.append(result.result)
        return cast(ResultT, return_value[0])
