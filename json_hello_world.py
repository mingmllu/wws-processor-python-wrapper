from wws_wrap import StreamOperator, wws_start
import json

class JsonHelloWorldOperator(StreamOperator):

    block_type = 'pywrap_json_hello_world'
    input_ports = [('in', str)]
    output_ports = [('out', str)]

    def __init__(self, inputs, outputs, **kwargs):
        StreamOperator.__init__(self, inputs, outputs)

    def process(self, data, key=None):
        output_dict = { "count_persons" : 0 }
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
                                 output_dict["count_persons"] += 1
        yield 'out', output_dict

if __name__ == '__main__':
    wws_start()
