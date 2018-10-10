import { ExternalOperator, Stream, InputPort, declare_external_op } from "@xstream/core"

interface HelloWorldOperator extends ExternalOperator<string> {
  in: InputPort<number>;
  $in: InputPort<number>;
  out: Stream<string>;
  $out: Stream<string>;
}

function pywrap_hello_world(params: {

}): HelloWorldOperator {
  let spec = {
    "blockType": "pywrap_hello_world",
    "functionName": "pywrap_hello_world",
    "version": "0.0.1",
    "paramsSpec": {},
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
  return declare_external_op<string, HelloWorldOperator>(spec)(params)
}

import { source } from "@xstream/core"
source("test/pywrap/input")
.pipe(pywrap_hello_world({}))
.sink("test/pywrap/output")
