from sardana.macroserver.macro import Macro, macro, Type
from tango import AttributeProxy
import json
from os.path import join


@macro(
    [
        ["roi_name", Type.String, None, "name of the roi in Environment/LaVue"],
        ["output", Type.Boolean, True, "output roi"],
        [
            "lavue_tango_path",
            Type.String,
            "rsxs/lavuecontroller/henry",
            "lavue TangoDS",
        ],
    ]
)
def roi_read(self, roi_name, output, lavue_tango_path):
    """Macro roi_read"""
    attr_proxy = AttributeProxy(join(lavue_tango_path, "DetectorROIs"))
    rois = json.loads(attr_proxy.read().value)
    try:
        roi = rois[roi_name]
        if output:
            self.output("{:s}: {:s}".format(roi_name, str(roi[0])))
        return roi[0]
    except KeyError:
        self.error('ROI "{:s}" not in Environment/LaVue'.format(roi_name))
        return []
