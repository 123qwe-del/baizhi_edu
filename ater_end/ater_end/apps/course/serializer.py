from rest_framework.serializers import ModelSerializer

from course.models import CourseCategory, Course, Teacher

# 课程分类
class CourseCategoryModelserializer(ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ('name', 'id')

# 教师
class TeacherModelSerializer(ModelSerializer):
    class Meta:
        model = Teacher
        fields = ('id', 'name', 'title','signature','image')

# 课程
class CourseModelSerializer(ModelSerializer):
    teacher = TeacherModelSerializer()

    class Meta:
        model = Course
        fields = ('id', 'name', 'course_img', "students", 'lessons', 'pub_lessons',
                  'price', 'teacher', 'lessons_list',"discount_name","discount_price","active_time")

# 课程章节
class CourseDetailModelSerializer(ModelSerializer):
    teacher = TeacherModelSerializer()

    class Meta:
        model = Course
        fields = (
            'id', "students", 'lessons', 'pub_lessons', 'level', 'price', 'teacher', 'name', 'course_img',
            "Chapter_list", 'lessons_list', "brief_url","discount_name","discount_price","active_time")
