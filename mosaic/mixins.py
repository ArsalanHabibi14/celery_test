from django.http import JsonResponse
from .models import *


class SetMosaicParameter:
    """ This Mixin is use to check the Mosaic Parameter """
    # Set A Dictionary of parameters
    parameter = {"cell_size": 250, "cut_size": 40, "color_enhance": 0, "blend": 0.5, "repeat": 50, "fill": "seq",
                 "candidates": 20, "radius": 2}

    def dispatch(self, request, *args, **kwargs):
        """ Check And Save The All Parameter """
        data = dict(request.POST)  # Get Data From The Request
        # List The Parameters
        parameter_list = ["cell_size", "cut_size", "color_enhance", "blend", "repeat", "fill", "candidates", "radius"]
        # Just For String Parameters
        string_parameter = ["fill"]
        float_parameter = ['color_enhance', 'blend']
        # Get The All Parameter And Check Them that is valid
        for s in parameter_list:
            # Check this requested Parameter is in the parameter list
            if s in data.keys():

                # and Check the requested parameter is String
                if s in string_parameter:

                    if data['fill'][0] != "seq" and data['fill'][0] != "random":
                        return JsonResponse({"detail": "The Fill Should be Sequence Or Random"})

                try:
                    # Try That Convert The Type of any parameter to the int
                    self.parameter[s] = int(data[s][0])

                except:
                    # Exception: Check The Requested Parameter in the string parameters and set that in parameter dictionary
                    if s in float_parameter:

                        self.parameter[s] = float(data[s][0])
                    elif s in string_parameter:
                        self.parameter[s] = data[s][0]

                    else:
                        # If it is not in the String Requested Parameter Just Return a Reponse
                        return JsonResponse({"detail": "The Type of parameter should be integer or float"})
        print(self.parameter)
        return super().dispatch(request, *args, **kwargs)


# ============================================
def set_mosaic_parameter(mosaic_id, parameter_dict):
    """ This Function is used to Set The Mosaic Parameter """
    get_mosaic = Mosaic.objects.filter(id=mosaic_id).first()
    # Set The Parameters
    get_mosaic.cell_size = parameter_dict["cell_size"]
    get_mosaic.cut_size = parameter_dict["cut_size"]
    get_mosaic.color_enhance = parameter_dict["color_enhance"]
    get_mosaic.blend = parameter_dict["blend"]
    get_mosaic.repeat = parameter_dict["repeat"]
    get_mosaic.fill = parameter_dict["fill"]
    get_mosaic.candidates = parameter_dict["candidates"]
    get_mosaic.radius = parameter_dict["radius"]
    get_mosaic.save()


# =================================================
def get_mosaic_model(pk, profile, company):
    get_mosaic = Mosaic.objects.filter(id=pk, user=profile, company=company).first()
    if get_mosaic is None:
        return False, Response({"detail": "Mosaic Not Found!"})
    return True, get_mosaic


# ================================================

def get_album_model(pk, profile, company):
    get_album = Album.objects.filter(id=pk, user=profile, company=company).first()
    if get_album is None:
        return False, Response({"detail": "Album Not Found!"})
    return True, get_album
