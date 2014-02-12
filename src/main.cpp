/*
  freeseer - vga/presentation capture software

  Copyright (C) 2014  Free and Open Source Software Learning Centre
  http://fosslc.org

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.

  For support, questions, suggestions or any other inquiries, visit:
  http://wiki.github.com/Freeseer/freeseer/
*/

#include <QGuiApplication>
#include <QQuickView>
#include <QThread>

#include "multimedia.h"

int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);

    QQuickView view;
    view.setSource(QUrl::fromLocalFile("application.qml"));
    view.show();

    Multimedia multimedia;
    multimedia.Initialize();
    multimedia.Start();
    QThread::sleep(5);
    multimedia.Stop();
    multimedia.Cleanup();

    return app.exec();
}
