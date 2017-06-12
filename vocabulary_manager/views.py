from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from .models import *
from .forms import *
import datetime
import random


@login_required
def index(request):
    review = get_words(request.user, size=True)
    query = request.GET.get('q', '')
    if query:
        qset = (
            Q(word__icontains=query),
        )
        results = VocabularyWord.objects.filter(qset).distinct().filter(user=request.user)

    else:
        results = VocabularyWord.objects.filter(user=request.user).order_by('word')

    page = request.GET.get('page', 1)
    paginator = Paginator(results, 100)

    try:
        words = paginator.page(page)
    except PageNotAnInteger:
        words = paginator.page(1)
    except EmptyPage:
        words = paginator.page(paginator.num_pages)

    index_ = words.number - 1
    max_index = len(paginator.page_range)
    start_index = index_ - 3 if index_ >=3 else 0
    end_index = index_ + 4 if index_ <= max_index - 4 else max_index
    page_range = paginator.page_range[start_index:end_index]

    context = {
        'words': words,
        'page_range': page_range,
        'last': max_index,
        'today': datetime.date.today(),
        'quantity': review,
    }
    return render(request, 'vocabulary_manager/index.html', context)


def get_words(user, num=10, size=False):
    words = VocabularyWord.objects.filter(user=user)
    # sorted_words = sorted(words, key=lambda p: p.next_time())
    # for x in words:
    #     print(x.next_time())
    # print(datetime.date.today())
    words = [x for x in words if x.next_time().date() <= datetime.date.today()]
    # print(words)
    if size:
        return len(words)
    else:
        return words[:num]


def get_definition(word):
    all_defins = []
    for defins in word.definitions.all():
        if len(defins.definitions.all()) == 0:
            all_defins.append(defins.type)
        else:
            for defin in defins.definitions.all():
                all_defins.append(defin.definition)
    return random.sample(all_defins, 1)


@login_required
def test(request):
    #del request.session['words']
    if 'words' in request.session:
        vwords_id = request.session['words']
        request.session['times'] = [0]

        print(vwords_id)
        vwords = VocabularyWord.objects.filter(word_id__in=vwords_id, user=request.user)
        #vwords = VocabularyWord.objects.filter(id=vwords_id)
        print(vwords)
        # for id in vwords_id:
        #     vwords.append(VocabularyWord.objects.get(id=id))

    else:
        vwords = get_words(request.user, 10)
    if len(vwords) == 0:
        if 'words' in request.session:
            del request.session['words']
            del request.session['times']
            del request.session['results']
        context = {
        }
    else:
        words = Word.objects.filter(vocabularyword__in=vwords)
        words_id = words.values_list('word', flat=True)
        rest = Word.objects.exclude(word__in=words_id)
        rest = rest.filter(language__id=1)
        #rest_id = rest.values_list('id', flat=True)
        #rest = random.sample(rest, 20)
        #rest = rest.filter(id__in=rest)

        rest_id = rest.values_list('id', flat=True)
        ids = []
        for id in rest:
            ids.append(id.id)
        rest_id = random.sample(ids, min(len(rest_id), 50))
        rest = rest.filter(id__in=rest_id)

        print(words)
        print(rest)

        questions = []
        answers = []
        results = []
        vocab = []
        k = 0

        for word in words[:1]:
            answer = []
            vocab.append(word.id)
            type = random.randint(0, 3)
            n = random.randint(0, 3)
            print(type)
            if len(word.translations.all()) == 0 and (type == 0 or type == 1):
                type += 2

            if type == 0:
                question = word
                right_answer = [word.translations.all()[0].translation]
                false_answers = []
                while k <= len(rest):
                    if len(false_answers) == 3:
                        break
                    elif len(rest[k].translations.all()) != 0:
                        false_answers.append([rest[k].translations.all()[0].translation])
                    k += 1

            elif type == 1:
                question = word.translations.all()[0].translation
                right_answer = [word.word]
                false_answers = []
                while k <= len(rest):
                    if len(false_answers) == 3:
                        break
                    elif len(rest[k].translations.all()) != 0:
                        false_answers.append([rest[k].word])
                    k += 1
            elif type == 2:
                question = word
                right_answer = get_definition(word)
                false_answers = []
                while k <= len(rest):
                    if len(false_answers) == 3:
                        break
                    elif len(rest[k].translations.all()) != 0:
                        false_answers.append(get_definition(rest[k]))
                    k += 1
            elif type == 3:
                question = get_definition(word)[0]
                right_answer = [word]
                false_answers = []
                while k <= len(rest):
                    if len(false_answers) == 3:
                        break
                    elif len(rest[k].translations.all()) != 0:
                        false_answers.append([rest[k]])
                    k += 1

            j = 0
            for i in range(4):
                if i == n:
                    answer.append((i, right_answer))
                    results.append(i)
                else:
                    answer.append((i, false_answers[j]))
                    j += 1
            questions.append(question)
            answers.append(answer)

        print(questions)
        print(answers)

        #request.session['test'] = [questions, answers, vwords]
        if 'words' not in request.session:
            request.session['words'] = vocab

            times = []
            for v in vocab:
                times.append(5)
            request.session['times'] = times
        request.session['results'] = results
        context = {
            'question': questions[0],
            'answer': answers[0]
        }
    return render(request, 'vocabulary_manager/test_page.html', context)


def vote(request):
    selected_choice = request.POST['choice']
    print(selected_choice)
    if 'results' in request.session and 'words' in request.session:
        test = request.session['results']
        words = request.session['words']
        times = request.session['times']
        print(test[0])
        print(test[0]==int(selected_choice))
        if test[0] == int(selected_choice) or times[0] == 0:
            print('true')
            request.session['words'] = words[1:]
            request.session['times'] = times[1:]
            request.session['results'] = test[1:]
            word = VocabularyWord.objects.filter(word_id=words[0], user=request.user)[0]
            word.calculate_ef(times[0])
            word.calculate_interval()
            if len(words[1:]) == 0:
                del request.session['words']
                del request.session['times']
                del request.session['results']
        else:
            print('false')
            word = words[0]
            words = words[1:]
            words.append(word)
            time = times[0] - 1
            times = times[1:]
            times.append(time)
            t = test[0]
            test = test[1:]
            test.append(t)
            request.session['words'] = words
            request.session['times'] = times
            request.session['results'] = test
            print(request.session['words'])


        return redirect('/vocabulary/test')
    # try:
    #     selected_choice = request.POSTPOST['choice']
    # except:
    #     # Redisplay the question voting form.
    #     return render(request, 'polls/detail.html', {
    #         'question': question,
    #         'error_message'message: "You didn't select a choice.",
    #     })
    #     else:
    #     selected_choice.votes += 1
    #     selected_choice.save()
    #     # Always return an HttpResponseRedirect after successfully dealingafter
    #     # with POST data. This prevents data from being posted twice if aPOSTposted
    #     # user hits the Back button.
    #     return HttpResponseRedirect(reverse('polls:results'
    #     polls, args = (question.id,)))

@login_required
def add(request, word_id):
    if len(VocabularyWord.objects.filter(word_id=word_id, user=request.user)) == 0:
        v_word = VocabularyWord()
        word = get_object_or_404(Word, pk=word_id)
        v_word.word = word
        v_word.user = request.user
        v_word.language = word.language
        v_word.save()
    return redirect('/dict/word/' + word_id)


@login_required
def delete(request, v_word_id, word_id):
    v_word = get_object_or_404(VocabularyWord, pk=v_word_id)

    if request.user == v_word.user:
        v_word.delete()
        return redirect('/dict/word/' + word_id)
    return redirect('/')