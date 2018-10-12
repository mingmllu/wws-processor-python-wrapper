from wws_wrap import StreamOperator, wws_start
import json

class PeopleCountingOperator(StreamOperator):

    block_type = 'pywrap_count_people'
    input_ports = [('in', str)]
    output_ports = [('out', str)]

    def __init__(self, inputs, outputs, camera: str, **kwargs):
        StreamOperator.__init__(self, inputs, outputs)
        self._camera = camera  # A name assigned to the processor

    def process(self, data, key=None):
        output_dict = { "camera" : self._camera, "count_person" : 0 }
        # will set input type hints to JSON directly
        data_double_quotes = data.replace("\'", "\"") #JSON strings must use double quotes
        data_dict = json.loads(data_double_quotes)
        if "payload" in data_dict:
            if "objects" in data_dict["payload"]:
                if "detections" in data_dict["payload"]["objects"]:
                   detect_obj_list = data_dict["payload"]["objects"]["detections"]
                   for detect_obj in detect_obj_list:
                       if "class" in detect_obj:
                           if detect_obj["class"]["name"] == "person":
                             if detect_obj["confidence"] >= 0.7:
                                 output_dict["count_person"] += 1
        yield 'out', output_dict

if __name__ == '__main__':
    wws_start()
