from js import document


class PnButton:

    def __init__(self, label: str, onclick=None):
        div = document.createElement("div")
        div.innerHTML = f"<button>{label}</button>"

        self._proxy = div.firstChild
        if onclick is not None:
            self.onclick = onclick
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
