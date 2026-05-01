from django.shortcuts import render

def mirror_view(request):
    """
    Renderiza a interface principal (Frontend) do Smart Mirror.
    Essa será a página exibida em tela cheia (fullscreen) no navegador do Raspberry Pi.
    """
    return render(request, 'widgets/mirror.html')

