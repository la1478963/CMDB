import re
from django.template import Library
from django.conf import settings
register = Library()
@register.inclusion_tag("menu.html")
def menu_html(request):
    """
    去Session中获取菜单相关信息，匹配当前URL，生成菜单
    :param request:
    :return:
    """
    # menu_list = []
    menu_list = request.session[settings.PERMISSION_MENU_KEY]
    current_url = request.path_info

    menu_dict = {}
    for item in menu_list:
        if not item['menu_gp_id']:
            menu_dict[item['id']] = item
    for item in menu_list:
        regex = "^{0}$".format(item['url'])
        if re.match(regex,current_url):
            menu_gp_id = item['menu_gp_id']
            if menu_gp_id:
                menu_dict[menu_gp_id]['active'] = True
            else:
                menu_dict[item['id']]['active'] = True
    result = {}
    for item in menu_dict.values():
        active = item.get('active')
        menu_id = item['menu_id']
        if menu_id in result:
            result[menu_id]['children'].append({ 'title': item['title'], 'url': item['url'],'active':active})
            if active:
                result[menu_id]['active'] = True
        else:
            result[menu_id] = {
                'menu_id':item['menu_id'],
                'menu_title':item['menu_title'],
                'active':active,
                'children':[
                    { 'title': item['title'], 'url': item['url'],'active':active}
                ]
            }

    return {'menu_dict':result}
