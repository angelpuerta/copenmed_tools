from app.utils.singleton import singleton


@singleton
class ReasonBuilder:

    def build(self) -> Relations:
        raise NotImplementedError()
