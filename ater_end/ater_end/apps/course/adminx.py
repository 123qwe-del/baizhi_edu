import xadmin

from course import models
from course.models import CourseCategory, Course, Teacher, CourseChapter, CourseLesson


# """课程分类表"""
class CourseCategoryAdmin(object):
    """课程分类表"""
    pass


xadmin.site.register(CourseCategory, CourseCategoryAdmin)


# """课程信息表"""
class CourseAdmin(object):
    """课程信息表"""
    pass


xadmin.site.register(Course, CourseAdmin)


# """讲师表"""
class TeacherAdmin(object):
    """讲师表"""
    pass


xadmin.site.register(Teacher, TeacherAdmin)


# """章节表"""
class CourseChapterAdmin(object):
    """章节表"""
    pass


xadmin.site.register(CourseChapter, CourseChapterAdmin)


# """课时表"""
class CourseLessonAdmin(object):
    pass


xadmin.site.register(CourseLesson, CourseLessonAdmin)


# ********************************************************************************
# 购物车相关
class CourseDiscountAdmin(object):
    """课程折扣模型"""
    pass


xadmin.site.register(models.CourseDiscount)


class CourseDiscountTypeAdmin(object):
    """课程优惠类型模型"""
    pass


xadmin.site.register(models.CourseDiscountType, CourseDiscountTypeAdmin)


class ActivityAdmin(object):
    """课程优惠时间表"""
    pass


xadmin.site.register(models.Activity, ActivityAdmin)


class CoursePriceDiscountAdmin(object):
    """课程与价格策略关系表"""
    pass


xadmin.site.register(models.CoursePriceDiscount, CoursePriceDiscountAdmin)


class CourseExpireAdmin(object):
    """课程与价格策略关系表"""
    pass


xadmin.site.register(models.CourseExpire, CourseExpireAdmin)
