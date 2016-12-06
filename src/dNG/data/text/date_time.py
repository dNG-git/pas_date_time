# -*- coding: utf-8 -*-

"""
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?pas;datetime

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;mpl2
----------------------------------------------------------------------------
#echo(pasDateTimeVersion)#
#echo(__FILEPATH__)#
"""

# pylint: disable=import-error

from math import floor
from time import gmtime, strftime, time

from .l10n import L10n

class DateTime(object):
    """
"DateTime" provides formatting methods for text processing like localized
output.

:author:     direct Netware Group et al.
:copyright:  direct Netware Group - All rights reserved
:package:    pas
:subpackage: datetime
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    TYPE_DATE_LONG = 1
    """
Long date format
    """
    TYPE_DATE_SHORT = 2
    """
Short date format
    """
    TYPE_DATE_TIME_LONG = 3
    """
Long date and time format
    """
    TYPE_DATE_TIME_SHORT = 4
    """
Short date and time format
    """
    TYPE_TIME = 5
    """
Short date format
    """
    TYPE_YEAR = 6
    """
Year-only value
    """
    TYPE_YEAR_AND_MONTH = 7
    """
Year and month format
    """
    TYPE_FUZZY = 8
    """
Fuzzy timestamps
    """
    TYPE_FUZZY_DAY = 9
    """
Fuzzy timestamps up to one day, short date and time format afterwards
    """
    TYPE_FUZZY_MONTH = 10
    """
Fuzzy timestamps up to one month, short date and time format afterwards
    """
    TYPE_FUZZY_YEAR = 11
    """
Fuzzy timestamps up to one year, short date and time format afterwards
    """

    @staticmethod
    def format_l10n(_type, timestamp, tz = 0, dtconnector = None, hide_tz = False):
        """
Returns the formatted date and / or time.

:param _type: Defines the requested type that should be returned.
:param timestamp: An Unix timestamp
:param tz: The difference in hours west of UTC
:param dtconnector: An string that combines a date and the time.
:param hide_tz: True to hide the timezone information.

:return: (str) Formatted date and / or time
:since:  v0.2.00
        """

        _return = L10n.get("core_unknown")

        if (type(_type) is not int): _type = DateTime.get_type_int(_type)

        if (type(timestamp) in ( int, float )):
            L10n.init("pas_datetime")

            if (tz != 0):
                tz *= -1
                timestamp += (3600 * tz)
            #

            if (dtconnector is None): dtconnector = L10n.get("pas_datetime_connector", " - ")
            _time = gmtime(timestamp)

            if (_type in ( DateTime.TYPE_FUZZY,
                           DateTime.TYPE_FUZZY_DAY,
                           DateTime.TYPE_FUZZY_MONTH,
                           DateTime.TYPE_FUZZY_YEAR
                         )
               ):
                time_difference = time() - timestamp

                if (time_difference < 0
                    or (_type == DateTime.TYPE_FUZZY_DAY and time_difference > 86399)
                    or (_type == DateTime.TYPE_FUZZY_MONTH and time_difference > 2591999)
                    or (_type == DateTime.TYPE_FUZZY_YEAR and time_difference > 31535999)
                   ): _type = DateTime.TYPE_DATE_TIME_SHORT
                else: _return = DateTime.format_fuzzy_l10n(timestamp, _type, tz)
            #

            if (_type == DateTime.TYPE_YEAR): _return = strftime("%Y", _time)
            elif (_type == DateTime.TYPE_YEAR_AND_MONTH): _return = strftime(L10n.get("pas_datetime_year_and_month"), _time)
            elif (_type in ( DateTime.TYPE_DATE_SHORT,
                             DateTime.TYPE_DATE_TIME_SHORT
                           )
                 ): _return = strftime(L10n.get("pas_datetime_shortdate"), _time)
            elif (_type in ( DateTime.TYPE_DATE_LONG, DateTime.TYPE_DATE_TIME_LONG )):
                month = strftime("%m", _time)

                _return = "{0}{1}{2}".format(strftime(L10n.get("pas_datetime_longdate_1"), _time),
                                             L10n.get("pas_datetime_longdate_month_{0:d}".format(int(month))),
                                             strftime(L10n.get("pas_datetime_longdate_2"), _time)
                                            )
            #

            if (_type in ( DateTime.TYPE_DATE_TIME_SHORT, DateTime.TYPE_DATE_TIME_LONG, DateTime.TYPE_TIME )):
                if (_return != ""): _return += dtconnector
                _return += strftime(L10n.get("pas_datetime_time"), _time)

                if (not hide_tz):
                    _return += " {0}".format(L10n.get("core_timezone_gmt"))

                    tz_hours = int(tz)
                    tz_minutes = int((tz % 1) * 60)
                    tz_minutes_str = (":{0:0=2.0f}".format(tz_minutes) if (tz_minutes > 1) else ":00")

                    if (tz < 0): _return += "{0:d}{1}".format(tz_hours, tz_minutes_str)
                    if (tz > 0): _return += "+{0:d}{1}".format(tz_hours, tz_minutes_str)
                #
            #
        #

        return _return
    #

    @staticmethod
    def format_fuzzy_l10n(timestamp, _type = None, tz = 0):
        """
Returns a descriptive, formatted date and time like "just now" or "7 minutes
ago".

:param timestamp: An Unix timestamp
:param _type: Defines the requested type that should be returned.
:param tz: The difference in hours west of UTC

:return: (str) Descriptive, formatted date and time
:since:  v0.2.00
        """

        _return = L10n.get("core_unknown")

        if (_type is None): _type = DateTime.TYPE_FUZZY
        elif (type(_type) is not int): _type = DateTime.get_type_int(_type)

        if (_type in ( DateTime.TYPE_FUZZY,
                       DateTime.TYPE_FUZZY_DAY,
                       DateTime.TYPE_FUZZY_MONTH,
                       DateTime.TYPE_FUZZY_YEAR
                     )
            and type(timestamp) in ( int, float )
           ):
            L10n.init("pas_datetime")

            if (tz != 0):
                tz *= -1
                timestamp += (3600 * tz)
            #

            time_difference = time() - timestamp

            if (time_difference < 0
                or (_type == DateTime.TYPE_FUZZY_DAY and time_difference > 86399)
                or (_type == DateTime.TYPE_FUZZY_MONTH and time_difference > 2591999)
                or (_type == DateTime.TYPE_FUZZY_YEAR and time_difference > 31535999)
               ): _return = DateTime.format_l10n(DateTime.TYPE_DATE_TIME_SHORT, timestamp, tz)
            elif (time_difference < 60): _return = L10n.get("pas_datetime_fuzzy_just_now")
            elif (time_difference < 300): _return = L10n.get("pas_datetime_fuzzy_last_five_minutes")
            elif (time_difference < 7200):
                _return = "{0}{1:d}{2}".format(L10n.get("pas_datetime_fuzzy_minutes_ago_1"),
                                               floor(time_difference / 60),
                                               L10n.get("pas_datetime_fuzzy_minutes_ago_2")
                                              )
            elif (time_difference < 172800):
                _return = "{0}{1:d}{2}".format(L10n.get("pas_datetime_fuzzy_hours_ago_1"),
                                               floor(time_difference / 3600),
                                               L10n.get("pas_datetime_fuzzy_hours_ago_2")
                                              )
            elif (time_difference < 5184000):
                _return = "{0}{1:d}{2}".format(L10n.get("pas_datetime_fuzzy_days_ago_1"),
                                               floor(time_difference / 86400),
                                               L10n.get("pas_datetime_fuzzy_days_ago_2")
                                              )
            else:
                time_current = gmtime()
                time_given = gmtime(timestamp)

                if (time_difference < 63072000):
                    _return = "{0}{1:d}{2}".format(L10n.get("pas_datetime_fuzzy_months_ago_1"),
                                                   (((time_current.tm_year - time_given.tm_year) * 12)
                                                    + (time_current.tm_mon - time_given.tm_mon)
                                                    + (1 if ((time_current.tm_mday - time_given.tm_mday) > 15) else 0)
                                                    + (-1 if ((time_current.tm_mday - time_given.tm_mday) < -15) else 0)
                                                   ),
                                                   L10n.get("pas_datetime_fuzzy_months_ago_2")
                                                  )
                else:
                    _return = "{0}{1:d}{2}".format(L10n.get("pas_datetime_fuzzy_years_ago_1"),
                                                   ((time_current.tm_year - time_given.tm_year)
                                                    + (1 if ((time_current.tm_mon - time_given.tm_mon) > 6) else 0)
                                                    + (-1 if ((time_current.tm_mon - time_given.tm_mon) < -6) else 0)
                                                   ),
                                                   L10n.get("pas_datetime_fuzzy_years_ago_2")
                                                  )
                #
            #
        #

        return _return
    #

    @staticmethod
    def get_type_int(_type):
        """
Parses the given type parameter given as a string value.

:param _type: String type

:return: (int) Internal type
:since:  v0.2.00
        """

        if (_type == "date_long"): _return = DateTime.TYPE_DATE_LONG
        elif (_type == "date_short"): _return = DateTime.TYPE_DATE_SHORT
        elif (_type == "date_time_long"): _return = DateTime.TYPE_DATE_TIME_LONG
        elif (_type == "fuzzy"): _return = DateTime.TYPE_FUZZY
        elif (_type == "fuzzy_day"): _return = DateTime.TYPE_FUZZY_DAY
        elif (_type == "fuzzy_month"): _return = DateTime.TYPE_FUZZY_MONTH
        elif (_type == "fuzzy_year"): _return = DateTime.TYPE_FUZZY_YEAR
        elif (_type == "time"): _return = DateTime.TYPE_TIME
        elif (_type == "year"): _return = DateTime.TYPE_YEAR
        elif (_type == "year_and_month"): _return = DateTime.TYPE_YEAR_AND_MONTH
        else: _return = DateTime.TYPE_DATE_TIME_SHORT

        return _return
    #
#
