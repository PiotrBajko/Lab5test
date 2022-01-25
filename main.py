from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
import io
from base64 import encodebytes
from PIL import Image

from jsonrpc import JSONRPCResponseManager, dispatcher

def get_response_image(image):
    byte_arr = io.BytesIO()
    image.save(byte_arr, format='PNG') # convert the PIL image to byte array
    encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii') # encode as base64
    return encoded_img


@dispatcher.add_method
def foobar(**kwargs):
	x1 = kwargs["x1"]
	x2 = kwargs["x2"]
	y1 = kwargs["y1"]
	y2 = kwargs["y2"]
	im = Image.open("mapa.png")
	crop_rectangle = (x1, y1, x2, y2)
	cropped_im = im.crop(crop_rectangle)
	encoded_img = get_response_image(cropped_im)
	return encoded_img


@Request.application
def application(request):
    # Dispatcher is dictionary {<method_name>: callable}
    dispatcher["echo"] = lambda s: s
    dispatcher["add"] = lambda a, b: a + b

    response = JSONRPCResponseManager.handle(
        request.data, dispatcher)
    return Response(response.json, mimetype='application/json')


if __name__ == '__main__':
    run_simple('localhost', 4000, application)