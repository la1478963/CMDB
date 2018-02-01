from django.shortcuts import render,HttpResponse
from client.bin.run import JG_info
from db import models
from django.views.decorators.csrf import csrf_exempt,csrf_protect
import requests
import json
from django.db import transaction

#给CMDB的api,提供给 salt 入库
@csrf_exempt
def ret_salt_api(req,):
    ret_str=req.body.decode()
    ret_data_dic=json.loads(ret_str)
    for host,value in ret_data_dic.items():
        if 'cpu' not in value.keys():
            print('error',host,value)
            continue
        cpu_obj=models.Cpu.objects.filter(
            cpuarch=value['cpu']['cpuarch'],
            num_cpus=value['cpu']['num_cpus'],
            cpu_model=value['cpu']['cpu_model'],
        ).first()
        if not cpu_obj:
            cpu_obj = models.Cpu.objects.create(
                cpuarch=value['cpu']['cpuarch'],
                num_cpus=value['cpu']['num_cpus'],
                cpu_model=value['cpu']['cpu_model'],
            )
        motherboard_obj=models.Motherboard.objects.filter(
            sn=value['motherboard']['Serial Number'],
            manufacturer=value['motherboard']['Manufacturer'],
            pn=value['motherboard']['Product Name']
        ).first()
        if not motherboard_obj:
            motherboard_obj = models.Motherboard.objects.create(
                sn=value['motherboard']['Serial Number'],
                manufacturer=value['motherboard']['Manufacturer'],
                pn=value['motherboard']['Product Name']
            )


        mem_obj=models.Memory.objects.filter(
            size=value['mem']['Size'],
            width=value['mem']['Data Width'],
            locator=value['mem']['Locator'],
            type=value['mem']['Type'],
        ).first()
        if not mem_obj:
            mem_obj = models.Memory.objects.create(
                size=value['mem']['Size'],
                width=value['mem']['Data Width'],
                locator=value['mem']['Locator'],
                type=value['mem']['Type'],
            )

        eth1_obj=models.Network.objects.filter(
            ip_address=value['network']['eth1'][0],
            mac_address=value['network']['eth1'][1],
        ).first()
        if not eth1_obj:
            eth1_obj = models.Network.objects.create(
                ip_address=value['network']['eth1'][0],
                mac_address=value['network']['eth1'][1],
            )

        eth0_obj=models.Network.objects.filter(
            ip_address=value['network']['eth0'][0],
            mac_address=value['network']['eth0'][1],
        ).first()
        if not eth0_obj:
            eth0_obj = models.Network.objects.create(
                ip_address=value['network']['eth0'][0],
                mac_address=value['network']['eth0'][1],
            )
        os_obj=models.Os.objects.filter(name=value['other']['os']).first()
        if not os_obj:
            os_obj = models.Os.objects.create(name=value['other']['os'])
        osarch_obj=models.Osarch.objects.filter(sarch=value['other']['osarch'],).first()
        if not osarch_obj:
            osarch_obj = models.Osarch.objects.create(sarch=value['other']['osarch'])

        disk_obj_li=[]
        for item in value['disk'].keys():
            disk_obj=models.Disk.objects.filter(path=item,size=value['disk'][item]).first()
            if not disk_obj:
                disk_obj = models.Disk.objects.create(path=item,size=value['disk'][item])
            disk_obj_li.append(disk_obj)

        obj = models.Host.objects.filter(hostname=host)
        if obj.first():
            with transaction.atomic():
                obj.update(
                    hostname=host,
                    login_port=value['port'],
                    cpu=cpu_obj,
                    motherboard=motherboard_obj,
                    mem=mem_obj,
                    eth1_network=eth1_obj,
                    eth0_network=eth0_obj,
                    uuid=value['other']['uuid'],
                    os=os_obj,
                    osarch=osarch_obj,
                    kernel=value['other']['kernel'],
                )
                obj.first().disk.remove()
                obj.first().disk.add(*disk_obj_li)
        else:
            with transaction.atomic():
                obj=models.Host.objects.create(
                    hostname=host,
                    login_port=value['port'],
                    cpu=cpu_obj,
                    motherboard=motherboard_obj,
                    mem=mem_obj,
                    eth1_network=eth1_obj,
                    eth0_network=eth0_obj,
                    uuid=value['other']['uuid'],
                    os=os_obj,
                    osarch=osarch_obj,
                    kernel=value['other']['kernel'],
                )
                obj.disk.add(*disk_obj_li)
    return HttpResponse('ok')


#调用salt_api执行
@csrf_exempt
def client_func(req,):
    #执行开始
    JG_func=JG_info._begin()
    if JG_func =='ok':
        return HttpResponse('更新成功')
    else:
        return HttpResponse('更新失败')