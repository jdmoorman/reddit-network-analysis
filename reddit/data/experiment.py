import pathlib
from typing import List, IO, Union, TypeVar
import os
import glob

from .paths import LOCAL_BASE

T = TypeVar('T', bound='Experiment')

class Experiment(object):
	def __init__(self,
	             *,
	             name: str = "experiment",
	             existing: bool = False) -> None:
		self.base_path = pathlib.Path(LOCAL_BASE, name)
		count = 1
		while (not existing) and self.base_path.exists():
			self.base_path = pathlib.Path(LOCAL_BASE, name + str(count))
			count += 1

		self.base_path.mkdir(parents=True, exist_ok=True)

		if not existing:
			with open(self.base_path / ".gitignore", "w") as f:
				f.write("*")

	def glob(self,
	         name: str) -> List[str]:
		return glob.glob(str(self.base_path / name))

	def open(self,
	         name: str,
	         mode: str) -> IO:
		return open(self.base_path / name, mode)