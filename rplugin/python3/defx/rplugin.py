# ============================================================================
# FILE: rplugin.py
# AUTHOR: Shougo Matsushita <Shougo.Matsu at gmail.com>
# License: MIT license
# ============================================================================

import typing

from defx.clipboard import Clipboard
from defx.view import View
from defx.util import error, Nvim


class Rplugin:

    def __init__(self, vim: Nvim) -> None:
        self._vim = vim
        self._views: typing.List[View] = []
        self._clipboard = Clipboard()

    def init_channel(self) -> None:
        self._vim.vars['defx#_channel_id'] = self._vim.channel_id

    def start(self, args: typing.List[typing.Any]) -> None:
        [paths, context] = args
        views = [x for x in self._views
                 if context['buffer_name'] == x._context.buffer_name]
        if not views or context['new']:
            view = View(self._vim, len(self._views))
            views = [view]
            self._views.append(view)
        views[0].init(paths, context, self._clipboard)

    def do_action(self, args: typing.List[typing.Any]) -> None:
        for view in [x for x in self._views
                     if x._bufnr == self._vim.current.buffer.number]:
            view.do_action(args[0], args[1], args[2])
            return

        error(self._vim, 'Invalid defx buffer is detected!')
