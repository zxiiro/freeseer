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

    recorder.pipeline_ = gst_pipeline_new ("freeseer");
    bus = gst_pipeline_get_bus (GST_PIPELINE (recorder.pipeline_));
    //bus_watch_id = gst_bus_add_watch (bus, bus_call, loop);
    gst_object_unref (bus);

    Recorder recorder;
}

void Multimedia::Cleanup()
{
    g_print ("Deleting pipeline\n");
    gst_object_unref (GST_OBJECT (recorder.pipeline_));
    //g_source_remove (bus_watch_id);
}

void Multimedia::Start()
{
    gst_element_set_state (recorder.pipeline_, GST_STATE_PLAYING);
    g_print ("Running...\n");
}

void Multimedia::Stop()
{
    g_print ("Returned, stopping playback\n");
    gst_element_set_state (recorder.pipeline_, GST_STATE_NULL);
}

/*
    PIPELINE MANIPULATION
*/
void Multimedia::LoadPipeline()
{

    recorder.videoconvert_ = gst_element_factory_make ("videoconvert", "videoconvert");
    recorder.sink_     = gst_element_factory_make ("ximagesink", "preview");

    gst_bin_add_many (GST_BIN (recorder.pipeline_), recorder.videoconvert_, recorder.sink_, NULL);
    gst_element_link (recorder.videoconvert_, recorder.sink_);
}

void Multimedia::LoadVideoSrc()
{
    recorder.source_ = gst_element_factory_make ("ximagesrc", "desktopsrc");
    gst_bin_add_many (GST_BIN (recorder.pipeline_), recorder.source_, NULL);
    gst_element_link (recorder.source_, recorder.videoconvert_);
}

void Multimedia::ChangeVideoSrc()
{

    GstPad* blockpad = gst_element_get_static_pad(recorder.videoconvert_, "src");
    gst_pad_add_probe(blockpad, GST_PAD_PROBE_TYPE_BLOCK_DOWNSTREAM,
      ChangeVideoSrcCB, &recorder, NULL);
}

GstPadProbeReturn Multimedia::ChangeVideoSrcCB(GstPad* pad, GstPadProbeInfo* info, gpointer user_data)
{
    gst_pad_remove_probe (pad, GST_PAD_PROBE_INFO_ID (info));
    g_print("Here");
    Recorder* recorder = (Recorder*) user_data;



    gst_element_set_state (recorder->sink_, GST_STATE_NULL);
    gst_bin_remove (GST_BIN (recorder->pipeline_), recorder->sink_);

    g_print("Fakesink");
    GstElement* sink = gst_element_factory_make ("autovideosink", "preview");
    gst_bin_add (GST_BIN (recorder->pipeline_), sink);
    gst_element_link_many (recorder->videoconvert_, sink, NULL);
    gst_element_set_state (sink, GST_STATE_PLAYING);

    return GST_PAD_PROBE_OK;
}
