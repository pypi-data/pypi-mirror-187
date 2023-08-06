from js import document
from pynanto.remote.widget import Widget


class PnSlider:

    def __init__(self):
        w = Widget(f'<input type="range">')
        self._proxy = w.container.firstChild
        document.body.append(w.container)

    def __getattr__(self, attr):
        if attr == '_proxy':
            return self._proxy
        return getattr(self._proxy, attr)

    def __setattr__(self, key, value):
        if key == '_proxy':
            super().__setattr__(key, value)
        else:
            setattr(self._proxy, key, value)
