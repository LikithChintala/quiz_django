from django.db.models import Max, Min, Avg, Func
from django.http import HttpResponseRedirect, request
from django.shortcuts import get_object_or_404,render, redirect
from django.views import generic
from .forms import SignUpForm
from .models import Question, Scores
from django.urls import reverse_lazy
from django.contrib.auth import logout


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')


def HomeView(request):
    return render(request, 'quiz_app/home.html')

class IndexView(generic.ListView):
    template_name = 'quiz_app/index.html'
    context_object_name = 'random_question_list'

    def get_queryset(self):
        """Return random five published questions."""
        return Question.objects.order_by('?')[:5]


class Round(Func):
    function = 'ROUND'
    template = '%(function)s(%(expressions)s, 2)'


class ResultsView(generic.ListView):
    model = Scores
    template_name = 'quiz_app/results.html'
    context_object_name = 'scores_results'

    def get_queryset(self):
        """Return scores of specific user."""
        return Scores.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        scores_list = data.get('scores_results')
        data['show_try_again_link'] = False
        if len(scores_list) > 0:
            data['current_score'] = scores_list[len(scores_list) - 1].value
            data['percent'] = (data['current_score'] / 5) * 100
            if data['current_score'] <= 2:
                data['message'] = 'Please try again!'
                data['show_try_again_link'] = True
            elif data['current_score'] == 3:
                data['message'] = 'Good job!'
            elif data['current_score'] == 4:
                data['message'] = 'Excellent work!'
            else:
                data['message'] = 'You are a genius!'
        data['aggregate'] = scores_list.aggregate(Avg('value'), Max('value'), Min('value'))
        data['avg'] = round(data['aggregate']['value__avg'], 2)
        return data


def add_score(request):
    if request.method == 'POST':
        score = 0
        count = 0
        for question in request.POST.keys():
            if question.startswith('q-'):
                question_id = question.split('-')[1]
                question_object = get_object_or_404(Question, pk=question_id)
                if question_object.answer_set.get().answer_choice_id == int(request.POST.get(question)):
                    score += 1
                count += 1
        scores = Scores.objects.create(user_id=request.user.id, value=score)
        scores.value = score
        scores.save()
        return redirect('/results/')
    else:
        return render(request, 'quiz_app/index.html')
