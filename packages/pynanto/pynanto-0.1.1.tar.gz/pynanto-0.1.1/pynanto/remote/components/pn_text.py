from js import document


class PnText:

    def __init__(self, text=None):
        div = document.createElement("div")
        if text is not None:
            div.innerHTML = text
        self._proxy = div
        document.body.append(div)

    def __getattr__(self, attr):
        if attr == '_proxy':
            return self._proxy
        return getattr(self._proxy, attr)

    def __setattr__(self, key, value):
        if key == '_proxy':
            super().__setattr__(key, value)
        else:
            setattr(self._proxy, key, value)
