from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage
from django.http import HttpRequest
from django.http import HttpResponseBadRequest
# Create your views here.

QUESTIONS = [
    {
        "title": f"Question {i}",
        "text": f"HELP HELP HElP",
    } for i in range(100)
]

class InvalidPageNumber(ValueError):
    pass


class EmptyPageException(Exception):
    pass


def get_page_number(request):
    number = request.GET.get('page', 1)
    try:
        number = int(number)
        if number <= 0:
            raise InvalidPageNumber("Page number must be greater than 0")
    except ValueError:
        raise InvalidPageNumber("Invalid page number")

    return number


# def get_question_id(request):
#     number = request.GET.get('page', 1)
#     try:
#         number = int(number)
#         if number <= 0:
#             raise InvalidPageNumber("Page number must be greater than 0")
#     except ValueError:
#         raise InvalidPageNumber("Invalid page number")
#
#     return number

def paginate(objects, page, per_page=3):
    paginator = Paginator(objects, per_page)
    try:
        page_data = paginator.page(page)
        return page_data
    except EmptyPage:
        raise EmptyPageException("Page doesn't exist")


def get_visible_pages(objects, page, per_page=3):
    paginator = Paginator(objects, per_page)
    paginator_len = 5
    page_numbers = list()

    first_page = page - 2 if page - 2 >= 1 else 1
    for i in range(paginator_len):
        try:
            paginator.page(first_page + i)
            page_numbers.append(first_page + i)
        except EmptyPage:
            break
    return page_numbers


def last_page(objects, page, per_page=3) -> bool:
    paginator = Paginator(objects, per_page)
    try:
        paginator.page(page + 1)
    except EmptyPage:
        return True
    return False


def index(request):
    try:
        pageNumber = get_page_number(request)
        questions = paginate(QUESTIONS, pageNumber)
    except InvalidPageNumber as e:
        return HttpResponseBadRequest(f"Invalid page number: {str(e)}")
    except EmptyPageException as e:
        return HttpResponseBadRequest(f"Empty page: {str(e)}")

    paginate_pages = get_visible_pages(QUESTIONS, pageNumber)

    return render(request, 'index.html',
                  {'questions': questions, 'visible_pages': paginate_pages, 'current_page': pageNumber,
                   'last_page': last_page(QUESTIONS, pageNumber)})


def register(request):
    return render(request, 'register.html')


def login(request):
    return render(request, 'login.html')


def settings(request):
    return render(request, 'settings.html')


def tag(request):
    return render(request, 'tag.html', {"questions": QUESTIONS})


def answer(request, id):
    return render(request, 'question.html', {"question": QUESTIONS[id], "answers": QUESTIONS})


def ask(request):
    return render(request, 'ask.html')
