import { ExternalOperator, Stream, InputPort, declare_external_op } from "@xstream/core"

interface PeopleCountingOperator extends ExternalOperator<string> {
  in: InputPort<string>;
  $in: InputPort<string>;
  out: Stream<string>;
  $out: Stream<string>;
}

function pywrap_count_people(params: {
  camera: string,
  topic: string,
  confidence: number
}): PeopleCountingOperator {
  let spec = {
    "blockType": "pywrap_count_people",
    "functionName": "pywrap_count_people",
    "version": "0.0.1",
    "paramsSpec": {
        "camera": {
            "default": "unknown"
        },
        "topic": {
            "default": "wws"
        },
        "confidence": {
            "default": 0.7
        }
    },
    "inputSpec": {
        "in": {
            "default": true
        }
    },
    "outputSpec": {
        "out": {
            "default": true
        }
    },
    "meta": {
        "processor": "wws/pywrap"
    }
  }
  return declare_external_op<string, PeopleCountingOperator>(spec)(params)
}



import { source } from "@xstream/core"
import { video_in, video_out } from "@xstream/gstreamer"
import { object_detector, Models } from "@xstream/tensorflow"
//some BIO cams

let BRISTOL_SQUARE="rtsp://rtsp_server:8554/bio/w_6/IMG_6334.MOV_640x360.h264"
let BRISTOL_WATERFRONT="rtsp://rtsp_server:8554/bio/w_9/IMG_6306.MOV_640x360.h264"
let BRISTOL_STREET="rtsp://rtsp_server:8554/bio/w_5/IMG_6330.MOV_640x360.h264"
let BRISTOL_PTZ="rtsp://rtsp_server:8554/bio/w_15/IMG_6318.MOV_640x360.h264";
let BRISTOL_BRIDGE="rtsp://rtsp_server:8554/bio/w_3/IMG_6326.MOV_640x360.h264"

let v0=video_in({url: BRISTOL_SQUARE})
let o0=object_detector({model: Models.FAST, fps:1})
v0.pipe(o0).pipe(video_out({name: 'video_after'}))
v0.pipe(video_out({name: 'video_before'}))
o0.event.sink("event_JSON_results")
o0.event.pipe(pywrap_count_people({camera: 'BRISTOL_SQUARE', confidence: 0.7, topic: 'wws_video'}))
.sink("count_people")