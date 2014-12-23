"""
Implementation of the RESTful endpoints for the Course About API.

"""
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from course_about import api
from rest_framework import status
from rest_framework.response import Response
from errors import CourseNotFoundError


class CourseAboutThrottle(UserRateThrottle):
    """Limit the number of requests users can make to the Course About API."""
    # TODO Limit based on expected throughput  # pylint: disable=fixme
    rate = '50/second'


class CourseAboutView(APIView):
    """ RESTful Course About API view.

    Used to retrieve JSON serialized Course About information.

    """
    authentication_classes = []
    permission_classes = []
    throttle_classes = CourseAboutThrottle,

    def get(self, request, course_id=None):  # pylint: disable=unused-argument
        """read course information.

        HTTP Endpoint for course info api.

        Args:
            Course Id = URI element specifying the course location. Course information will be
                returned for this particular course.

        Return:
            A JSON serialized representation of the course information

        """
        try:
            return Response(api.get_course_about_details(request, course_id))
        except CourseNotFoundError:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "message": (
                        u"An error occurred while retrieving course information"
                        u" for course '{course_id}'"
                    ).format(course_id=course_id)
                }
            )