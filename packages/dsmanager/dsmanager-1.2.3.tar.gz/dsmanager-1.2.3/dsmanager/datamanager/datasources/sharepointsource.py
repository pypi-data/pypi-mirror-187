"""@Author: Rayane AMROUCHE

Sharepoint Sources Handling.
"""

import os
import io

from typing import Any

from shareplum import Site  # type: ignore # pylint: disable=import-error
from shareplum import Office365  # type: ignore # pylint: disable=import-error
from shareplum.site import Version  # type: ignore # pylint: disable=import-error

# type: ignore # pylint: disable=import-error
from shareplum.site import _Site365


from dsmanager.datamanager.datasources.datasource import DataSource

from dsmanager.datamanager.datastorage import DataStorage

from dsmanager.controller.logger import Logger


class SharepointSource(DataSource):
    """Inherited Data Source Class for sharepoint sources."""

    schema_read = DataStorage(
        {
            "source_type": "sharepoint",
            "username_env_name": "onedrive_username_environment_variable_name",
            "password_env_name": "onedrive_password_environment_variable_name",
            "path": "https://sharepoint_address.sharepoint.com/sites/site_name/"
            "folder/file.xlsx",
            **DataSource._file_schema,
        }
    )

    @staticmethod
    @Logger.log_source(["path"])
    def read_source(
        path: str, username_env_name: str, password_env_name: str, **kwargs: Any
    ) -> Any:
        """Sharepoint source reader.

        Args:
            path (str): Url of the datasource.
            username_env_name (str): Name of the username env variable.
            password_env_name (str): Name of the password env variable.

        Returns:
            Any: Data from source.
        """
        path_split = path.split("/")
        authcookie = Office365(
            "/".join(path_split[:3]),
            username=os.getenv(username_env_name, ""),
            password=os.getenv(password_env_name, ""),
        ).GetCookies()
        site = Site(
            "/".join(path_split[:5]),
            version=Version.v365,
            authcookie=authcookie,
        )
        if not isinstance(site, _Site365):
            return None
        folder = site.Folder("/".join(path_split[5:-1]))
        file = folder.get_file(path_split[-1])

        if isinstance(file, bytes) and "encoding" in kwargs:
            try:
                file = io.StringIO(file.decode(kwargs["encoding"]))
            except UnicodeDecodeError:
                return file

        data = super(SharepointSource, SharepointSource)._decode_files(file, **kwargs)
        return data

    @staticmethod
    def read(source_info: dict, **kwargs: Any) -> Any:
        """Handle source and returns the source data.

        Args:
            source_info (dict): Source metadatas.

        Returns:
            Any: Source datas.
        """
        DataSource._load_source(source_info, **kwargs)
        sharepoint_path = source_info["path"]
        data = SharepointSource.read_source(
            path=sharepoint_path,
            username_env_name=source_info["username_env_name"],
            password_env_name=source_info["password_env_name"],
            **source_info["args"],
        )

        Logger.get_logger("datasource").info("Read data from '%s'.", sharepoint_path)
        return data
