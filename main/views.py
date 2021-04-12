from django.shortcuts import render

# Index View 
def IndexView(request):
    return render( request, 'main/index.html')

def TokenomicsView(request):
    return render( request, 'main/tokenomics.html')

    
