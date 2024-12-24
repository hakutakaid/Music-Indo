#
# Copyright (C) 2024 by hakutakaid@Github, < https://github.com/hakutakaid >.
#
# This file is part of < https://github.com/hakutakaid/MusicIndo > project,
# and is released under the MIT License.
# Please see < https://github.com/hakutakaid/MusicIndo/blob/master/LICENSE >
#
# All rights reserved.
#


class AssistantErr(Exception):
    def __init__(self, errr: str):
        super().__init__(errr)


class UnableToFetchCarbon(Exception):
    pass
