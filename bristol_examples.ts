
import { video_in, video_out } from "@xstream/gstreamer"

//some BIO cams

let BRISTOL_SQUARE="rtsp://rtsp_server:8554/bio/w_6/IMG_6334.MOV_640x360.h264"
let BRISTOL_WATERFRONT="rtsp://rtsp_server:8554/bio/w_9/IMG_6306.MOV_640x360.h264"
let BRISTOL_STREET="rtsp://rtsp_server:8554/bio/w_5/IMG_6330.MOV_640x360.h264"
let BRISTOL_PTZ="rtsp://rtsp_server:8554/bio/w_15/IMG_6318.MOV_640x360.h264";
let BRISTOL_BRIDGE="rtsp://rtsp_server:8554/bio/w_3/IMG_6326.MOV_640x360.h264"


video_in({url: BRISTOL_SQUARE})
.pipe(video_out({name: 'bio'}))
