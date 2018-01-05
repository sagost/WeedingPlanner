# -*- coding: utf-8 -*-
"""
/***************************************************************************
 WeedingPlanner
                                 A QGIS plugin
 Create weeding plan from NDVI image
                             -------------------
        begin                : 2016-03-22
        copyright            : (C) 2016 by Salvatore Agosta / SAL Engineering s.r.l.
        email                : sagosta@salengineering.it
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load WeedingPlanner class from file WeedingPlanner.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .weeding_planner import WeedingPlanner
    return WeedingPlanner(iface)
