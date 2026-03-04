import traceback
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .RAG import rag_answer
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# Create your views here.
@require_GET
def ask_agent(request):
    question = request.GET.get("q", "").strip()

    if not question:
        return JsonResponse({"answer": "请输入你的问题"}, status=400)

    try:
        answer,context = rag_answer(question)
        return JsonResponse({
            "question": question,
            "answer": answer,
            "context": context
        })
    except Exception as e:
        print("❌ RAG ERROR:")
        traceback.print_exc()

        return JsonResponse({
            "answer": f"后端异常：{str(e)}"
        }, status=500)

def chat_page(request):
    return render(request, "agent/chat.html")