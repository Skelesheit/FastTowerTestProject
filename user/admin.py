from fastapi_admin.resources import Model, Dropdown
from fasttower import admin

from user import models


@admin.site.app.register
class UserTabMenu(Dropdown):
    label = "Users"
    icon = "fas fa-bars"
    resources = []
    title = "Users"