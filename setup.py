#!/usr/bin/env python

import re
from pathlib import Path
from subprocess import check_call

from setuptools import Command, find_packages, setup


def read_app_metadata():
    content = (
        Path(__file__).parent.joinpath("app", "__init__.py").read_text(encoding="utf-8")
    )

    def find_value(name: str) -> str:
        match = re.search(
            rf'^{re.escape(name)}\s*=\s*["\']([^"\']+)["\']\s*$',
            content,
            flags=re.MULTILINE,
        )
        if not match:
            raise RuntimeError(f"Unable to find {name} in app/__init__.py")
        return match.group(1)

    return {
        "name": find_value("__appname__"),
        "version": find_value("__version__"),
        "description": find_value("__description__"),
    }


metadata = read_app_metadata()

cmdclass = {}


class bdist_app(Command):
    """Custom command to build the application."""

    description = "Build the application"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        check_call(["pyinstaller", "-y", "app.spec"])


cmdclass["bdist_app"] = bdist_app

setup(
    name=metadata["name"],
    version=metadata["version"],
    packages=find_packages(),
    description=metadata["description"],
    author="Namuan",
    author_email="info@deskriders.dev",
    license="MIT",
    url="https://deskriders.dev",
    entry_points={
        "gui_scripts": ["task-rider=app.__main__:main"],
    },
    cmdclass=cmdclass,
)
