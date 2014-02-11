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

#include "multimedia.h"


Multimedia::Multimedia()
{

}

void Multimedia::Initialize()
{
    gst_init(NULL, NULL);

    pipeline = gst_pipeline_new ("freeseer");
    source   = gst_element_factory_make ("ximagesrc", "desktopsrc");
    videoconvert = gst_element_factory_make ("videoconvert", "videoconvert");
    sink     = gst_element_factory_make ("autovideosink", "preview");

    bus = gst_pipeline_get_bus (GST_PIPELINE (pipeline));
    //bus_watch_id = gst_bus_add_watch (bus, bus_call, loop);
    gst_object_unref (bus);

    gst_bin_add_many (GST_BIN (pipeline),
                    source, videoconvert, sink, NULL);
    gst_element_link (source, videoconvert);
    gst_element_link (videoconvert, sink);

    gst_element_set_state (pipeline, GST_STATE_PLAYING);
    g_print ("Running...\n");
}

void Multimedia::Cleanup()
{
    g_print ("Returned, stopping playback\n");
    gst_element_set_state (pipeline, GST_STATE_NULL);

    g_print ("Deleting pipeline\n");
    gst_object_unref (GST_OBJECT (pipeline));
    //g_source_remove (bus_watch_id);
}
