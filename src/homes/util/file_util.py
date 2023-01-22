"""This module provides file string concatenation and creation functions."""


import os

__all__ = ["FileUtil"]


class FileUtil:
    """FileUtil can concatenates the path with the project path.

    And some basic file path functions will be provided, such as
    concatenate path string, create dir.
    """

    # Current project location.
    CURRENT_PROJECT_LOCATION: str = "./"

    @classmethod
    def splice_project_location(cls, target: str) -> str:
        """concatenates the path with the project string.

        Args:
            target (str): The target path.

        Returns:
            str: Result.
        """
        return os.path.join(cls.CURRENT_PROJECT_LOCATION, target)

    @staticmethod
    def make_dirs(path: str, flags: int) -> None:
        """Create folders recursively.

        Args:
            path (str): Target folder.
            flags (int): Flags.
        """
        if not os.path.exists(path):
            os.makedirs(path, flags, True)

    @staticmethod
    def absolute_path(filename: str) -> str:
        """Turn the file path into its absolute path.

        Args:
            filename (str): File path.

        Returns:
            str: Return the absolute path.
        """
        return os.path.abspath(filename)

    @staticmethod
    def relative_path(filename: str, start: str) -> str:
        """Turn the file path into its relative path.

        Args:
            filename (str): File path.

        Returns:
            str: Return the relative path.
        """
        return os.path.relpath(filename, start)

    @staticmethod
    def concat_path(source: str, target: str) -> str:
        """Concatenate source with target.

        Args:
            source (str): Source path.
            target (str): Target path.

        Returns:
            str: Return the concatenated string.
        """
        return os.path.join(source, target)
