from django import template
from ..models import *
from django.utils.safestring import mark_safe
from calendar import monthrange, month_name

register = template.Library()


def cellId(day, month, year, apart):
    if day == -1:
        return f"{apart}LastCell"
    else:
        return f'{day}_{month}_{year}_{apart}'


@register.simple_tag()
def tabulka(args):
    month = int(args['month'])
    year = int(args['year'])

    print("DEBUG PRINTS\n" + "-" * 30)

    properties = sorted(list(map(str, Properties.objects.all())))
    bookings = Bookings.objects.all()
    days_in_this_month = list(range(monthrange(year, month)[1] + 1))
    tab_head = [['<div class="monthHeadCell">' + month_name[month] + " " + str(year) + '</div>'] + [
        '<div class="apartHeadCell">' + str(apart) + '</div>' for apart in properties]]
    tabulka = tab_head + [['<div class="dayColumnCell">' + str(day) + '</div>'] + [
        f'<div class="cell" id="{cellId(day, month, year, apart)}"></div>' for apart in range(len(properties))] for day
                          in days_in_this_month[1:]]
    # добавим последней строчкой первое число следующего месяца
    tabulka += [
        ['<div class="dayColumnCell">1</div>'] + [f'<div class="cell" id="{cellId(-1, month, year, apart)}"></div>' for
                                                  apart in range(len(properties))]]
    days_in_this_month += [1]  # также добавим последним днём месяца 1(первый день след. месяца)

    for b in bookings:

        if b.arrival.month == month and b.arrival.year == year:  # если в этом месяце заезд

            guests = str(b.adults)
            if b.children: guests += f'+{b.children}'
            if b.pets: guests += f' + {b.pets} pets'
            if b.infants: guests += f' + {b.infants} младенцев'

            if b.departure.toordinal() - b.arrival.toordinal() == 1:  # one-night condition
                tabulka[b.arrival.day][properties.index(
                    str(b.property)) + 1] = f'<div class="cell one_night_cell" id="{cellId(b.arrival.day, month, year, properties.index(str(b.property)))}">' + b.first_name + " " + b.last_name + " (" + guests + ')</div>'

            else:
                tabulka[b.arrival.day][properties.index(
                    str(b.property)) + 1] = f'<div class="cell arrive_depart_cell" id="{cellId(b.arrival.day, month, year, properties.index(str(b.property)))}">' + b.first_name + " " + b.last_name + '</div>'

                tabulka[b.arrival.day + 1][properties.index(
                    str(b.property)) + 1] = f'<div class="cell live_cell" id="{cellId(b.arrival.day + 1, month, year, properties.index(str(b.property)))}">' + guests + '</div>'

            # В цикле закрасим не закрашенные дни, если есть хотя бы один такой, не считая дня выезда
            # если ячейка пуста, только тогда отметим там выезд(иначе можем перекрыть другую бронь)
            # а также если выезд не в следующем месяце
            # + здесь же закрасим всё не закрашенное между заездом и выездом, если есть хотя бы один такой день
            if (b.departure.month == month or (b.departure.day == 1 and ((b.departure.month - 1) == month) or ((
                    month == 12 and b.departure.month == 1))) and b.departure.year - year <= 1):

                # введём понятия индекса дня выезда, потому что в матрице есть два "первых" числа месяца
                if b.departure.day == 1 and b.departure.month == month + 1:
                    depart_i = -1
                else:
                    depart_i = b.departure.day

                if b.departure.toordinal() - b.arrival.toordinal() > 2:
                    for i in days_in_this_month[b.arrival.day + 2:depart_i]:
                        tabulka[i][properties.index(
                            str(b.property)) + 1] = f'<div class="cell live_cell" id="{cellId(i, month, year, properties.index(str(b.property)))}"></div>'

                if tabulka[depart_i][properties.index(
                        str(b.property)) + 1] == f'<div class="cell" id="{cellId(depart_i, month, year, properties.index(str(b.property)))}"></div>':
                    tabulka[depart_i][
                        properties.index(
                            str(b.property)) + 1] = f'<div class="cell arrive_depart_cell" id="{cellId(depart_i, month, year, properties.index(str(b.property)))}"></div>'

            # если выезд не в этом месяце и не первого числа следующего месяца, тупо закрасим оранжевым всё до конца
            else:
                for i in days_in_this_month[b.arrival.day + 2:-1]:
                    tabulka[i][properties.index(
                        str(b.property)) + 1] = f'<div class="cell live_cell" id="{cellId(i, month, year, properties.index(str(b.property)))}"></div>'
                tabulka[-1][properties.index(
                    str(b.property)) + 1] = f'<div class="cell live_cell" id="{cellId(-1, month, year, properties.index(str(b.property)))}"></div>'

        elif b.departure.month == month and b.departure.year == year:  # иначе если не заезд, а только выезд

            # введём понятия индекса дня выезда, потому что в матрице есть два "первых" числа месяца
            if b.departure.day == 1 and b.departure.month == month + 1:
                depart_i = -1
            else:
                depart_i = b.departure.day

            # если ячейка пуста, только тогда отметим там выезд(иначе можем перекрыть другую бронь)
            if tabulka[depart_i][properties.index(
                    str(b.property)) + 1] == f'<div class="cell" id="{cellId(depart_i, month, year, properties.index(str(b.property)))}"></div>':
                tabulka[depart_i][
                    properties.index(
                        str(b.property)) + 1] = f'<div class="cell arrive_depart_cell" id="{cellId(depart_i, month, year, properties.index(str(b.property)))}"></div>'

            for row in range(1, depart_i):
                tabulka[row][properties.index(
                    str(b.property)) + 1] = f'<div class="cell live_cell" id="{cellId(row, month, year, properties.index(str(b.property)))}"></div>'

        elif (
                ((b.arrival.month < month and b.arrival.year == year) or (b.arrival.year < year))
                    and ((b.departure.year == year and b.departure.month > month) or (b.departure.year > year))
        ): #если заезд был раньше, но и выезд не в этом месяце


            for row in days_in_this_month[1:-1]:

                tabulka[row][properties.index(
                    str(b.property)) + 1] = f'<div class="cell live_cell" id="{cellId(row, month, year, properties.index(str(b.property)))}"></div>'

            row=-1
            if b.departure.day == 1 and ((b.departure.month - 1) == month or (month == 12 and b.departure.month == 1)):  # если выезд 1-го числа след. месяца

                if tabulka[row][properties.index(
                        str(b.property)) + 1] == f'<div class="cell" id="{cellId(row, month, year, properties.index(str(b.property)))}"></div>':
                    tabulka[row][
                        properties.index(
                            str(b.property)) + 1] = f'<div class="cell arrive_depart_cell" id="{cellId(row, month, year, properties.index(str(b.property)))}"></div>'

            else:
                tabulka[row][properties.index(
                    str(b.property)) + 1] = f'<div class="cell live_cell" id="{cellId(row, month, year, properties.index(str(b.property)))}"></div>'



    htmltab = '<div id="tabulkaDiv"><div class="tabulkaTable" border="1">'
    htmltab += '<div class="headRow">'
    for cell in tabulka[0]:
        htmltab += cell
    htmltab += '</div>'
    for row in tabulka[1:]:
        htmltab += '<div class="row">'
        for cell in row:
            htmltab += cell
        htmltab += '</div>'
    htmltab += '</div></div>'

    max_m_before = args['configs']['max_months_before_current'].config_value
    max_m_after = args['configs']['max_months_after_current'].config_value
    current_year = args['current_year']
    current_month = args['current_month']
    months = list(range(1, 13))
    buttons_code = ''

    for i in range(1, max_m_before + 1)[::-1]:
        cyear = current_year
        cmonth = months[current_month - i - 1]
        css_class = 'btn'
        if current_month - i < 1:
            cyear = current_year - 1
        if cyear == year and cmonth == month:
            css_class = 'disabledbtn'
        buttons_code += f'<a href="/create?m={cmonth}&y={cyear}" class="{css_class}">{month_name[months[current_month - i - 1]]}{cyear}</a>'

    css_class = 'btn'
    if current_month == month and current_year == year:
        css_class = "disabledbtn"
    buttons_code += f'<a href="/create?m={current_month}&y={current_year}" class="{css_class}">{month_name[current_month]}{current_year}</a>'

    for i in range(1, max_m_after + 1):
        css_class = 'btn'
        cyear = current_year
        cmonth = current_month + i

        if current_month + i > 12:
            cmonth = current_month + i - 12
            cyear += 1

        if cyear == year and cmonth == month:
            css_class = "disabledbtn"

        buttons_code += f'<a href="/create?m={cmonth}&y={cyear}" class="{css_class}">{month_name[cmonth]}{cyear}</a>'

    print("-" * 30)  # debug messages end

    html_code = buttons_code + htmltab
    return mark_safe(html_code)
