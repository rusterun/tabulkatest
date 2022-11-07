from django.shortcuts import render, redirect
from .models import Bookings, Comments, Properties, Configs
from .forms import BookingsForm
from django.views.generic import ListView
import calendar, datetime
from django.contrib.auth.decorators import user_passes_test


def index(request):
    bookings = Bookings.objects.order_by('arrival')
    return render(request, 'main/index.html', {'title': 'Главная',
                                               'bookings': bookings})


class BookingsPage(ListView):
    model = Bookings
    template_name = 'main/second.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(BookingsPage, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the Baklawa
        context['comments'] = Comments.objects.all()
        context['properties'] = Properties.objects.all()
        context['mrange'] = list(range(1, calendar.monthrange(2022, 8)[1] + 1))

        return context


# def second(request):
#     bookings = Bookings.objects.order_by('-booking_info')
#     today = datetime.today().date()
#     monthranges = {a: monthrange(today.year, a)[1] for a in range(1,13)}
#     sixty=list(range(60))
#     return render(request, 'main/second.html', {'title': 'Главная',
#                                                'bookings': bookings,
#                                                 'monthranges': monthranges,
#                                                 'sixty': sixty})


def create(request):
    error = ''
    if request.method == 'POST':
        form = BookingsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            error = 'Формочка некорректна'

    form = BookingsForm
    context = {
        'form': form,
        'error': error
    }

    configs = dict()

    configs['max_months_after_current'] = Configs.objects.get(config_name='max_months_after_current')
    configs['max_months_before_current'] = Configs.objects.get(config_name='max_months_before_current')

    arguments = dict()

    arguments['month'] = request.GET.get('m', datetime.datetime.today().month)
    arguments['year'] = request.GET.get('y', datetime.datetime.today().year)
    arguments['current_year'] = datetime.datetime.today().year
    arguments['current_month'] = datetime.datetime.today().month
    arguments['configs'] = configs

    context['arguments'] = arguments
    return render(request, 'main/create.html', context)

@user_passes_test(lambda u: u.is_superuser)
def manage(request):
    return render(request, 'main/manage.html', {})