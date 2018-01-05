# coding=utf-8
"""DockWidget test.

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

__author__ = 'sagosta@salengineering.it'
__date__ = '2016-03-22'
__copyright__ = 'Copyright 2016, Salvatore Agosta / SAL Engineering s.r.l.'

import unittest

from PyQt4.QtGui import QDockWidget

from weeding_planner_dockwidget import WeedingPlannerDockWidget

from utilities import get_qgis_app

QGIS_APP = get_qgis_app()


class WeedingPlannerDockWidgetTest(unittest.TestCase):
    """Test dockwidget works."""

    def setUp(self):
        """Runs before each test."""
        self.dockwidget = WeedingPlannerDockWidget(None)

    def tearDown(self):
        """Runs after each test."""
        self.dockwidget = None

    def test_dockwidget_ok(self):
        """Test we can click OK."""
        pass

if __name__ == "__main__":
    suite = unittest.makeSuite(WeedingPlannerDialogTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

