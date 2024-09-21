from django.shortcuts import render, redirect, get_object_or_404
from ..forms.question import StoreQuestionForm
from django.contrib.auth.decorators import login_required
from provider_details.models import Store,CommonQuestion
@login_required(login_url='provider-login')
def common_question_list(request):
    store = get_object_or_404(Store, provider__phone=request.user.phone)
    common_questions = store.storeCommonQuestion.all()
    return render(request, 'provider/questions/list.html', {'common_questions': common_questions, 'store': store})

@login_required(login_url='provider-login')
def common_question_create(request):
    store = get_object_or_404(Store, provider__phone=request.user.phone)
    if request.method == 'POST':
        form = StoreQuestionForm(request.POST)
        if form.is_valid():
            common_question = form.save(commit=False)
            common_question.store = store
            common_question.save()
            return redirect('common_question_list')
    else:
        form = StoreQuestionForm()
    return render(request, 'provider/questions/create.html', {'form': form, 'store': store})

@login_required(login_url='provider-login')
def common_question_edit(request, question_id):
    store = get_object_or_404(Store, provider__phone=request.user.phone)
    common_question = get_object_or_404(CommonQuestion, id=question_id)
    if request.method == 'POST':
        form = StoreQuestionForm(request.POST, instance=common_question)
        if form.is_valid():
            form.save()
            return redirect('common_question_list')
    else:
        form = StoreQuestionForm(instance=common_question)
    return render(request, 'provider/questions/update.html', {'form': form, 'store': store, 'common_question': common_question})

@login_required(login_url='provider-login')
def common_question_delete(request, question_id):
    store = get_object_or_404(Store, provider__phone=request.user.phone)
    common_question = get_object_or_404(CommonQuestion, id=question_id, store=store)
    common_question.delete()
    return redirect('common_question_list')