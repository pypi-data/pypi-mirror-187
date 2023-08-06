import ipywidgets as widgets
from traitlets import Unicode, Int, Float, Bool, List, validate
from .helpers import MplColorHelper

# See js/lib/faerun.js for the frontend counterpart to this file.


@widgets.register
class Faerun(widgets.DOMWidget):
    """An smiles_drawer.js widget."""

    # Name of the widget view class in front-end
    _view_name = Unicode("FaerunView").tag(sync=True)

    # Name of the widget model class in front-end
    _model_name = Unicode("FaerunModel").tag(sync=True)

    # Name of the front-end module containing widget view
    _view_module = Unicode("faerun-notebook").tag(sync=True)

    # Name of the front-end module containing widget model
    _model_module = Unicode("faerun-notebook").tag(sync=True)

    # Version of the front-end module containing widget view
    _view_module_version = Unicode("^0.1.6").tag(sync=True)
    # Version of the front-end module containing widget model
    _model_module_version = Unicode("^0.1.6").tag(sync=True)

    # Widget specific property.
    # Widget properties are defined as traitlets. Any property tagged with `sync=True`
    # is automatically synced to the frontend *any* time it changes in Python.
    # It is synced back to Python from the frontend *any* time the model is touched.
    x = List([]).tag(sync=True)
    y = List([]).tag(sync=True)
    z = List([]).tag(sync=True)
    c = List([]).tag(sync=True)
    s = List([]).tag(sync=True)
    t = List([]).tag(sync=True)
    cmap = Unicode("viridis").tag(sync=True)
    width = Int(400).tag(sync=True)
    height = Int(400).tag(sync=True)
    color = Unicode("#000000").tag(sync=True)
    background_color = Unicode("#ffffff").tag(sync=True)
    tree_color = Unicode(None, allow_none=True).tag(sync=True)
    view = Unicode("front").tag(sync=True)
    full_width = Bool(False).tag(sync=True)
    hovered_index = Int(-1).tag(sync=True)
    selected_index = Int(-1).tag(sync=True)
    has_legend = Bool(False).tag(sync=True)
    point_scale = Float(5.0).tag(sync=True)
    max_point_size = Float(20.0).tag(sync=True)

    @validate('c')
    def _values_to_colors(self, proposal):
        value = proposal.value
        helper = MplColorHelper(self.cmap, min(value), max(value))
        return helper.get_rgb(value)
