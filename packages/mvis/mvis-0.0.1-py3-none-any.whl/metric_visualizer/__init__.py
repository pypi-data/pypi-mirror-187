# -*- coding: utf-8 -*-
# file: __init__.py.py
# time: 03/02/2022
# author: yangheng <yangheng@m.scnu.edu.cn>
# github: https://github.com/yangheng95
# Copyright (C) 2021. All Rights Reserved.

__version__ = "0.0.1"
__name__ = "mvis"

from .core import MetricVisualizer

from update_checker import UpdateChecker

checker = UpdateChecker()
check_result = checker.check(__name__, __version__)

if check_result:
    print(check_result)
