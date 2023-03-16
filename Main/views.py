from datetime import date, datetime, timedelta
from calendar import monthrange

from rest_framework.generics import RetrieveAPIView, GenericAPIView, CreateAPIView
from rest_framework.response import Response
from Main.models import Car, Session
from Main.serializers import SessionSerializer
from Main.utils import validate_date
from Main.consts import *


class CheckAvailableCar(RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        if not Session.objects.filter(car=kwargs['pk']).exists():
            return Response((Car.objects.get(id=kwargs['pk'])).is_available)
        current_month_sessions = Session.objects.filter(car=kwargs['pk']).filter(
            session_finish__month__gte=date.today().month + 1).filter(session_start__month__gte=date.today().month - 1)
        if current_month_sessions.exists():
            if current_month_sessions.first().session_start > date.today() or date.today() > current_month_sessions.first().session_finish:
                Car.objects.filter(id=kwargs['pk']).update(is_available=True)
        return Response((Car.objects.get(id=kwargs['pk'])).is_available)


class CalculatePrice(GenericAPIView):
    def post(self, request):
        session_start = datetime.strptime(request.data['session_start'], '%Y-%m-%d').date()
        session_finish = datetime.strptime(request.data['session_finish'], '%Y-%m-%d').date()
        if validate_date(session_start, session_finish)[0]:
            count_days = (session_finish - session_start).days
            total_price = 0
            for day in range(count_days):
                if day < 4:
                    total_price += 1000
                elif day < 9:
                    total_price += 1000 * 0.95
                elif day < 17:
                    total_price += 1000 * 0.90
                else:
                    total_price += 1000 * 0.85
            return Response(int(total_price))
        return Response(validate_date(session_start, session_finish)[1])


class CreateSession(CreateAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer

    def post(self, request, *args, **kwargs):
        car = request.data['car']
        session_start = datetime.strptime(request.data['session_start'], '%Y-%m-%d').date()
        session_finish = datetime.strptime(request.data['session_finish'], '%Y-%m-%d').date()
        if not Car.objects.get(id=car).is_available:
            return Response(not_available)
        if Session.objects.filter(car=car).exists():
            if Session.objects.filter(car=car) \
                    .filter(session_finish__month__gte=session_start.month) \
                    .filter(session_finish__month__lte=session_start.month + 1) \
                    .order_by('session_finish').first() \
                    .session_finish > (session_start - timedelta(days=3)):
                return Response('3 days are not over yet')
        if validate_date(session_start, session_finish)[0]:
            Car.objects.filter(id=car).update(is_available=False)
            return self.create(request, *args, **kwargs)
        return Response(validate_date(session_start, session_finish)[1])


class Statistic(GenericAPIView):
    def get(self, request, *args, **kwargs):
        car_reports = {}
        car_reports_together = []
        sessions_current_month = Session.objects \
            .filter(session_start__month__gte=date.today().month - 1) \
            .filter(session_start__month__lte=date.today().month) \
            .filter(session_start__year__gte=date.today().year - 1) \
            .filter(session_start__year__lte=date.today().year)
        days_in_current_month = monthrange(date.today().year, date.today().month)[1]
        for car in Car.objects.all():
            days_in_rent = 0
            for session in sessions_current_month.filter(car=car):
                finish = session.session_finish
                start = session.session_start
                if finish.month < date.today().month:
                    continue
                if finish.month > date.today().month:
                    finish = date(date.today().year, date.today().month, days_in_current_month)
                if start.month != date.today().month:
                    start = date(date.today().year, date.today().month, 1)
                days_in_rent += (finish - start).days + 1

            rented_day_percent = days_in_rent * 100 // days_in_current_month
            car_reports[f'Car id:{car.id}'] = f'Days in rent {rented_day_percent}%'
            car_reports_together.append(rented_day_percent)
        data = {
            'report for evey car': car_reports,
            'report for all cars together': f'{sum(car_reports_together) // len(car_reports_together)}%'
        }
        return Response(data)
