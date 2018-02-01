from django.conf import settings


def init_permission(user,request):
    """
    初始化权限信息，获取权限信息并放置到session中。
    :param user: Rbac
    :param request:
    :return:
    """
    permission_list = user.roles.filter(permissions__id__isnull=False).values('permissions__id',
                                        'permissions__title',              # 用户列表
                                        'permissions__url',
                                        'permissions__code',
                                        'permissions__menu_gp_id',         # 组内菜单ID，Null表示是菜单
                                        'permissions__group_id',            # 权限的组ID
                                        'permissions__group__menu_id',     # 权限的组的菜单ID
                                        'permissions__group__menu__title', # 权限的组的菜单名称
                                        ).distinct()

    # 菜单相关（以后再匹配）,inclusion_tag
    menu_permission_list = []
    for item in permission_list:
        tpl = {
            'id':item['permissions__id'],
            'title':item['permissions__title'],
            'url':item['permissions__url'],
            'menu_gp_id':item['permissions__menu_gp_id'],
            'menu_id':item['permissions__group__menu_id'],
            'menu_title':item['permissions__group__menu__title'],
        }
        menu_permission_list.append(tpl)
    request.session[settings.PERMISSION_MENU_KEY] = menu_permission_list

    # 权限相关，中间件
    """
    {
        1:{
            codes: [list,add,edit,del],
            urls: [  /userinfo/,  /userinfo/add/,  /userinfo/... ]
        },
        2:{
            codes: [list,add,edit,del],
            urls: [  /userinfo/,  /userinfo/add/,  /userinfo/... ]
        }
        3:{
            codes: [list,add,edit,del],
            urls: [  /userinfo/,  /userinfo/add/,  /userinfo/... ]
        }
    }

    """
    result = {}
    for item in  permission_list:
        group_id = item['permissions__group_id']
        code = item['permissions__code']
        url = item['permissions__url']
        if group_id in result:
            result[group_id]['codes'].append(code)
            result[group_id]['urls'].append(url)
        else:
            result[group_id] = {
                'codes':[code,],
                'urls':[url,]
            }
    request.session[settings.PERMISSION_URL_DICT_KEY] = result