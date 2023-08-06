from .bias import Bias
from .dark import Dark
from .defects import Defects
from .detcal import DetCal
from .eper import Eper
from .fe55 import Fe55
from .gain import Gain
from .linearity import Linearity
from .metrology import Metrology
from .pocketpump import PocketPump
from .prnu import Prnu
from .ptc import Ptc
from .qe import Qe
from .ramp import Ramp
from .superflat import Superflat


def load(testers="all"):
    """
    Load the testers as azcam tools.
    """

    if testers == "all":
        bias = Bias()
        dark = Dark()
        defects = Defects()
        detcal = DetCal()
        eper = Eper()
        fe55 = Fe55()
        gain = Gain()
        linearity = Linearity()
        metrology = Metrology()
        pocketpump = PocketPump()
        prnu = Prnu()
        ptc = Ptc()
        qe = Qe()
        ramp = Ramp()
        superflat = Superflat()

    return
