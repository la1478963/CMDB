#!/usr/bin/python
# -*- coding:utf-8 -*-
#make in LA

class Page(object):
    def __init__(self,pag,data_num,url,par_age=10,display_page_count=11):
        '''
        分页功能
        :param pag: 当前页
        :param url:要跳转的url
        :param data_num:  所有数据量
        :param par_age:  每页数据量
        :param display_page_count:  页码数量
        '''
        self.pag=pag
        self.url=url
        self.data_num=data_num
        self.par_age=par_age
        self.display_page_count=display_page_count
        page_count, b = divmod(self.data_num, self.par_age)
        if b != 0:
            page_count += 1
        self.page_count=page_count
    @property
    def start(self):
        return (self.pag-1)*self.par_age
    @property
    def end(self):
        return self.pag*self.par_age

    def ret_page_str(self):
        # print(self.page_count)
        if self.pag > self.page_count:
            self.pag = self.page_count
        page_list = []
        # self.display_page_count = 11
        half_display_page_count = int(self.display_page_count / 2)

        if self.pag <= 1:
            up_page = '<li><a href="#" class="disabled">上一页</a></li>'
        else:
            up_page = '<li><a href="%s/?page=%s">上一页</a></li>' % (self.url,self.pag - 1,)
        page_list.append(up_page)

        if self.pag <= half_display_page_count:
            display_page_start = 1
            display_page_end = self.display_page_count + 1
        elif self.pag >= self.page_count - half_display_page_count:
            display_page_start = self.page_count - self.display_page_count
            display_page_end = self.page_count+1
        else:
            display_page_start = self.pag - half_display_page_count
            display_page_end = self.pag + half_display_page_count + 1
        for i in range(display_page_start, display_page_end):
            tpl = ' <li><a href="%s/?page=%s">%s</a></li>' % (self.url,i, i)
            page_list.append(tpl)

        if self.pag >= self.page_count:
            down_page = '<li><a href="#" class="disabled">下一页</a></li>'
        else:
            down_page = '<li><a href="%s/?page=%s">下一页</a></li>' % (self.url,self.pag + 1,)
        page_list.append(down_page)
        page_str = "".join(page_list)

        return page_str