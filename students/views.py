# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse
from crm import models
# Create your views here.
from SuperCrm import settings
# from  crm.permissions import permission
import time, os, json


def stu_my_classes(request):
    return render(request, "students/my_classes.html")


def studyrecords(request, enroll_obj_id):
    enroll_obj = models.Enrollment.objects.get(id=enroll_obj_id)
    return render(request, "students/studyrecords.html", {"enroll_obj": enroll_obj})


def homework_detail(request, studyrecord_id):
    studyrecord_obj = models.StudyRecord.objects.get(id=studyrecord_id)
    homework_path = "{base_dir}/{class_id}/{course_record_id}/{studyrecord_id}/" \
        .format(base_dir=settings.HOMEWORK_DATA,
                class_id=studyrecord_obj.student.enrolled_class_id,
                course_record_id=studyrecord_obj.course_record_id,
                studyrecord_id=studyrecord_obj.id
                )
    if not os.path.isdir(homework_path):
        os.makedirs(homework_path)

    if request.method == "POST":
        print(request.FILES)
        # class_id/course_record_id/studyrecord_id
        for k, file_obj in request.FILES.items():
            with open("%s/%s" % (homework_path, file_obj.name), "wb") as f:
                for chunk in file_obj.chunks():
                    f.write(chunk)

                    # return HttpResponse(json.dumps({"status":0, "msg":"file upload success"}))

    file_lists = []
    for file_name in os.listdir(homework_path):
        f_path = "%s/%s" % (homework_path, file_name)
        modify_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(os.stat(f_path).st_mtime))
        file_lists.append([file_name, os.stat(f_path).st_size, modify_time])
    print("file lists", file_lists)

    if request.method == "POST":
        return HttpResponse(json.dumps({"status": 0,
                                        "msg": "file upload success",
                                        'file_lists': file_lists}))
    return render(request, "students/homework_detail.html",
                  {"studyrecord_obj": studyrecord_obj,
                   "file_lists": file_lists})
