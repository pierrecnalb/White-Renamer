#!/usr/bin/python3

# Copyright (C) 2015-2016 Pierre Blanc
#
# This file is part of WhiteRenamer.
#
# WhiteRenamer is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# WhiteRenamer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with WhiteRenamer. If not, see <http://www.gnu.org/licenses/>.

import ActionType

class AddAction(ActionType):
    """"""
    def __init__(self, action_location):
        ActionType.__init__(action_location)

    def add_custom_name(self, name):
        return CustomNameAction(name)

    def add_folder_name(self):
        return FolderNameUsageAction()

    def add_date(self, is_modified_date, format_display):
        return DateAction(is_modified_date, format_display)

    def add_counter(self, start_at, increment, digit_number):
        return Counter(start_at, increment, digit_number)

    def add_image_date(self, time_format):
        return ImageDateTimeOriginal(time_format)

    def add_image_f_number(self):
        return ImageFNumber()

    def add_image_exposure_time(self):
        return ImageExposureTime()

    def add_image_iso(self):
        return ImageISO()

    def add_image_camera_model(self):
        return ImageCameraModel()

    def add_image_x_dimension(self):
        return ImageXDimension()

    def add_image_y_dimension(self):
        return ImageYDimension()

    def add_image_focal_length(self):
        return ImageFocalLength()

    def add_image_artist(self):
        return ImageArtist()

    def add_music_artist():
        return MusicArtist()

    def MusicTitle(self):
        return MusicTitle()

    def MusicYear(self):
        return MusicYear()

    def MusicAlbum(self):
        return MusicAlbum()

    def MusicTrack(self):
        return MusicTrack()

    def MusicGenre(self):
        return MusicGenre()
