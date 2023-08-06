#/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from typing import Callable, Iterable
from pathlib import Path


class DirectoryStructure:
  """Creating a directory structure from iterable directory names

  Not validating the given `ds` to `add()`, don't test it
  """
  def __init__(self, root_dir: str):
    self.root_dir = Path(root_dir)
    self.dirs = []

  def add(self,
          dirs: Iterable[str | Iterable[str]],
          parent_dir: Path | None = None
  ) -> None:
    """Generating the parent and child `dirs` to `create()`
    """
    if parent_dir is None:
      parent_dir = self.root_dir
    if not dirs:
      self.dirs.append(parent_dir)
    for parent in dirs:
      if not isinstance(parent, str):
        # `root/a/b` will be replaced with `root/a/b/c`
        self.add(parent, self.dirs.pop())
        continue
      self.dirs.append(parent_dir / parent)

  def create(self) -> None:
    """Super-mkdir; create a leaf directory and all intermediate ones
    """
    for child_dir in self.dirs:
      os.makedirs(child_dir, exist_ok=True)


class Rule:
  """Rules to the directories and files
  """
  def __init__(self, path: str) -> None:
    self.path = Path(path)
    self.dir_rules = tuple()
    self.file_rules = tuple()
    self.shared_rules = tuple()

  def set_dir_rules(self, *rules: Callable) -> None:
    """Directory specific rules
    """
    self.dir_rules = rules

  def set_file_rules(self, *rules: Callable) -> None:
    """File specific rules
    """
    self.file_rules = rules

  def add(self, *rules: Callable) -> None:
    """Rules for both, directories and files
    """
    self.shared_rules.extend(rules)

  def execute(
      self, exec_path: Path | None = None, recursive: bool = True
  ) -> None:
    """Executes the rules, for files, for directories and for both
    """
    if exec_path is None:
      exec_path = self.path

    if not exec_path.exists():
      return None

    if exec_path.isfile():
      for fr in self.file_rules:
        exec_path = fr(exec_path)

    if exec_path.isdir():
      for dr in self.dir_rules:
        exec_path = dr(exec_path)

    for sr in self.shared_rules:
      exec_path = sr(exec_path)

    if not recursive:
      return None

    for child in exec_path.iterdirs():
      self.execute(child, recursive)
