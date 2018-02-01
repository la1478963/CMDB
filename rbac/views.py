from django.shortcuts import render,HttpResponse,redirect
from utlis.form_class import LoginForm
from db import models
from django.conf import settings
from utlis import check_code
from io import BytesIO
from rbac.service.init_permission import init_permission
import json
import requests
from utlis.salt_api import SaltApi
from django.views.decorators.csrf import csrf_exempt,csrf_protect
import jieba
import json
from gensim.models.word2vec import Word2Vec
from keras.models import load_model
from keras.preprocessing import sequence
import numpy as np
import xlrd
import xlwt
from keras import backend as K
import os
import importlib
import re
from gensim.models.word2vec import Word2Vec
from keras.models import load_model
from keras.preprocessing import sequence
import numpy as np
import xlrd
import xlwt
from keras import backend as K
from string import punctuation
import importlib
import h5py
from jieba import analyse


class SuanFa(object):
    def __init__(self):
        os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
        os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
        os.environ['KERAS_BACKEND'] = 'tensorflow'
        jieba.set_dictionary("dict.txt")
        jieba.initialize()
        jieba.load_userdict('digital_dict.txt')
        self.MAX_SENTENCE_LENGTH = 40
        self.MODELPATH1 = 'liangxiang_w2v_model.save'  # word2index lookup model
        self.MODELPATH2 = 'model_v0.314_epoch-07-loss0.0742-valLoss0.1214.hdf5'
        self.VALIPATH = './'
        self.THRESOLD = 0.4
        self.model = load_model(self.MODELPATH2)
        # self.model = request.session.get('model')
        self.wordEmbeddingModelPath = self.MODELPATH1
        self.word2vecModel = Word2Vec.load(self.wordEmbeddingModelPath)  # 载入保存的文件
        self.word2v = dict([(k, v.index) for k, v in self.word2vecModel.wv.vocab.items()])  # 获得词库
        self.biaodian = r'[,，。.!！？?;；]'

    def main(self,line: str):
        sentences = re.split(self.biaodian, line.strip())
        y_pred = self.evaluate(sentences, self.model, self.word2v)
        result = self.writeExcel(sentences, y_pred, self.THRESOLD)
        sm = len(result)
        fm = 0.0
        for ss in result:
            if str(ss).__eq__('负面'):
                fm += 1.0
        fuResu = "%.2f" % (fm / sm * 100)
        zhengResu = "%.2f" % (100 - (fm / sm) * 100)
        return {'neg': fuResu, 'pos': zhengResu}

    def to_ids1(self,vocab, words):
        '''基于w2v，将短语转化为向量'''
        punctuations = set(punctuation + "！？，。【】；’'、·")
        out = []
        for word in words:
            if word in punctuations:
                continue
            id = vocab.get(word)
            if id is None:
                id = 0
            out.append(id)
        return np.array(out)

    def evaluate(self,testTitle, model, word2index):
        num_recs = len(testTitle)

        XTEST = np.empty(num_recs, dtype=list)
        YTEST = np.zeros(num_recs)
        for index, onetitle in enumerate(testTitle):
            cutTitle = jieba.cut(onetitle, cut_all=False, HMM=False)
            XTEST[index] = self.to_ids1(word2index, cutTitle)
        XTEST = sequence.pad_sequences(XTEST, maxlen=self.MAX_SENTENCE_LENGTH)
        return model.predict(XTEST)

    def writeExcel(self,title_data, y_pred, thresold):
        assert y_pred.size == len(title_data)
        predLabels = []
        y_predHat = [1 if i[0] > thresold else 0 for i in y_pred]

        for ele in y_predHat:
            if ele == 1:
                predLabels.append('负面')
            else:
                predLabels.append('非负面')
        return predLabels





class Init(object):
    def home(self,request):
        return render(request,'home.html',{'req':request})

    @csrf_exempt
    def FC(self,request):
        import jieba
        line=request.POST.get('txt')
        result = list(jieba.cut(line.strip()))
        data = {'result': result, 'code': 200}
        return HttpResponse(json.dumps(data))

    @csrf_exempt
    def GJCCQ(self,request):
        line = request.POST.get('txt')
        number=int(request.POST.get('num'))
        if not number:
            number=20
        tfidf = analyse.extract_tags
        keywords = tfidf(line, number)
        res_dic={'result':{'keywords': keywords},'code':200}
        return HttpResponse (json.dumps(res_dic))


    @csrf_exempt
    def QGFX(self,request):
        line = request.POST.get('txt')
        sf=SuanFa()
        JG_dic=sf.main(line)
        return HttpResponse(json.dumps({'result':JG_dic,'code':200}))


    @csrf_exempt
    def CXBZ(self,request):
        import jieba.posseg as pseg
        import json
        '''词性标注+分词'''
        line = request.POST.get('txt')
        spe = {'eng', 'xx', 'xu'}
        spe2 = {'g', 'i', 'j', 'l'}
        a = []
        b = []
        t = type(line)
        if t is str:
            resu = pseg.cut(line)
            for ws in resu:
                a.append(ws.word)
                ss = ws.flag
                if ss not in spe:
                    ss = ss[0:1]
                if ss in spe2:
                    ss = '#'
                b.append(ss)
        result_dic = {'seg': a, 'speech': b}
        result={'result':result_dic,'code':200}
        return HttpResponse(json.dumps(result))



    def v48_update(self,request):
        salt = SaltApi("https://101.201.141.232:8001/")
        dic={'client': 'local', 'fun': 'cmd.run', 'tgt': 'hm_sd_v48web','arg':'sh /home/www/update_v48.sh'}
        result1 = salt.salt_command(dic)
        return HttpResponse('v48测试环境 代码已经更新')


    def login(self,request):
        if request.method=='GET':
            form=LoginForm()
            return render(request,'login.html',locals())
        else:
            tag = {'msg': True, 'data': None, 'status': True}
            form = LoginForm(data=request.POST)
            if form.is_valid():
                code = request.POST.get('code').upper()
                if request.session[settings.CODEIMG].upper() != code:
                    tag['status'] = False
                    tag['data'] = '验证码错误'
                else:
                    obj = models.UserInfo.objects.filter(**form.cleaned_data).first()
                    if not obj:
                        tag['status'] = False
                        tag['data'] = '用户名密码错误'
                    else:
                        init_permission(obj.auth, request)
            else:
                tag['msg']=False
                tag['data']=form.errors
            return HttpResponse(json.dumps(tag))


    def logout(self,request):
        request.session.clear()
        return redirect('/arya/login/')




def Code(request):
    img_obj, code = check_code.create_validate_code()
    stream = BytesIO()
    img_obj.save(stream, 'png')
    request.session[settings.CODEIMG] = code
    return HttpResponse(stream.getvalue())

init=Init()


