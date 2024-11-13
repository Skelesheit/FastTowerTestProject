from fastapi_admin.resources import Model, Dropdown
from fasttower import admin

from tmpk import models


@admin.site.app.register
class TmpkTabMenu(Dropdown):
    label = "Tmpks"
    icon = "fas fa-bars"
    resources = []
    title = "Tmpks"